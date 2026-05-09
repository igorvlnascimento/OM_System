"""
Model Registry — unified singleton registry for all model backends.

Backends
--------
TransformersModelRegistry  — HuggingFace Transformers (encoder / decoder)
VLLMModelRegistry          — vLLM (fast GPU inference)
OllamaModelRegistry        — Ollama (local HTTP server)
LlamaCPPModelRegistry      — llama.cpp via llama-cpp-python

All registries share the same abstract interface (ModelRegistry).
Use ModelRegistryFactory.get(backend) to obtain the singleton for a backend.
"""

from __future__ import annotations

import gc
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import torch

CURRENT = Path(__file__).resolve()
PROJECT_ROOT: Path | str = ""

for _parent in CURRENT.parents:
    if (_parent / "pyproject.toml").exists():
        PROJECT_ROOT = _parent
        break

CACHE_DIR = PROJECT_ROOT / "tmp" if PROJECT_ROOT else Path("tmp")


# ─── Abstract base ────────────────────────────────────────────────────────────

class ModelRegistry(ABC):
    """Common interface for all model registry backends."""

    _models: dict[str, Any] = {}

    @abstractmethod
    def load(self, model_name: str, **kwargs) -> dict:
        """Load a model and return its entry dict."""

    @abstractmethod
    def unload(self, model_name: str) -> None:
        """Free resources associated with *model_name*."""

    def is_loaded(self, model_name: str) -> bool:
        return model_name in self._models

    def list_loaded(self) -> list[str]:
        return list(self._models.keys())

    def _get_or_raise(self, model_name: str) -> dict:
        if model_name not in self._models:
            raise RuntimeError(
                f"Model '{model_name}' is not loaded. Call .load() first."
            )
        return self._models[model_name]


# ─── Transformers backend ──────────────────────────────────────────────────────

class TransformersModelRegistry(ModelRegistry):
    """
    Singleton registry for HuggingFace Transformers models.

    Responsibilities
    ----------------
    - Download / cache models to CACHE_DIR via AutoModel / AutoTokenizer.
    - Keep models on a chosen device (CPU or CUDA).
    - Expose tokenization helpers and forward-pass shortcuts.
    - Recover from GPU OOM by evicting cached models and retrying.
    """

    _instance: "TransformersModelRegistry | None" = None
    _models: dict[str, Any] = {}

    def __new__(cls) -> "TransformersModelRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # ── Lifecycle ──────────────────────────────────────────────────────────────

    def load(
        self,
        model_name: str,
        device: str = "cuda",
        attn_implementation: str = "eager",
        dtype: torch.dtype | None = None,
    ) -> dict:
        from transformers import AutoModel, AutoTokenizer

        if model_name in self._models:
            stored = self._models[model_name]
            if stored["attn_implementation"] != attn_implementation:
                raise ValueError(
                    f"Model '{model_name}' is already loaded with "
                    f"attn_implementation={stored['attn_implementation']!r}. "
                    "Unload it first before reloading with different settings."
                )
            return stored

        if dtype is None:
            dtype = torch.float16 if device != "cpu" else torch.float32

        print(f"Loading {model_name} onto {device}...")

        def _load_model():
            return AutoModel.from_pretrained(
                model_name,
                trust_remote_code=True,
                torch_dtype=dtype,
                attn_implementation=attn_implementation,
                cache_dir=CACHE_DIR,
            ).to(device)

        try:
            model = _load_model()
        except torch.cuda.OutOfMemoryError:
            print(
                f"GPU OOM while loading '{model_name}'. "
                "Unloading all GPU models and retrying..."
            )
            evicted = [
                n for n, e in self._models.items() if e["device"] == device
            ]
            for name in evicted:
                self.unload(name)
            model = _load_model()
            for name in evicted:
                try:
                    self.load(name, device=device, attn_implementation=attn_implementation)
                except torch.cuda.OutOfMemoryError:
                    continue

        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=CACHE_DIR)
        entry = {
            "model": model,
            "tokenizer": tokenizer,
            "device": device,
            "attn_implementation": attn_implementation,
            "dtype": dtype,
        }
        self._models[model_name] = entry
        self.freeze_model(model_name)
        print(f"{model_name} loaded onto {device}")
        return entry

    def unload(self, model_name: str) -> None:
        if model_name in self._models:
            del self._models[model_name]
            torch.cuda.empty_cache()
            print(f"{model_name} unloaded")

    # ── Tokenizer helpers ──────────────────────────────────────────────────────

    def tokenize(
        self, model_name: str, text: str | list[str], **kwargs
    ) -> dict[str, torch.Tensor]:
        """Tokenize *text* and return tensors already on the model's device."""
        entry = self._get_or_raise(model_name)
        kwargs.setdefault("padding", True)
        kwargs.setdefault("truncation", True)
        inputs = entry["tokenizer"](text, return_tensors="pt", **kwargs)
        device = entry["device"]
        return {k: v.to(device) for k, v in inputs.items()}

    def tokenize_as_str(
        self, model_name: str, text: str | list[str]
    ) -> list[str]:
        return self._get_or_raise(model_name)["tokenizer"].tokenize(text)

    def convert_tokens_to_ids(
        self, model_name: str, tokens: list[str]
    ) -> list[int]:
        return self._get_or_raise(model_name)["tokenizer"].convert_tokens_to_ids(tokens)

    def get_tokenizer_mask_token(self, model_name: str) -> str:
        return self._get_or_raise(model_name)["tokenizer"].mask_token

    def get_tokenizer_cls_token(self, model_name: str) -> str:
        return self._get_or_raise(model_name)["tokenizer"].cls_token

    def get_tokenizer_sep_token(self, model_name: str) -> str:
        return self._get_or_raise(model_name)["tokenizer"].sep_token

    def get_tokenizer_pad_token_id(self, model_name: str) -> int:
        return self._get_or_raise(model_name)["tokenizer"].pad_token_id

    # ── Inference helpers ──────────────────────────────────────────────────────

    def run(self, model_name: str, text: str | list[str], **kwargs):
        """Tokenize *text* and run a full forward pass. Returns (outputs, inputs)."""
        entry = self._get_or_raise(model_name)
        inputs = self.tokenize(model_name, text, **kwargs)
        model = entry["model"]
        model.eval()
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs, inputs

    def run_from_input_ids(
        self,
        model_name: str,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        **kwargs,
    ):
        """Run inference directly from pre-built tensors."""
        entry = self._get_or_raise(model_name)
        model = entry["model"]
        device = entry["device"]
        model.eval()
        with torch.no_grad():
            outputs = model(
                input_ids=input_ids.to(device),
                attention_mask=attention_mask.to(device),
                **kwargs,
            )
        return outputs

    # ── Model helpers ──────────────────────────────────────────────────────────

    def get_model(self, model_name: str):
        return self._get_or_raise(model_name)["model"]

    def get_tokenizer(self, model_name: str):
        return self._get_or_raise(model_name)["tokenizer"]

    def freeze_model(self, model_name: str) -> None:
        for p in self._get_or_raise(model_name)["model"].parameters():
            p.requires_grad = False

    def get_model_hidden_size(self, model_name: str) -> int:
        return self._get_or_raise(model_name)["model"].config.hidden_size

    def get_model_device(self, model_name: str) -> torch.device:
        return next(self._get_or_raise(model_name)["model"].parameters()).device


# ─── vLLM backend ─────────────────────────────────────────────────────────────

class VLLMModelRegistry(ModelRegistry):
    """
    Singleton registry for vLLM inference engines.

    Responsibilities
    ----------------
    - Instantiate and configure vLLM LLM engines with SamplingParams.
    - Provide a generate() method for batched text generation.
    - Clean up GPU memory on unload via engine shutdown.
    """

    _instance: "VLLMModelRegistry | None" = None
    _models: dict[str, Any] = {}

    def __new__(cls) -> "VLLMModelRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # ── Lifecycle ──────────────────────────────────────────────────────────────

    def load(
        self,
        model_name: str,
        dtype: str = "float16",
        max_model_len: int | None = None,
        max_num_seqs: int = 2,
        max_num_batched_tokens: int | None = None,
        padding_side: str = "left",
        K: int = 10,
        seed: int = 42,
        **kwargs,
    ) -> dict:
        from vllm import LLM, SamplingParams
        from transformers import AutoConfig, AutoTokenizer

        if model_name in self._models:
            return self._models[model_name]

        print(f"Loading {model_name} via vLLM...")
        config = AutoConfig.from_pretrained(model_name)
        max_context = getattr(config, "max_position_embeddings", 8192)
        model_len = (
            max_model_len
            if max_model_len and max_model_len <= max_context
            else max_context
        )
        llm = LLM(
            model=model_name,
            download_dir=str(CACHE_DIR),
            trust_remote_code=True,
            dtype=dtype,
            max_model_len=model_len,
            max_num_seqs=max_num_seqs,
            tensor_parallel_size=1,
            seed=seed,
        )
        tokenizer = AutoTokenizer.from_pretrained(
            model_name, padding_side=padding_side, trust_remote_code=True
        )
        tokenizer.pad_token = tokenizer.eos_token or tokenizer.pad_token
        max_tokens = max_num_batched_tokens or max_context
        params = SamplingParams(
            max_tokens=max_tokens,
            n=K,
            truncate_prompt_tokens=max_context - 1 if model_len >= max_context else None,
            seed=seed,
        )
        entry = {
            "llm": llm,
            "tokenizer": tokenizer,
            "params": params,
        }
        self._models[model_name] = entry
        print(f"{model_name} loaded via vLLM")
        return entry

    def unload(self, model_name: str) -> None:
        if model_name not in self._models:
            return
        llm = self._models[model_name]["llm"]
        if hasattr(llm, "shutdown"):
            llm.shutdown()
        elif hasattr(llm, "llm_engine") and hasattr(llm.llm_engine, "shutdown"):
            llm.llm_engine.shutdown()
        del self._models[model_name]
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        print(f"{model_name} unloaded from vLLM")

    # ── Inference ──────────────────────────────────────────────────────────────

    def generate(
        self,
        model_name: str,
        input_texts: list[str],
        sampling_params=None,
    ) -> list[str]:
        """Generate text for each prompt in *input_texts*."""
        entry = self._get_or_raise(model_name)
        params = sampling_params or entry["params"]
        results = entry["llm"].generate(input_texts, params)
        return [out.text for result in results for out in result.outputs]


# ─── Ollama backend ───────────────────────────────────────────────────────────

class OllamaModelRegistry(ModelRegistry):
    """
    Singleton registry for Ollama-served models.

    Responsibilities
    ----------------
    - Register model names managed by the Ollama server (no local loading).
    - Provide generate() for chat/completion and encode() for embeddings.
    - Pass generation options (temperature, seed, keep_alive) consistently.
    """

    _instance: "OllamaModelRegistry | None" = None
    _models: dict[str, Any] = {}

    def __new__(cls) -> "OllamaModelRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # ── Lifecycle ──────────────────────────────────────────────────────────────

    def load(
        self,
        model_name: str,
        max_model_length: int | None = None,
        seed: int = 42,
        **kwargs,
    ) -> dict:
        """Register *model_name* so it can be referenced in generate/encode calls."""
        if model_name in self._models:
            return self._models[model_name]
        entry = {
            "model_name": model_name,
            "max_model_length": max_model_length,
            "seed": seed,
        }
        self._models[model_name] = entry
        print(f"{model_name} registered in OllamaModelRegistry")
        return entry

    def unload(self, model_name: str) -> None:
        if model_name in self._models:
            del self._models[model_name]
            print(f"{model_name} unregistered from OllamaModelRegistry")

    # ── Inference ──────────────────────────────────────────────────────────────

    def generate(
        self,
        model_name: str,
        prompts: list[list[dict[str, str]]],
        temperature: float = 1.0,
        keep_alive: str = "5m",
    ) -> list[str]:
        """Run chat completion for each prompt (list of message dicts)."""
        import ollama

        entry = self._get_or_raise(model_name)
        results = [
            ollama.chat(
                model=entry["model_name"],
                messages=prompt,
                options={
                    "temperature": temperature,
                    "num_predict": entry["max_model_length"],
                    "seed": entry["seed"],
                    "keep_alive": keep_alive,
                },
            )
            for prompt in prompts
        ]
        return [r["message"]["content"] for r in results]

    def encode(
        self,
        model_name: str,
        input_texts: list[str],
        truncation: bool = True,
    ) -> list:
        """Return embeddings for *input_texts* via the Ollama embed endpoint."""
        import ollama

        entry = self._get_or_raise(model_name)
        return ollama.embed(
            model=entry["model_name"],
            input=input_texts,
            truncate=truncation,
            options={
                "seed": entry["seed"],
                "num_ctx": entry["max_model_length"],
                "keep_alive": 0,
            },
        )["embeddings"]


# ─── llama.cpp backend ────────────────────────────────────────────────────────

class LlamaCPPModelRegistry(ModelRegistry):
    """
    Singleton registry for llama.cpp models via llama-cpp-python.

    Responsibilities
    ----------------
    - Load GGUF model files into memory via llama_cpp.Llama.
    - Provide generate() for chat completion.
    - Free model memory on unload.
    """

    _instance: "LlamaCPPModelRegistry | None" = None
    _models: dict[str, Any] = {}

    def __new__(cls) -> "LlamaCPPModelRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # ── Lifecycle ──────────────────────────────────────────────────────────────

    def load(
        self,
        model_name: str,
        n_ctx: int = 4096,
        n_batch: int | None = None,
        n_gpu_layers: int = -1,
        seed: int = 42,
        verbose: bool = False,
        embedding: bool = False,
        **kwargs,
    ) -> dict:
        """
        Load a llama.cpp model.

        Parameters
        ----------
        model_name:
            Path to a GGUF file or a Hugging Face repo/filename accepted by
            ``llama_cpp.Llama.from_pretrained``.
        n_ctx:
            Context size in tokens.
        n_batch:
            Maximum tokens per decode batch. Defaults to n_ctx. Must be >= n_ctx
            for embedding models and recommended for LLM inference to avoid
            llama_decode errors with certain architectures.
        n_gpu_layers:
            Number of layers offloaded to GPU (-1 = all).
        embedding:
            Enable embedding mode (required for encode()).
        """
        from llama_cpp import Llama

        if model_name in self._models:
            return self._models[model_name]

        if n_batch is None:
            n_batch = n_ctx

        print(f"Loading {model_name} via llama.cpp...")
        model_path = Path(model_name)
        if model_path.exists():
            llm = Llama(
                model_path=str(model_path),
                n_ctx=n_ctx,
                n_batch=n_batch,
                n_gpu_layers=n_gpu_layers,
                seed=seed,
                verbose=verbose,
                embedding=embedding,
            )
        else:
            # Treat model_name as "owner/repo/filename" or just repo slug
            parts = model_name.split("/")
            repo_id = "/".join(parts[:2])
            filename = parts[2] if len(parts) > 2 else None
            llm = Llama.from_pretrained(
                repo_id=repo_id,
                filename=filename,
                n_ctx=n_ctx,
                n_batch=n_batch,
                n_gpu_layers=n_gpu_layers,
                seed=seed,
                verbose=verbose,
                embedding=embedding,
                cache_dir=str(CACHE_DIR),
            )

        if embedding:
            # BERT-based embedding models use bidirectional (non-causal) attention.
            # llama_context defaults to causal_attn=True, which causes llama_decode
            # to return -1 for non-causal models. Disable it explicitly.
            import llama_cpp.llama_cpp as lib
            lib.llama_set_causal_attn(llm._ctx.ctx, False)

        entry = {
            "llm": llm,
            "n_ctx": n_ctx,
            "seed": seed,
        }
        self._models[model_name] = entry
        print(f"{model_name} loaded via llama.cpp")
        return entry

    def unload(self, model_name: str) -> None:
        if model_name in self._models:
            del self._models[model_name]
            gc.collect()
            print(f"{model_name} unloaded from llama.cpp")

    # ── Inference ──────────────────────────────────────────────────────────────

    def generate(
        self,
        model_name: str,
        prompts: list[list[dict[str, str]]],
        max_tokens: int = 512,
        temperature: float = 1.0,
    ) -> list[str]:
        """Run chat completion for each prompt (list of message dicts)."""
        entry = self._get_or_raise(model_name)
        llm = entry["llm"]
        results = []
        for prompt in prompts:
            llm.reset()
            results.append(llm.create_chat_completion(
                messages=self._truncate_messages(llm, prompt, max_tokens),
                max_tokens=max_tokens,
                temperature=temperature,
                seed=entry["seed"],
            ))
        return [r["choices"][0]["message"]["content"] for r in results]

    @staticmethod
    def _truncate_messages(
        llm,
        messages: list[dict[str, str]],
        max_tokens: int,
        overhead: int = 64,
    ) -> list[dict[str, str]]:
        """Truncate the last user message so the prompt fits within n_ctx.

        Parameters
        ----------
        overhead:
            Extra token budget reserved for chat-template formatting tokens
            (role markers, BOS/EOS, etc.) that are not part of the raw content.
        """
        budget = llm.n_ctx() - max_tokens - overhead

        total = sum(
            len(llm.tokenize(m["content"].encode("utf-8", errors="ignore")))
            for m in messages
        )

        if total <= budget:
            return messages

        messages = [m.copy() for m in messages]
        for i in reversed(range(len(messages))):
            if messages[i]["role"] == "user":
                tokens = llm.tokenize(
                    messages[i]["content"].encode("utf-8", errors="ignore")
                )
                excess = total - budget
                tokens = tokens[: max(1, len(tokens) - excess)]
                messages[i]["content"] = llm.detokenize(tokens).decode(
                    "utf-8", errors="ignore"
                )
                break
        return messages

    def encode(
        self,
        model_name: str,
        input_texts: list[str],
        truncation: bool = True,
    ) -> list:
        """Return embeddings for *input_texts*. Requires embedding=True at load time.

        Texts are encoded one at a time. Passing a list to embed() packs multiple
        short sequences into a single batch, which fails for BERT-based models on GPU.
        """
        entry = self._get_or_raise(model_name)
        llm = entry["llm"]
        return [llm.embed(text) for text in input_texts]


# ─── Factory ──────────────────────────────────────────────────────────────────

class ModelRegistryFactory:
    """
    Return the singleton ModelRegistry for a given backend.

    Supported backends
    ------------------
    "transformers"  -> TransformersModelRegistry
    "vllm"          -> VLLMModelRegistry
    "ollama"        -> OllamaModelRegistry
    "llamacpp"      -> LlamaCPPModelRegistry
    """

    _registry_classes: dict[str, type[ModelRegistry]] = {
        "transformers": TransformersModelRegistry,
        "vllm": VLLMModelRegistry,
        "ollama": OllamaModelRegistry,
        "llamacpp": LlamaCPPModelRegistry,
    }

    @staticmethod
    def get(backend: str) -> ModelRegistry:
        cls = ModelRegistryFactory._registry_classes.get(backend)
        if cls is None:
            supported = list(ModelRegistryFactory._registry_classes)
            raise ValueError(
                f"Unknown backend '{backend}'. Supported: {supported}"
            )
        return cls()

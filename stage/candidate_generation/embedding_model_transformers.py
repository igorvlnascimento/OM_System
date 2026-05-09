import torch
from torch import Tensor
from torch.nn import functional as F
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm

from stage.model_registry import ModelRegistryFactory
from stage.candidate_generation.embedding_model import EmbeddingModel


class EmbeddingModelTransformers(EmbeddingModel):
    def __init__(
        self,
        model_name: str,
        cache_dir=None,
        padding_side: str = "left",
        max_length: int | None = None,
        batch_size: int = 2,
        padding: bool = True,
        use_cuda: bool | None = None,
    ):
        self.model_name = model_name
        self.use_cuda = torch.cuda.is_available() if use_cuda is None else use_cuda
        self.max_length = max_length
        self.batch_size = batch_size
        self.padding = padding

        device = "cuda" if self.use_cuda else "cpu"
        self.registry = ModelRegistryFactory.get("transformers")
        self.registry.load(model_name, device=device)

        # Set padding_side on the tokenizer after loading
        self.registry.get_tokenizer(model_name).padding_side = padding_side

    # ── EmbeddingModel interface ───────────────────────────────────────────────

    def similarity(self, embeddings1, embeddings2):
        return embeddings1 @ embeddings2.T

    def encode(self, input_texts, truncation=True):
        batch_dict = self.tokenize(
            input_texts,
            max_length=self.max_length,
            padding=self.padding,
            truncation=truncation,
        )
        with torch.no_grad():
            return torch.cat(
                [
                    self.embed(x, a)
                    for x, a in tqdm(
                        DataLoader(
                            TensorDataset(
                                batch_dict["input_ids"],
                                batch_dict["attention_mask"],
                            ),
                            batch_size=self.batch_size,
                            shuffle=False,
                        )
                    )
                ],
                dim=0,
            )

    def clean_memory(self) -> None:
        self.registry.unload(self.model_name)

    # ── Internal helpers ───────────────────────────────────────────────────────

    def tokenize(self, input_texts, max_length=8192, padding=True, truncation=True):
        tokenizer = self.registry.get_tokenizer(self.model_name)
        return tokenizer(
            input_texts,
            padding=padding,
            truncation=truncation,
            max_length=max_length,
            return_tensors="pt",
        )

    def embed(self, input_ids: Tensor, attention_mask: Tensor) -> Tensor:
        outputs = self.registry.run_from_input_ids(
            self.model_name,
            input_ids,
            attention_mask,
            use_cache=False,
        )
        embedding = self._last_token_pool(outputs.last_hidden_state.cpu(), attention_mask)
        return F.normalize(embedding.cpu(), p=2, dim=1)

    def _last_token_pool(
        self, last_hidden_states: Tensor, attention_mask: Tensor
    ) -> Tensor:
        left_padding = attention_mask[:, -1].sum() == attention_mask.shape[0]
        if left_padding:
            return last_hidden_states[:, -1]
        sequence_lengths = attention_mask.sum(dim=1) - 1
        batch_size = last_hidden_states.shape[0]
        return last_hidden_states[
            torch.arange(batch_size, device=last_hidden_states.device),
            sequence_lengths,
        ]

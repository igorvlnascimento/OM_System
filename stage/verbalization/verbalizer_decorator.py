from abc import ABC

from rdflib import RDFS

DOMAIN_RANGE = {RDFS.domain, RDFS.range}


class Verbalizer(ABC):
    concept_dict: dict

    def verbalize(self, value):
        if isinstance(value, list):
            return self._verbalize_triples(value)
        return self._ensure_label(value)

    def verbalize_triple(self, module):
        return self._verbalize_triples(module)

    def _verbalize_triples(self, triples):
        merged = self._merge_domain_range(triples)
        return [
            tuple(self._ensure_label(iri) for iri in triple)
            for triple in merged
        ]

    def _ensure_label(self, iri):
        key = str(iri)
        if key not in self.concept_dict:
            self.concept_dict[key] = self._compute_label(iri)
        return self.concept_dict[key]

    def _compute_label(self, iri):
        return str(iri)

    def _merge_domain_range(self, triples):
        pending = {}
        result = []
        for s, p, o in triples:
            if p in DOMAIN_RANGE and s in pending:
                prev_p, prev_o, prev_idx = pending.pop(s)
                if {p, prev_p} == DOMAIN_RANGE:
                    if prev_p == RDFS.domain:
                        result[prev_idx] = (prev_o, s, o)
                    else:
                        result[prev_idx] = (o, s, prev_o)
                    continue
            if p in DOMAIN_RANGE:
                pending[s] = (p, o, len(result))
            result.append((s, p, o))
        return result

    def get_label_from_iri(self, iri):
        return iri.split("#")[-1] if "#" in iri else iri.split("/")[-1]


class VerbalizerDecorator(Verbalizer):
    def __init__(self, component: Verbalizer):
        self._component = component

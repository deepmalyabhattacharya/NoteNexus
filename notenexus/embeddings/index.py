from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Any

import numpy as np

try:
    import faiss  # type: ignore
except Exception:  # pragma: no cover
    faiss = None  # type: ignore

from notenexus.config import DEFAULT_MODEL_CONFIG


@dataclass
class EmbeddingResult:
    ids: List[str]
    embeddings: np.ndarray


class EmbeddingIndex:
    def __init__(self, model_name: str | None = None) -> None:
        self.model_name: str = model_name or DEFAULT_MODEL_CONFIG.embedding_model
        self.model: Any | None = None
        self.dim: int | None = None
        self.texts: list[str] = []
        self.ids: list[str] = []
        self.index = None  # lazily created when needed

    def _ensure_model(self) -> None:
        if self.model is None:
            # Lazy import to avoid importing heavy libs on module import
            from sentence_transformers import SentenceTransformer  # type: ignore

            self.model = SentenceTransformer(self.model_name)
            try:
                self.dim = self.model.get_sentence_embedding_dimension()
            except Exception:
                # Fallback: infer dimension on first encode
                self.dim = None

    def _ensure_faiss_index(self, dim: int) -> None:
        if self.index is None and faiss is not None:
            self.index = faiss.IndexFlatIP(dim)

    def add(self, ids: List[str], texts: List[str]) -> EmbeddingResult:
        assert len(ids) == len(texts)
        self._ensure_model()
        embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        effective_dim = embeddings.shape[1]
        if self.index is None and faiss is not None:
            self._ensure_faiss_index(effective_dim)
        if self.index is not None:
            self.index.add(embeddings)
        self.ids.extend(ids)
        self.texts.extend(texts)
        return EmbeddingResult(ids=ids, embeddings=embeddings)

    def search(self, query: str, k: int = 5) -> List[Tuple[str, float, str]]:
        if not self.texts:
            return []
        self._ensure_model()
        query_emb = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        if self.index is not None:
            k_eff = min(k, len(self.texts))
            scores, indices = self.index.search(query_emb, k_eff)
            idxs = indices[0]
            scs = scores[0]
        else:
            # Fallback cosine similarity
            matrix = self.model.encode(self.texts, convert_to_numpy=True, normalize_embeddings=True)
            sims = (matrix @ query_emb.T).squeeze(1)
            idxs = np.argsort(-sims)[:k]
            scs = sims[idxs]
        results: List[Tuple[str, float, str]] = []
        for idx, score in zip(idxs, scs):
            if 0 <= idx < len(self.texts):
                results.append((self.ids[idx], float(score), self.texts[idx]))
        return results

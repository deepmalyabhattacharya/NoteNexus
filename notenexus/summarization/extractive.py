from __future__ import annotations

from typing import List

import networkx as nx
import nltk
from nltk.tokenize import sent_tokenize


def _sentence_similarity(sent1: str, sent2: str) -> float:
    words1 = set(w.lower() for w in sent1.split())
    words2 = set(w.lower() for w in sent2.split())
    if not words1 or not words2:
        return 0.0
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / max(1, len(union))


def textrank_summarize(text: str, max_sentences: int = 5) -> str:
    # Ensure punkt is available at runtime; download if missing
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")

    sentences: List[str] = [s.strip() for s in sent_tokenize(text) if s.strip()]
    if not sentences:
        return ""
    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    graph = nx.Graph()
    for i, si in enumerate(sentences):
        for j in range(i + 1, len(sentences)):
            sj = sentences[j]
            sim = _sentence_similarity(si, sj)
            if sim > 0:
                graph.add_edge(i, j, weight=sim)

    if graph.number_of_edges() == 0:
        # Fallback: take the first N sentences
        return " ".join(sentences[:max_sentences])

    scores = nx.pagerank(graph, weight="weight")
    ranked_indices = sorted(scores, key=scores.get, reverse=True)[:max_sentences]
    ranked_indices.sort()
    summary = " ".join(sentences[idx] for idx in ranked_indices)
    return summary

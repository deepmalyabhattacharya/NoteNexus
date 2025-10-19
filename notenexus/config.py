from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ModelConfig:
    summarizer_model: str = "facebook/bart-large-cnn"
    qa_model: str = "deepset/roberta-base-squad2"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"


@dataclass(frozen=True)
class AppConfig:
    enable_gpu: bool = True
    max_summary_sentences: int = 5
    max_input_length: int = 4096
    faiss_use_gpu: bool = False


DEFAULT_MODEL_CONFIG = ModelConfig()
DEFAULT_APP_CONFIG = AppConfig()

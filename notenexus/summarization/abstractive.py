from __future__ import annotations

from notenexus.config import DEFAULT_MODEL_CONFIG

_summarizer = None


def get_summarizer():
    global _summarizer
    if _summarizer is None:
        # Lazy import to avoid heavy import on module load
        from transformers import pipeline  # type: ignore

        _summarizer = pipeline(
            "summarization",
            model=DEFAULT_MODEL_CONFIG.summarizer_model,
            framework="pt",
        )
    return _summarizer


def generate_summary(text: str, max_length: int = 256, min_length: int = 64) -> str:
    if not text.strip():
        return ""
    summarizer = get_summarizer()
    result = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return result[0]["summary_text"].strip()

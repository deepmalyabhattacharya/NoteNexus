from __future__ import annotations

from notenexus.config import DEFAULT_MODEL_CONFIG

_qa = None


def get_qa_pipeline():
    global _qa
    if _qa is None:
        from transformers import pipeline  # type: ignore

        _qa = pipeline("question-answering", model=DEFAULT_MODEL_CONFIG.qa_model, framework="pt")
    return _qa


def answer_question(question: str, context: str) -> dict:
    if not question.strip() or not context.strip():
        return {"answer": "", "score": 0.0, "start": -1, "end": -1}
    qa = get_qa_pipeline()
    return qa(question=question, context=context)

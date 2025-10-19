from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from notenexus.config import DEFAULT_APP_CONFIG
from notenexus.summarization.extractive import textrank_summarize
from notenexus.summarization.abstractive import generate_summary
from notenexus.qa.pipeline import answer_question
from notenexus.embeddings.index import EmbeddingIndex
from notenexus.storage.memory import InMemoryStore


app = FastAPI(title="NoteNexus", version="0.1.0")
store = InMemoryStore()
_index: EmbeddingIndex | None = None


def get_index() -> EmbeddingIndex:
    global _index
    if _index is None:
        _index = EmbeddingIndex()
    return _index


class NoteIn(BaseModel):
    id: str
    text: str


class SummarizeIn(BaseModel):
    id: str
    mode: str = "extractive"  # or "abstractive"


class QAIn(BaseModel):
    question: str
    id: str | None = None


class SearchIn(BaseModel):
    query: str
    k: int = 5


@app.post("/notes")
async def create_or_update_note(note: NoteIn):
    store.put(note.id, note.text)
    get_index().add([note.id], [note.text])
    return {"status": "ok", "id": note.id}


@app.get("/notes/{note_id}")
async def get_note(note_id: str):
    n = store.get(note_id)
    if not n:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"id": n.id, "text": n.text}


@app.post("/summarize")
async def summarize(body: SummarizeIn):
    n = store.get(body.id)
    if not n:
        raise HTTPException(status_code=404, detail="Note not found")
    if body.mode == "extractive":
        summary = textrank_summarize(n.text, max_sentences=DEFAULT_APP_CONFIG.max_summary_sentences)
    elif body.mode == "abstractive":
        summary = generate_summary(n.text)
    else:
        raise HTTPException(status_code=400, detail="Invalid mode")
    return {"id": body.id, "mode": body.mode, "summary": summary}


@app.post("/qa")
async def qa(body: QAIn):
    if body.id:
        n = store.get(body.id)
        if not n:
            raise HTTPException(status_code=404, detail="Note not found")
        context = n.text
    else:
        # retrieve top results and build context
        results = get_index().search(body.question, k=5)
        context = "\n\n".join(text for _, _, text in results)
    ans = answer_question(body.question, context)
    return {"question": body.question, "answer": ans.get("answer", ""), "score": ans.get("score", 0.0)}


@app.post("/search")
async def search(body: SearchIn):
    results = get_index().search(body.query, k=body.k)
    return {
        "query": body.query,
        "results": [
            {"id": _id, "score": score, "text": text}
            for _id, score, text in results
        ],
    }

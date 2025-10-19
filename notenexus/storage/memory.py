from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Note:
    id: str
    text: str


class InMemoryStore:
    def __init__(self) -> None:
        self._notes: Dict[str, Note] = {}

    def put(self, note_id: str, text: str) -> Note:
        note = Note(id=note_id, text=text)
        self._notes[note_id] = note
        return note

    def get(self, note_id: str) -> Optional[Note]:
        return self._notes.get(note_id)

    def all(self) -> List[Note]:
        return list(self._notes.values())

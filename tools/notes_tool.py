import json
import os
from datetime import datetime
import uuid

NOTES_FILE = "data/notes.json"

def _load_notes():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r") as f:
        return json.load(f)

def _save_notes(notes):
    os.makedirs("data", exist_ok=True)
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)

def add_note(content: str, tags: str = "") -> str:
    notes = _load_notes()
    note = {
        "id": str(uuid.uuid4())[:8],
        "content": content,
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "created_at": datetime.now().isoformat()
    }
    notes.append(note)
    _save_notes(notes)
    return f"Note added with ID: {note['id']}"

def list_notes(limit: int = 10) -> str:
    notes = _load_notes()
    notes = sorted(notes, key=lambda x: x["created_at"], reverse=True)[:limit]
    if not notes:
        return "No notes found."
    return "\n".join([f"[{n['id']}] {n['created_at'][:16]} - {n['content'][:80]}" for n in notes])

def search_notes(query: str) -> str:
    notes = _load_notes()
    query = query.lower()
    matches = [n for n in notes if query in n["content"].lower() or any(query in t.lower() for t in n["tags"])]
    if not matches:
        return f"No notes matching '{query}'"
    return "\n".join([f"[{n['id']}] {n['content']}" for n in matches[:10]])

def delete_note(note_id: str) -> str:
    notes = _load_notes()
    original_len = len(notes)
    notes = [n for n in notes if n["id"]!= note_id]
    if len(notes) == original_len:
        return f"Note {note_id} not found"
    _save_notes(notes)
    return f"Note {note_id} deleted"
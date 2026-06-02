import httpx
import json
import os
from tools.notes_tool import _load_notes, add_note

OLLAMA_MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"

def _ollama_generate(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7}
    }
    try:
        with httpx.Client(timeout=60) as client:
            r = client.post(OLLAMA_URL, json=payload)
            r.raise_for_status()
            data = r.json()
            return data.get("response", "").strip()
    except Exception as e:
        return f"Error calling Ollama: {e}"

def ask_llm(prompt: str) -> str:
    """Ask local LLM a question"""
    if not prompt.strip():
        return "Please provide a prompt"
    return _ollama_generate(prompt)

def summarize_my_notes() -> str:
    """Summarize all personal notes"""
    notes = _load_notes()
    if not notes:
        return "No notes to summarize"
    notes_text = "\n".join([f"- {n['content']}" for n in notes[-20:]])
    prompt = f"Summarize these personal notes into 3-5 concise bullet points:\n\n{notes_text}"
    summary = _ollama_generate(prompt)
    return f"Notes summary:\n{summary}"

def generate_note(topic: str) -> str:
    """Generate a note about a topic and save it"""
    if not topic.strip():
        return "Please provide a topic"
    prompt = f"Write a short, actionable personal note about: {topic}\nReturn only the note text, no preamble."
    content = _ollama_generate(prompt)
    # Save it
    save_result = add_note(content)
    return f"Generated note about '{topic}':\n{content}\n\n{save_result}"

def explain_note(note_id: str) -> str:
    """Explain a note by ID in simple terms"""
    notes = _load_notes()
    note = next((n for n in notes if n['id'] == note_id), None)
    if not note:
        return f"Note {note_id} not found"
    prompt = f"Explain this personal note in one clear sentence:\n\n{note['content']}"
    explanation = _ollama_generate(prompt)
    return f"Note: {note['content']}\nExplanation: {explanation}"
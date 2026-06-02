from mcp.server.fastmcp import FastMCP

from tools.time_tool import get_current_time, get_timezone_info
from tools.weather_tool import get_weather
from tools.notes_tool import add_note, list_notes, search_notes, delete_note
from tools.system_tool import get_system_info
from tools.llm_tool import ask_llm, summarize_my_notes, generate_note, explain_note
from tools.profile_tool import get_user_profile

mcp = FastMCP("Personal Assistant")

@mcp.tool()
def who_am_i() -> str:
    return get_user_profile()

@mcp.tool()
def current_time() -> str:
    """Get current time in Asia/Kuala_Lumpur"""
    return get_current_time()

@mcp.tool()
def timezone_info() -> str:
    """Get timezone information"""
    return get_timezone_info()

@mcp.tool()
def weather(city: str = "Kuala Lumpur") -> str:
    """Get current weather for a Malaysian city"""
    return get_weather(city)

@mcp.tool()
def add_personal_note(content: str) -> str:
    """Add a personal note"""
    return add_note(content)

@mcp.tool()
def list_personal_notes() -> str:
    """List all personal notes"""
    return list_notes()

@mcp.tool()
def search_personal_notes(query: str) -> str:
    """Search notes by keyword"""
    return search_notes(query)

@mcp.tool()
def delete_personal_note(note_id: str) -> str:
    """Delete a note by ID"""
    return delete_note(note_id)

@mcp.tool()
def system_info() -> str:
    """Get system information"""
    return get_system_info()

@mcp.tool()
def ask_local_llm(prompt: str) -> str:
    """Ask local Ollama LLM a question"""
    return ask_llm(prompt)

@mcp.tool()
def summarize_my_notes_tool() -> str:
    """Summarize all personal notes using local LLM"""
    return summarize_my_notes()

@mcp.tool()
def generate_note_tool(topic: str) -> str:
    """Generate and save a note about a topic using local LLM"""
    return generate_note(topic)

@mcp.tool()
def explain_note_tool(note_id: str) -> str:
    """Explain a note by ID using local LLM"""
    return explain_note(note_id)

if __name__ == "__main__":
    mcp.run()
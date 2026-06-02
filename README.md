# MCP Personal Assistant Server

A local Model Context Protocol (MCP) server with 12 personal assistant tools. Works with Claude Desktop, 5ire, or the included offline client using Ollama.

## Features

### 12 Tools

- **current_time** - Get current time in any timezone
- **system_info** - CPU, memory, disk, OS info
- **weather** - Weather lookup via wttr.in
- **take_notes** - Save markdown notes
- **read_notes** - Read a note by ID
- **list_notes** - List all notes
- **delete_notes** - Delete a note
- **remember** - Store key-value memories
- **recall** - Recall a memory by key
- **who_am_i** - List all stored memories
- **search_web** - DuckDuckGo search
- **ask_local_llm** - Query local Ollama model

Data is stored in `./data/` as JSON and Markdown files. No database required.

## Quick Start

### 1. Setup

```bash
git clone <your-repo>
cd mcp-personal-assistant-server
python3 -m venv .venv
source .venv/bin/activate
pip install mcp psutil requests
```

### 2. Install Ollama

```bash
brew install ollama
ollama serve
ollama pull llama3.2
```

### 3. Run Offline Client

```bash
python offline_client.py
```

Commands:
- `time in Kuala Lumpur`
- `system info`
- `weather Tokyo`
- `note: buy milk`
- `list notes`
- `remember my name is Firdaus`
- `who am i`
- `search Python MCP`
- `ask: what is MCP?`
- `quit`

## Claude Desktop Setup

### Config file location
macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Example config
```json
{
  "mcpServers": {
    "personal-assistant": {
      "command": "/Users/firdausaslam/Documents/Work/Workstation/GitHub/mcp-personal-assistant-server/.venv/bin/python",
      "args": ["/Users/firdausaslam/Documents/Work/Workstation/GitHub/mcp-personal-assistant-server/server.py"],
      "cwd": "/Users/firdausaslam/Documents/Work/Workstation/GitHub/mcp-personal-assistant-server",
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

Restart Claude Desktop after editing. Test with: "What time is it?"

### Install Claude Desktop without admin

```bash
mkdir -p ~/Applications
brew install --cask --appdir=~/Applications claude
open ~/Applications/Claude.app
```

## Project Structure

```
mcp-personal-assistant-server/
├── server.py           # MCP server with 12 tools
├── offline_client.py   # Standalone CLI client
├── data/
│   ├── notes/          # Markdown notes
│   └── memory.json     # Key-value store
├── .venv/              # Python virtual env
└── README.md
```

## Requirements

- Python 3.9+
- mcp
- psutil
- requests
- Ollama (for ask_local_llm)

## Adding Tools

Edit `server.py`:

```python
@mcp.tool()
def my_tool(arg: str) -> str:
    # Description for LLM
    return f"Result: {arg}"
```

Restart client/Claude Desktop to load.

## Troubleshooting

**Config not loaded**
- Quit Claude completely: `Cmd+Q`
- Validate JSON: `cat config.json | python3 -m json.tool`

**Server crashes**
- Test import: `python -c "import server; print('OK')"`
- Check python path in config matches `.venv/bin/python`

**Ollama not responding**
- Ensure `ollama serve` is running
- Pull model: `ollama pull llama3.2`

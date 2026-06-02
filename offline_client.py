import asyncio
import json
import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

OLLAMA_MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/chat"

SERVER_PARAMS = StdioServerParameters(
    command=".venv/bin/python",
    args=["server.py"],
)

async def call_ollama(messages, tools=None):
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.2}
    }
    if tools:
        payload["tools"] = tools
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(OLLAMA_URL, json=payload)
        r.raise_for_status()
        return r.json()

async def main():
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_resp = await session.list_tools()
            mcp_tools = []
            for t in tools_resp.tools:
                mcp_tools.append({
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description or "",
                        "parameters": t.inputSchema
                    }
                })

            print(f"Connected. {len(mcp_tools)} tools loaded. Model: {OLLAMA_MODEL}\n")

            messages = [{
                "role": "system",
                "content": "You are a helpful assistant with access to tools. Always call a tool when the user asks for time, weather, notes, system info, or LLM tasks. After a tool returns data, summarize it briefly in natural language and show the key result."
            }]

            while True:
                user = input("You: ").strip()
                if user.lower() in ("exit", "quit"):
                    break
                if not user:
                    continue

                messages.append({"role": "user", "content": user})
                resp = await call_ollama(messages, tools=mcp_tools)
                msg = resp["message"]

                # Handle tool calls
                while msg.get("tool_calls"):
                    messages.append(msg)
                    for tc in msg["tool_calls"]:
                        fname = tc["function"]["name"]
                        args = tc["function"]["arguments"]
                        if isinstance(args, str):
                            args = json.loads(args)
                        print(f"\n→ Calling {fname} {args}")
                        result = await session.call_tool(fname, args)
                        tool_text = result.content[0].text if result.content else str(result)
                        print(f"✓ Result: {tool_text[:200]}{'...' if len(tool_text)>200 else ''}\n")

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tc.get("id"),
                            "name": fname,
                            "content": tool_text
                        })

                    # Get next response
                    resp = await call_ollama(messages, tools=mcp_tools)
                    msg = resp["message"]

                print(f"Assistant: {msg['content']}\n")
                messages.append(msg)

if __name__ == "__main__":
    asyncio.run(main())
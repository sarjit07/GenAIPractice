"""
A minimal MCP server, built with FastMCP (part of the official `mcp` SDK).

This process knows nothing about Claude or any LLM — it just exposes a
handful of tools over the MCP protocol (stdio transport) and answers
tools/list and tools/call requests. It is spawned as a subprocess by the
MCP client in mcp.ipynb.

Run it directly to sanity-check it starts:
    python mcp_server.py
(it will sit waiting for JSON-RPC on stdin — Ctrl+C to exit)
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("demo-server")

# In-memory state for the notes tools, just to demonstrate a server that
# holds state across multiple tool calls within one connection.

_notes: list[str] = []


@mcp.tool()
def calculate(expression: str) -> str:
    """Evaluate a basic arithmetic expression (+, -, *, /, parentheses) and return the result.

    Args:
        expression: e.g. "12 * (3 + 4)"
    """
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return f"Error: expression contains disallowed characters: {expression!r}"
    try:
        result = eval(expression, {"__builtins__": {}}, {})
    except Exception as e:
        return f"Error evaluating expression: {e}"
    return str(result)


@mcp.tool()
def remember(note: str) -> str:
    """Store a short note in the server's in-memory list for later recall.

    Args:
        note: The text to remember.
    """
    _notes.append(note)
    return f"Stored note #{len(_notes)}: {note!r}"


@mcp.tool()
def recall() -> str:
    """Return every note stored so far via the remember tool."""
    if not _notes:
        return "No notes stored yet."
    return "\n".join(f"{i + 1}. {n}" for i, n in enumerate(_notes))


if __name__ == "__main__":
    mcp.run(transport="stdio")

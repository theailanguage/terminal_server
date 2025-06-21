#!/usr/bin/env python

"""
terminal_server_sse.py

This file implements an MCP server using the SSE (Server-Sent Events) transport protocol.
It uses the FastMCP framework to expose tools that clients can call over an SSE connection.
SSE allows real-time, one-way communication from server to client over HTTP — ideal for pushing model updates.

The server uses:
- `Starlette` for the web server
- `uvicorn` as the ASGI server
- `FastMCP` from `mcp.server.fastmcp` to define the tools
- `SseServerTransport` to handle long-lived SSE connections
"""

#   [ MCP Client / Agent in Browser ]
#                  |
#      (connects via SSE over HTTP)
#                  |
#           [ Uvicorn Server ]
#                  |
#          (ASGI Protocol Bridge)
#                  |
#           [ Starlette App ]
#                  |
#           [ FastMCP Server ]
#                  |
#     @mcp.tool() like `add_numbers`, `run_command`



import os
import subprocess  # For running shell commands
from mcp.server.fastmcp import FastMCP  # Core MCP wrapper to define tools and expose them
from mcp.server import Server  # Underlying server abstraction used by FastMCP
from mcp.server.sse import SseServerTransport  # The SSE transport layer

from starlette.applications import Starlette  # Web framework to define routes
from starlette.routing import Route, Mount  # Routing for HTTP and message endpoints
from starlette.requests import Request  # HTTP request objects

import uvicorn  # ASGI server to run the Starlette app

# --------------------------------------------------------------------------------------
# STEP 1: Initialize FastMCP instance — this acts as your "tool server"
# --------------------------------------------------------------------------------------
mcp = FastMCP("terminal")  # Name of the server for identification purposes

# Default directory where shell commands will run (used in run_command tool)
DEFAULT_WORKSPACE = os.path.expanduser("~/mcp/workspace")


# --------------------------------------------------------------------------------------
# TOOL 1: run_command — execute a shell command and return output
# --------------------------------------------------------------------------------------
@mcp.tool()
async def run_command(command: str) -> str:
    """
    Executes a shell command in the default workspace and returns the result.

    Args:
        command (str): A shell command like 'ls', 'pwd', etc.

    Returns:
        str: Standard output or error message from running the command.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=DEFAULT_WORKSPACE,
            capture_output=True,
            text=True
        )
        return result.stdout or result.stderr
    except Exception as e:
        return str(e)


# --------------------------------------------------------------------------------------
# TOOL 2: add_numbers — adds two numbers and returns the result
# --------------------------------------------------------------------------------------
@mcp.tool()
async def add_numbers(a: float, b: float) -> float:
    """
    Adds two numbers and returns the sum.

    Args:
        a (float): The first number
        b (float): The second number

    Returns:
        float: The sum of a and b
    """
    return a + b


# --------------------------------------------------------------------------------------
# STEP 2: Create the Starlette app to expose the tools via HTTP (using SSE)
# --------------------------------------------------------------------------------------
def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """
    Constructs a Starlette app with SSE and message endpoints.

    Args:
        mcp_server (Server): The core MCP server instance.
        debug (bool): Enable debug mode for verbose logs.

    Returns:
        Starlette: The full Starlette app with routes.
    """
    # Create SSE transport handler to manage long-lived SSE connections
    sse = SseServerTransport("/messages/")

    # This function is triggered when a client connects to `/sse`
    async def handle_sse(request: Request) -> None:
        """
        Handles a new SSE client connection and links it to the MCP server.
        """
        # Open an SSE connection, then hand off read/write streams to MCP
        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,  # Low-level send function provided by Starlette
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    # Return the Starlette app with configured endpoints
    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),          # For initiating SSE connection
            Mount("/messages/", app=sse.handle_post_message),  # For POST-based communication
        ],
    )


# --------------------------------------------------------------------------------------
# STEP 3: Start the server using Uvicorn if this file is run directly
# --------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Get the underlying MCP server instance from FastMCP
    mcp_server = mcp._mcp_server  # Accessing private member (acceptable here)

    # Command-line arguments for host/port control
    import argparse

    parser = argparse.ArgumentParser(description='Run MCP SSE-based server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8081, help='Port to listen on')
    args = parser.parse_args()

    # Build the Starlette app with debug mode enabled
    starlette_app = create_starlette_app(mcp_server, debug=True)

    # Launch the server using Uvicorn
    uvicorn.run(starlette_app, host=args.host, port=args.port)

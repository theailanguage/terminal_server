# MCP Server for Executing Terminal Commands

## Introduction

Hey everyone! Welcome back to **The AI Language**. In this project, we’re building an **MCP server that can execute terminal commands**. This allows you to ask **Claude for Desktop** to run commands on your computer and return the output — like using a terminal, but powered by AI!

> 🎥 Video tutorials:
>
> - **Without Docker:** [Watch here](https://youtu.be/_veLqeCzdIQ)
> - **With Docker:** [Watch here](https://youtu.be/cgml6yzrOjc)

[SUBSCRIBE](https://youtube.com/@theailanguage?sub_confirmation=1)

If you enjoy learning about AI, coding, and automation, please **like and subscribe** to the channel — it really helps us make more great content for you!


---

## What is MCP?

**MCP (Model Context Protocol)** is a system that allows AI models to:

- **Store data** (like files or API responses)
- **Run tools** (functions that AI can execute)
- **Use prompts** (predefined templates for tasks)

In this tutorial, we’re building a tool that takes a command, runs it in the terminal, and sends back the output.

---

## Two Ways to Set Up Your MCP Server

You can run your MCP server **with or without Docker**:

### 🔹 Option 1: Run Directly Using Python (no Docker)

This is great for development or local experimentation.

### 🔹 Option 2: Run Using Docker

Perfect for clean environments and easy distribution — no need to install Python or dependencies globally.

Both methods work with **Claude for Desktop**, and we’ll walk you through both.

---

## Option 1: Setup Without Docker (Local Python)

### Step 1: Install Python and `uv`

You need **Python 3.10 or higher** and a tool called `uv`:

- Install Python: https://www.python.org/downloads/
- Install `uv`:
  ```sh
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- Fix permissions if needed:
  ```sh
  sudo chown -R $(whoami):staff ~/.local
  ```

### Step 2: Create Project Structure
```sh
mkdir -p ~/mcp/servers/terminal_server
mkdir -p ~/mcp/workspace
cd ~/mcp/servers/terminal_server
```

### Step 3: Initialize and Activate Project
```sh
uv init
uv venv
source .venv/bin/activate  # Mac/Linux
# or
.venv\Scripts\activate     # Windows
```

### Step 4: Install Required Packages
```sh
uv add "mcp[cli]"
```

### Step 5: Create Your Server
Create `terminal_server.py` and paste this:

```python
import os
import subprocess
import logging
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logging.info("Starting Terminal Server MCP...")

mcp = FastMCP("terminal")
DEFAULT_WORKSPACE = os.path.expanduser("~/mcp/workspace")
logging.info(f"Workspace path: {DEFAULT_WORKSPACE}")

@mcp.tool()
async def run_command(command: str) -> str:
    logging.info(f"Running command: {command}")
    try:
        result = subprocess.run(command, shell=True, cwd=DEFAULT_WORKSPACE, capture_output=True, text=True)
        return result.stdout or result.stderr
    except Exception as e:
        logging.exception("Command failed")
        return str(e)

if __name__ == "__main__":
    mcp.run(transport='stdio')
```

### Step 6: Start the Server
```sh
uv run terminal_server.py
```

---

## Option 2: Setup With Docker

### Step 1: Create a Dockerfile
In the same folder as `terminal_server.py`, create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "terminal_server.py"]
```

Make sure you have a `requirements.txt` that includes:
```
mcp[cli]
```

### Step 2: Build the Docker Image
```sh
docker build -t terminal_server_docker .
```

### Step 3: Configure Claude Desktop to Use the Docker Image
Open:
```sh
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Add:
```json
{
  "mcpServers": {
    "terminal_server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--init",
        "-e", "DOCKER_CONTAINER=true",
        "-v", "/Users/<your-username>/mcp/workspace:/root/mcp/workspace",
        "terminal_server_docker"
      ]
    }
  }
}
```
> Replace `<your-username>` with your actual macOS username.

Then restart Claude Desktop.

---

## Testing the MCP Server

In Claude, try these prompts:

- `Run the command ls in my workspace.`
- `Execute echo Hello from Claude.`

You should see the output directly from your terminal server 🎉

---

## Wrapping Up

Congrats! You’ve built a working MCP server that executes terminal commands — and you can run it with or without Docker.

Want to go further?
- Add security checks to block dangerous commands
- Let Claude write to or read from files
- Connect to cloud or remote systems

👉 Let us know in the YouTube comments what you'd like to build next!

Don’t forget to **like, subscribe, and share** to support more videos like this. See you next time 🚀


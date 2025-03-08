# MCP Server for Executing Terminal Commands

## Introduction

Hey everyone! Welcome back to **The AI Language**. Today, we’re building an **MCP server that can execute terminal commands**. This means you can ask **Claude for Desktop** to run commands on your computer and send back the output, just like using a terminal but through AI.

[![Tutorial video](https://img.youtube.com/vi/_veLqeCzdIQ/maxresdefault.jpg)](https://youtu.be/_veLqeCzdIQ)

Before we begin, if you enjoy learning about AI, coding, and automation, please **like this video and subscribe** to the channel. It really helps us bring more tutorials your way! Now, let’s get started!

---

## What is MCP?

**MCP (Model Context Protocol)** is a system that lets AI interact with external tools and fetch information. MCP servers can do three things:

- **Store data** (like files or API responses)
- **Run tools** (functions that AI can execute)
- **Use prompts** (predefined templates for tasks)

Today, we’re building a tool that takes a command, runs it in the terminal, and sends back the output.

---

## Installing Claude for Desktop

First, install **Claude for Desktop** from [Claude’s website](https://claude.ai). It allows us to test MCP integrations easily.

- **Mac:** Drag the app to Applications.
- **Windows:** Follow the installer steps.

Once installed, open it and log in.

---

## Setting Up Python and the Right Tools

We need **Python 3.10 or higher** and a tool called **uv** to manage our project. **uv** is a fast package manager for Python that helps us install and run dependencies.

To install python - https://www.python.org/downloads/
Video link - https://www.youtube.com/watch?v=jmK0qwXBTcE

### Step 1: Install `uv`

#### Mac/Linux:
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```
For fixing permission issues if they occurr
```sh
sudo chown -R $(whoami):staff ~/.local  
```

#### Windows:
Follow the instructions at [uv’s installation page](https://astral.sh/uv/).

Restart your terminal after installation so `uv` is recognized.

### Step 2: Create the MCP Directory Structure

We’ll store our MCP servers inside a structured directory:
```sh
mkdir -p ~/mcp/servers/terminal_server
mkdir -p ~/mcp/workspace
cd ~/mcp/servers/terminal_server
```

- `mcp/servers/` stores all MCP servers.
- `mcp/workspace/` is a dedicated workspace directory.

### Step 3: Set Up a Python Project
```sh
uv init
```
This initializes our Python project inside `terminal_server`.

### Step 4: Set Up a Virtual Environment
```sh
uv venv
source .venv/bin/activate  # Mac/Linux
# or
.venv\Scripts\activate     # Windows
```
This creates a virtual environment, which keeps our project’s dependencies separate from the system’s Python installation.

### Step 5: Install Required Packages
```sh
uv add "mcp[cli]"
```
This installs the MCP package, which allows our server to communicate with Claude.

---

## Building the MCP Server That Executes Terminal Commands

### Step 1: Create the Server File
```sh
touch terminal_server.py
```

### Step 2: Import the Necessary Code
```python
import os
import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("terminal")
DEFAULT_WORKSPACE = os.path.expanduser("~/mcp/workspace")
```
We import the required libraries. `subprocess` lets us run terminal commands, and `FastMCP` helps us set up an MCP server. The workspace directory is always set to `~/mcp/workspace/`.

### Step 3: Define the Function to Run Commands
```python
@mcp.tool()
def run_command(command: str) -> str:
    """
    Run a terminal command inside the workspace directory.
    
    Args:
        command: The shell command to run.
    
    Returns:
        The command output or an error message.
    """
    try:
        result = subprocess.run(command, shell=True, cwd=DEFAULT_WORKSPACE, capture_output=True, text=True)
        return result.stdout or result.stderr
    except Exception as e:
        return str(e)
```
This function takes a command, runs it inside `~/mcp/workspace/`, and returns the output.

### Step 4: Start the Server
```python
if __name__ == "__main__":
    mcp.run(transport='stdio')
```
This starts the MCP server, allowing Claude to communicate with it.

Run this command to start your server:
```sh
uv run terminal_server.py
```
This runs our Python script inside the virtual environment using `uv`.

---

## Connecting to Claude for Desktop

Now, let’s tell **Claude** how to use our server. Open this file:
```sh
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Add this code inside the file (replace username with your username):
```json
{
    "mcpServers": {
        "terminal": {
            "command": "/Users/<username>/.local/bin/uv",
            "args": [
                "--directory", "/Users/<username>/mcp/servers/terminal_server",
                "run", 
                "terminal_server.py"
            ]
        }
    }
}
```

Save the file and restart **Claude for Desktop**. You should see a hammer icon, which means your tool is ready.

---

## Testing the MCP Server

Let’s test it out! In **Claude**, ask:

- `Run the command ls in my workspace.`
- `Execute echo Hello World.`

Claude will send the command to our server, which will execute it and return the response.

---

## Wrapping Up

And that’s it! We built an **MCP server** that can execute terminal commands and connected it to Claude. Now, it can run real commands on your machine!

Want to improve it? Try adding:

- **Security filters** to prevent unsafe commands.
- **More features**, like reading and writing files.
- **Cloud integration** to run commands remotely.

Let me know in the comments what you’d like to build next! Don’t forget to **like, subscribe, and share** for more tutorials. See you next time! 🚀


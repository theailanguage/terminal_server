# MCP SSE Server and STDIO Server Examples

## Introduction

Welcome to **The AI Language** project! In this repository, you'll find multiple examples of setting up MCP Servers. MCP (Model Context Protocol) is a framework for AI models that enables them to store data, run tools, and use prompts for specific tasks.

### Available Server Examples
We provide four examples to help you set up your MCP server in different environments. The table below summarizes each configuration:

| Example | Server Type | Transport Method | Environment | Docker | Tutorial Link |
|---------|-------------|------------------|-------------|--------|---------------|
| 1 | **Terminal Server (STDIO)** | STDIO | Local | No | [Tutorial 1](https://youtu.be/_veLqeCzdIQ) |
| 2 | **Terminal Server (STDIO)** | STDIO | Local | Yes | [Tutorial 2](https://youtu.be/cgml6yzrOjc) |
| 3 | **Terminal Server (SSE)** | SSE | Local | Yes | [Tutorial 3](https://youtu.be/s0YJNcT1XMA) |
| 4 | **Terminal Server (SSE)** | SSE | Google Cloud Platform (Web) | Yes | [Tutorial 3](https://youtu.be/s0YJNcT1XMA) |

If you enjoy learning about AI, coding, and automation, please **like and subscribe** to the channel — it really helps us make more great content for you!  
[SUBSCRIBE](https://youtube.com/@theailanguage?sub_confirmation=1)

## What is MCP?

**MCP (Model Context Protocol)** is a protocol that allows AI models to:
- **Store data** (like files or API responses)
- **Run tools** (functions that AI can execute)
- **Use prompts** (predefined templates for tasks)

---

## Option 1: Setup Without Docker (Local Python)

This option demonstrates how to set up an MCP server locally using Python without Docker. Follow the video tutorial: [Tutorial 1](https://youtu.be/_veLqeCzdIQ)

---

## Option 2: Setup With Docker

This option shows how to containerize the MCP server with Docker and run it locally. Follow the video tutorial: [Tutorial 2](https://youtu.be/cgml6yzrOjc)

---

## Option 3: Setup with SSE (Local, Docker)

This option demonstrates how to run an MCP server over SSE using Docker in a local environment. Follow the video tutorial: [Tutorial 3](https://youtu.be/s0YJNcT1XMA)

---

## Option 4: Setup with SSE on Google Cloud Platform

This option details how to deploy the SSE server to Google Cloud Platform using Docker. Follow the video tutorial: [Tutorial 3](https://youtu.be/s0YJNcT1XMA)

---

## Testing the MCP Server

Once the server is running, you can test it by using prompts in Claude, such as:

- `Run the command ls in my workspace.`
- `Execute echo Hello from Claude.`

You should see the output directly from your terminal server 🎉

---

## Wrapping Up

Congrats! You've successfully built an MCP server that can execute terminal commands. You can run it locally or in Docker, depending on your preference.

### Next Steps:
- Add security checks to block potentially dangerous commands.
- Allow Claude to read and write files.
- Connect the server to cloud systems or remote environments.

For any issues or improvements, feel free to contribute and open an issue or pull request in this repository!

## 🤝 Contributing

At this time, this project does **not accept external code contributions**.

This is to keep licensing simple and avoid any shared copyright.

You're very welcome to:
✅ Report bugs or request features (via GitHub Issues)  
✅ Fork the repo and build your own version  
✅ Suggest documentation improvements

If you'd like to collaborate in another way, feel free to open a discussion!
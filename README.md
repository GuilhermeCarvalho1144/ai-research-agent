# AI Research Agent

A lightweight CLI research assistant built with **LangGraph**, **LangChain**, **Ollama**, and **Firecrawl MCP**.

It runs a local chat model through Ollama, connects to Firecrawl's MCP server over stdio, loads the available MCP tools, and lets you interactively ask research-oriented questions from the terminal.

## Features

- Local LLM inference with **Ollama**
- Tool-enabled agent built with **LangGraph**
- **Firecrawl MCP** integration for:
  - website scraping
  - crawling pages
  - extracting information from the web
- Interactive terminal chat loop
- Conversation memory within the running session
- Environment-based configuration with `.env`

## Project Structure

```text
.
├── main.py
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
└── README.md

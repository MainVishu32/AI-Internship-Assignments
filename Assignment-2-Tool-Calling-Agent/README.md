# AI Tool Calling Agent

An AI agent built using Python, LangChain, and Google Gemini.

The agent can understand a user's request, select an appropriate tool, execute the tool, and return the result to the user.

## Features

- Google Gemini LLM
- LangChain tool calling
- Calculator tool
- Timezone-based time tool
- Automatic tool selection
- Interactive command-line interface
- Graceful error handling
- Safe mathematical expression evaluation
- Environment-variable based API configuration

## Tools

### 1. Calculator

Performs basic mathematical calculations such as:

- Addition
- Subtraction
- Multiplication
- Division
- Modulo
- Powers

Example:

```text
User: What is 125 * 48?

Agent selects: calculator

Tool result: 6000
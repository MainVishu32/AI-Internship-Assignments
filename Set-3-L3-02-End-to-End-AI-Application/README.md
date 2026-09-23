# AI Study Assistant

An AI-powered web application that helps students understand technical and academic topics using Google Gemini, LangChain, FastAPI, and a simple web interface.

## Features

- AI-powered study assistance
- Natural language question answering
- Conversation memory for follow-up questions
- System prompt for consistent study-focused responses
- LangChain-based LLM integration
- Google Gemini as the LLM provider
- FastAPI REST API backend
- Interactive web interface
- API documentation through Swagger UI
- Input validation and error handling
- Environment-variable based API key configuration

---

## Architecture

```mermaid
flowchart TD
    A[Student / Browser] --> B[Web UI - HTML CSS JavaScript]
    B --> C[FastAPI REST API]
    C --> D[Input Validation]
    D --> E[LangChain AI Service]
    E --> F[Conversation History]
    E --> G[System Prompt]
    G --> H[Google Gemini LLM]
    F --> H
    H --> E
    E --> C
    C --> B
    B --> A
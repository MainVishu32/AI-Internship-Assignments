import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise EnvironmentError(
        "GOOGLE_API_KEY is not configured in the .env file."
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key,
    temperature=0.3,
)


SYSTEM_PROMPT = """
You are an AI Study Assistant.

Help students understand technical and academic topics
in a simple and structured way.

When appropriate:
- Explain concepts clearly.
- Use examples.
- Use bullet points.
- Keep answers focused and easy to understand.

Use the previous conversation to understand follow-up questions.
"""


conversation_history = []


def ask_ai(question: str) -> str:
    """Send a question to Gemini while remembering the conversation."""

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]

    messages.extend(conversation_history)

    messages.append(
        HumanMessage(content=question)
    )

    response = llm.invoke(messages)

    answer = response.text

    conversation_history.append(
        HumanMessage(content=question)
    )

    conversation_history.append(
        AIMessage(content=answer)
    )

    return answer
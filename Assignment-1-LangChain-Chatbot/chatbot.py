import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise EnvironmentError(
        "GOOGLE_API_KEY is not configured. "
        "Please add it to the .env file."
    )

# Create Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key,
    temperature=0.7
)

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful AI assistant. "
        "Answer questions clearly, accurately, and concisely."
    ),
    MessagesPlaceholder(variable_name="history"),
    (
        "human",
        "{input}"
    )
])

# Create LangChain chain
chain = prompt | llm

# Store conversation history
store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]


# Add conversation memory
chatbot = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)


print("===================================")
print("      AI Chatbot - LangChain")
print("===================================")
print("Type 'exit' to stop the chatbot.")
print()

while True:
    user_input = input("You: ")

    if user_input.strip().lower() in {"exit", "quit"}:
        print("AI: Goodbye!")
        break

    try:
        response = chatbot.invoke(
            {"input": user_input},
            config={
                "configurable": {
                    "session_id": "demo"
                }
            }
        )

        print("AI:", response.text)
        print()

    except Exception as e:
        print("AI: Sorry, something went wrong.")
        print("Error:", e)
        print()
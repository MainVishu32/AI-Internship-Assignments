import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import calculator, get_time


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise EnvironmentError(
        "GOOGLE_API_KEY is not configured in the .env file."
    )


# Create the Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key,
    temperature=0
)


# Register our tools
tools = [
    calculator,
    get_time,
]

tool_map = {
    "calculator": calculator,
    "get_time": get_time,
}


# Give Gemini access to the tools
llm_with_tools = llm.bind_tools(tools)


def run_agent(user_input):
    """
    Run the AI agent and execute any tools selected by Gemini.
    """

    messages = [
        ("user", user_input)
    ]

    while True:

        # Ask Gemini what to do
        response = llm_with_tools.invoke(messages)

        # Add Gemini's response to conversation
        messages.append(response)

        # If Gemini did not request a tool, return its answer
        if not response.tool_calls:
            return response.text

        # Execute requested tools
        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            print(f"\n[Agent selected tool: {tool_name}]")
            print(f"[Arguments: {tool_args}]")

            if tool_name not in tool_map:
                tool_result = "Unknown tool requested."

            else:
                try:
                    tool_result = tool_map[tool_name].invoke(tool_args)

                except Exception as error:
                    tool_result = f"Tool execution failed: {error}"

            print(f"[Tool result: {tool_result}]")

            # Give the tool result back to Gemini
            messages.append(
                {
                    "role": "tool",
                    "content": str(tool_result),
                    "tool_call_id": tool_call["id"],
                }
            )


if __name__ == "__main__":

    print("AI Tool Calling Agent")
    print("Type 'exit' to stop.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            print("Agent: Goodbye!")
            break

        if not question.strip():
            print("Agent: Please enter a question.")
            continue

        try:
            answer = run_agent(question)
            print("\nAgent:", answer)

        except Exception as error:
            print(f"\nAgent: Sorry, something went wrong: {error}")

        print()
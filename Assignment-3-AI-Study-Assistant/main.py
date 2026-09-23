from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ai_service import ask_ai


app = FastAPI(
    title="AI Study Assistant",
    description="AI-powered study assistant using FastAPI, LangChain and Gemini.",
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "AI Study Assistant is running."
    }


@app.post("/api/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    if len(question) > 2000:
        raise HTTPException(
            status_code=400,
            detail="Question is too long. Please keep it under 2000 characters."
        )

    try:
        answer = ask_ai(question)

        return AnswerResponse(
            answer=answer
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail=(
                "The AI service is temporarily unavailable. "
                "Please try again later."
            )
        )


app.mount(
    "/",
    StaticFiles(
        directory="static",
        html=True
    ),
    name="static",
)
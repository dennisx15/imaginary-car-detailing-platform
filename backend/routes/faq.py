from fastapi import APIRouter

router = APIRouter()

@router.get("/faq")
def faq():
    return {
        "question": "Do you offer pet hair removal services?",
        "answer": "Yes"
    }
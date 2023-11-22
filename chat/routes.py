from fastapi import APIRouter, Depends, status, Form
from fastapi.responses import JSONResponse
from core.security import oauth2_scheme
from chat.schemas import ChatRequest
from chat.inf import run

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)

@router.post('', status_code=status.HTTP_201_CREATED)
async def chat_respond(data: ChatRequest):
    """
    Respond to a chat request.

    Args:
        data (ChatRequest): The chat request data.

    Returns:
        JSONResponse: The JSON response containing the chat response.
    """
    response = run(data.query)
    print(response)
    return JSONResponse(content=response)

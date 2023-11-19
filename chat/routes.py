from fastapi import APIRouter, Depends, status, Form
from core.security import oauth2_scheme
from fastapi.responses import JSONResponse
from chat.schemas import ChatRequest
from chat.inf import run


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)

@router.post('', status_code=status.HTTP_201_CREATED)
async def chat_respond(data: ChatRequest) :
    response = run(data.query)
    print(response)
    return JSONResponse(content=response)
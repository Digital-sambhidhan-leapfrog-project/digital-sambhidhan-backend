from pydantic import BaseModel, Field
from typing import Union 


class ChatScheme(BaseModel):
    
    class Config:
        form_attributes = True
        arbitrary_types_allowed = True

class ChatRequest(ChatScheme):
    query: str = Field(..., title="Query", description="Message to be sent to the chatbot")
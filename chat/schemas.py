from pydantic import BaseModel, Field

class ChatScheme(BaseModel):
    """
    Base class for chat-related Pydantic models.
    """
    class Config:
        form_attributes = True
        arbitrary_types_allowed = True

class ChatRequest(ChatScheme):
    """
    Pydantic model for a chat request.

    Attributes:
        query (str): The message to be sent to the chatbot.
    """
    query: str = Field(..., title="Query", description="Message to be sent to the chatbot")

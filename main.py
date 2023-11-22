import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from sqlalchemy.exc import OperationalError
from colorama import Fore, Style

from core.database import engine
from core.security import JWTAuth
from users import models
from users.routes import router as guest_router, user_router
from chat.routes import router as chat_router
from chat.inf import init as chat_init
from auth.routes import router as auth_router

# Color Codes
class ColorCode:
    """
    Color codes for printing colored text in the console.
    """
    RED = Fore.RED
    GREEN = Fore.GREEN
    BLUE = Fore.BLUE
    YELLOW = Fore.YELLOW
    RESET = Style.RESET_ALL


app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include Routers
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(chat_router)



# Database Initialization Retry
while True:
    try:
        models.Base.metadata.create_all(bind=engine)
        print(ColorCode.GREEN + "Database Connected!")
        break
    except OperationalError:
        print(ColorCode.RED + "Connection failed. Retrying...")
        time.sleep(1)

# Add Middleware for JWT Authentication
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

# Initialize Chat
print(ColorCode.YELLOW + "----Initializing Chat Model...----")
print(ColorCode.YELLOW + "Please wait until the initialization is complete. This may take some time.")
chat_init()
print(ColorCode.GREEN + "----Chat Model Initialized!----")

# Testing Route
@app.get("/")
async def hello_world(text: str = "I am online!"):
    """
    Simple test route to check if the application is online.

    Args:
        text (str): Custom text to include in the response.

    Returns:
        JSONResponse: Response containing a message.
    """
    return JSONResponse(content={"message": text})

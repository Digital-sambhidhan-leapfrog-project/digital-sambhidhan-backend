from fastapi import FastAPI
from fastapi.responses import JSONResponse
from users.routes import router as guest_router, user_router
from chat.routes import router as chat_router
from chat.inf import init as chat_init
from auth.routes import router as auth_router
from core.security import JWTAuth, oauth2_scheme
from starlette.middleware.authentication import AuthenticationMiddleware
from users import models
from core.database import engine
from fastapi import Depends
import time
from sqlalchemy.exc import OperationalError

app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(chat_router)

while True:
    try:
        models.Base.metadata.create_all(bind=engine)
        break
    except OperationalError:
        print("Connection failed. Retrying...")
        time.sleep(1)

# Add Middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

chat_init()


@app.get("/")
async def hello_world(text: str = "Hello World"):
    return JSONResponse(content={"message": text})
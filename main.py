from fastapi import FastAPI
from fastapi.responses import JSONResponse
from users.routes import router as guest_router, user_router
from auth.routes import router as auth_router
from core.security import JWTAuth, oauth2_scheme
from starlette.middleware.authentication import AuthenticationMiddleware
from users import models
from core.database import engine
from fastapi import Depends

app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)

models.Base.metadata.create_all(bind=engine)

# Add Middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())


@app.get("/")
async def hello_world(text: str = "Hello World"):
    return JSONResponse(content={"message": text})
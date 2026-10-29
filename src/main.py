from fastapi import FastAPI

from src.routers import user

app = FastAPI(title="CI/CD lab app")
app.include_router(user.router)

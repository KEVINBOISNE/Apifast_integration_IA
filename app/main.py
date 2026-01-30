from fastapi import FastAPI
from app.routers import ai, validators

app = FastAPI(title="FastAPI File Upload Service")

app.include_router(ai.router)
app.include_router(validators.router)

@app.get("/ping")
async def root():
    return {"ping": "pong"}

@app.get("/Core")
async def root():
    return {"Core": "Core connection are validated"}
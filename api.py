from fastapi import FastAPI
from pydantic import BaseModel
from core.llama_response import analyze_chunk
import asyncio

app = FastAPI()

class AnalyzeRequest(BaseModel):
    message: str
    history: list[str]

@app.post("/analyze-message")
async def analyze_message(request: AnalyzeRequest):
    result = await analyze_chunk(request.message, request.history)
    return result

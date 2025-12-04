import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from llama_cpp import Llama

MODEL_PATH = r"D:\DevTools\AI\models\llama3-8b-instruct.Q4_K_M.gguf"

llm = Llama(model_path=MODEL_PATH, n_ctx=4096, n_threads=6)

app = FastAPI(title="Local AI API")

class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 200

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    out = llm(req.prompt, max_tokens=req.max_tokens, stop=["User:", "You:", "\n\n"])
    reply = out["choices"][0]["text"].strip()
    return ChatResponse(reply=reply)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from src.chain import conv_chain

app = FastAPI(title="Hackathon RAG-Chat practica usando reto1 🐱")



class ChatReq(BaseModel):
    message: str

class ChatRes(BaseModel):
    answer: str
    sources: List[str] = []  

@app.post("/chat", response_model=ChatRes)
def chat(req: ChatReq):
    # Ejecuta el chain
    result = conv_chain({"question": req.message})
    answer = result["answer"]
    # extrae las fuentes si es que hay extraccion de los pdfs
    sources = [doc.metadata.get("source","") for doc in result.get("source_documents",[])]
    return ChatRes(answer=answer, sources=sources)
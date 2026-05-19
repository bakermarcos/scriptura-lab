from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import chat, health, sources

app = FastAPI(
    title="Scriptura Lab API",
    version="0.2.0",
    description="Local-first Bible study assistant backend powered by RAG and configurable model providers.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(sources.router)
app.include_router(chat.router)

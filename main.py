from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.endpoints.chat import router as chat_router
from api.v1.endpoints.health import router as health_router
from auth.routes import router as auth_router

app = FastAPI(title="Unentropia API", version="0.0.1")


app.include_router(health_router, prefix="/api/v1/health", tags=["health"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(auth_router, prefix="/auth/google", tags=["auth"])

origins = ["https://unentropia-ui.vercel.app", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

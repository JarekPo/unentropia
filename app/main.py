import uvicorn
from api.v1.endpoints.chat import router as chat_router
from api.v1.endpoints.health import router as health_router
from auth.routes import router as auth_router
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from jose import exceptions

app = FastAPI(title="Unentropia API", version="0.0.1")


app.include_router(health_router, prefix="/api/v1/health", tags=["health"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(auth_router, prefix="/auth/google", tags=["auth"])

origins = ["http://localhost:3000", "*"]  # Allow all origins for development; adjust in production

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.exception_handler(exceptions.ExpiredSignatureError)
async def expired_token_handler(request: Request, exc: exceptions.ExpiredSignatureError):
    print("Token expired:", exc)
    print("Request URL:", request.url)
    print("Request:", request)
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Token has expired. Please log in again."},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

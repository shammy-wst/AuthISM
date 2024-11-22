from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat
from config.settings import settings

app = FastAPI(title="AuthISM API")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(chat.router, prefix=settings.API_V1_STR + "/chat", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API AuthISM"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
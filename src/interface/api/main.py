from fastapi import FastAPI
from src.interface.api.v1.endpoints import auth, consoles


app = FastAPI(
    title="Gamer API",
    description="API para gerenciamento de jogos - Desafio Backend",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(consoles.router, prefix="/consoles", tags=["Consoles"])

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Service is running"}
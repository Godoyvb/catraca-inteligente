from fastapi import FastAPI

app = FastAPI(
    title="Catraca Inteligente",
    description="API para projeto acadêmico",
    version="1.0.0"
)

@app.get("/")
def inicio():
    return {
        "mensagem": "Servidor da Catraca Inteligente funcionando!"
    }

@app.get("/status")
def status():
    return {
        "status": "online"
    }

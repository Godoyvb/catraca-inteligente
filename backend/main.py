from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone

from backend.rabbitmq import enviar_evento

app = FastAPI(
    title="Catraca Inteligente",
    description="API acadêmica de demonstração",
    version="1.0.0"
)


class EventoAcesso(BaseModel):
    identificador_demo: str
    autorizado: bool


@app.get("/")
def inicio():
    return {
        "mensagem": "Catraca Inteligente funcionando!"
    }


@app.get("/status")
def status():
    return {
        "status": "online",
        "rabbitmq": "integrado"
    }


@app.post("/acesso")
def registrar_acesso(evento: EventoAcesso):
    mensagem = {
        "identificador_demo": evento.identificador_demo,
        "autorizado": evento.autorizado,
        "data_hora": datetime.now(timezone.utc).isoformat()
    }

    try:
        enviar_evento(mensagem)

        return {
            "mensagem": "Evento enviado ao RabbitMQ!",
            "evento": mensagem
        }

    except Exception as erro:
        raise HTTPException(
            status_code=503,
            detail=f"Erro ao enviar evento: {str(erro)}"
        )

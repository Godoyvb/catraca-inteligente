
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timezone

from backend.rabbitmq import enviar_evento
from database.database import criar_tabela, salvar_evento, listar_eventos
from backend.arduino import conectar_arduino

app = FastAPI(
    title="Catraca Inteligente",
    description="API acadêmica de demonstração",
    version="1.0.0"
)

criar_tabela()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"]
)


class EventoAcesso(BaseModel):
    identificador_demo: str
    autorizado: bool


@app.get("/")
def inicio():
    return {"mensagem": "Catraca Inteligente funcionando!"}


@app.get("/status")
def status():
    return {
        "status": "online",
        "rabbitmq": "integrado",
        "database": "integrado"
    }


@app.get("/arduino/status")
def status_arduino():
    conectado = conectar_arduino()

    return {
        "arduino": "conectado" if conectado else "desconectado",
        "porta": "/dev/ttyACM0"
    }


@app.post("/acesso")
def registrar_acesso(evento: EventoAcesso):
    mensagem = {
        "identificador_demo": evento.identificador_demo,
        "autorizado": evento.autorizado,
        "data_hora": datetime.now(timezone.utc).isoformat()
    }

    try:
        salvar_evento(mensagem)
        enviar_evento(mensagem)

        return {
            "mensagem": "Evento registrado com sucesso!",
            "evento": mensagem,
            "catraca": (
                "abertura_simulada"
                if evento.autorizado
                else "acesso_negado_sem_movimento"
            )
        }

    except Exception as erro:
        raise HTTPException(
            status_code=503,
            detail=f"Erro ao registrar evento: {str(erro)}"
        )


@app.get("/eventos")
def consultar_eventos():
    try:
        eventos = listar_eventos()

        return {
            "total": len(eventos),
            "eventos": eventos
        }

    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao consultar eventos: {str(erro)}"
        )

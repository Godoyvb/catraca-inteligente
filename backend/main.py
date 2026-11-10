
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timezone
from pathlib import Path
import subprocess

from backend.rabbitmq import enviar_evento
from database.database import criar_tabela, salvar_evento, listar_eventos
from backend.arduino import testar_comunicacao

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
    comunicacao = testar_comunicacao()

    return {
        "arduino": "conectado" if comunicacao else "desconectado",
        "comunicacao": "ok" if comunicacao else "falha",
        "porta": "/dev/ttyACM0"
    }

@app.post("/camera/capturar")
def capturar_foto():
    pasta = Path(__file__).resolve().parent.parent / "frontend" / "capturas"
    pasta.mkdir(parents=True, exist_ok=True)

    nome_arquivo = datetime.now().strftime("captura_%Y%m%d_%H%M%S.jpg")
    caminho = pasta / nome_arquivo

    try:
        resultado = subprocess.run(
            [
                "rpicam-still",
                "-n",
                "-t", "2000",
                "--width", "1280",
                "--height", "720",
                "-o", str(caminho)
            ],
            capture_output=True,
            text=True,
            timeout=20
        )

        if resultado.returncode != 0 or not caminho.exists():
            raise RuntimeError(resultado.stderr[-1000:])

        return {
            "mensagem": "Foto capturada com sucesso!",
            "arquivo": nome_arquivo,
            "url": f"/camera/foto/{nome_arquivo}"
        }

    except Exception as erro:
        if caminho.exists():
            caminho.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao capturar foto: {str(erro)}"
        )


@app.get("/camera/foto/{nome_arquivo}")
def visualizar_foto(nome_arquivo: str):
    from fastapi.responses import FileResponse

    if (
        not nome_arquivo.startswith("captura_")
        or not nome_arquivo.endswith(".jpg")
        or Path(nome_arquivo).name != nome_arquivo
    ):
        raise HTTPException(status_code=400, detail="Nome de arquivo inválido")

    caminho = (
        Path(__file__).resolve().parent.parent
        / "frontend" / "capturas" / nome_arquivo
    )

    if not caminho.is_file():
        raise HTTPException(status_code=404, detail="Foto não encontrada")

    return FileResponse(caminho, media_type="image/jpeg")


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

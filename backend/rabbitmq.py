import os
import json
import pika

from dotenv import load_dotenv

load_dotenv()


def enviar_evento(evento):
    usuario = os.getenv("RABBIT_USER", "catraca")
    senha = os.getenv("RABBIT_PASSWORD")

    if not senha:
        raise RuntimeError("RABBIT_PASSWORD não configurada no .env")

    credenciais = pika.PlainCredentials(usuario, senha)

    parametros = pika.ConnectionParameters(
        host="localhost",
        port=5672,
        credentials=credenciais,
        heartbeat=30,
        blocked_connection_timeout=10
    )

    conexao = pika.BlockingConnection(parametros)

    try:
        canal = conexao.channel()

        canal.queue_declare(
            queue="eventos_acesso",
            durable=True
        )

        canal.confirm_delivery()

        mensagem = json.dumps(evento, ensure_ascii=False)

        canal.basic_publish(
            exchange="",
            routing_key="eventos_acesso",
            body=mensagem,
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type="application/json"
            ),
            mandatory=True
        )

        return True

    finally:
        conexao.close()

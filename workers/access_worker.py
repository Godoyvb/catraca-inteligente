
import os
import json
import pika
from dotenv import load_dotenv

load_dotenv()

usuario = os.getenv("RABBIT_USER", "catraca")
senha = os.getenv("RABBIT_PASSWORD")

if not senha:
    raise RuntimeError("RABBIT_PASSWORD não configurada no .env")

credenciais = pika.PlainCredentials(usuario, senha)

parametros = pika.ConnectionParameters(
    host="localhost",
    port=5672,
    credentials=credenciais,
    heartbeat=30
)

conexao = pika.BlockingConnection(parametros)
canal = conexao.channel()

canal.queue_declare(
    queue="eventos_acesso",
    durable=True
)

print("Worker aguardando eventos...", flush=True)


def processar_evento(ch, metodo, propriedades, corpo):
    try:
        evento = json.loads(corpo.decode("utf-8"))

        print("\nEvento recebido:")
        print(json.dumps(evento, indent=2, ensure_ascii=False))

        resultado = "APROVADO" if evento.get("autorizado") else "NEGADO"
        print("RESULTADO DA DEMONSTRAÇÃO:", resultado)

        ch.basic_ack(delivery_tag=metodo.delivery_tag)

    except Exception as erro:
        print("Erro ao processar evento:", erro)
        ch.basic_nack(
            delivery_tag=metodo.delivery_tag,
            requeue=False
        )


canal.basic_qos(prefetch_count=1)

canal.basic_consume(
    queue="eventos_acesso",
    on_message_callback=processar_evento
)

canal.start_consuming()

import os
import json
import pika
from dotenv import load_dotenv

load_dotenv()

USUARIO = os.getenv("RABBIT_USER", "catraca")
SENHA = os.getenv("RABBIT_PASSWORD")

if not SENHA:
    raise RuntimeError("RABBIT_PASSWORD não configurada no .env")

credenciais = pika.PlainCredentials(USUARIO, SENHA)

parametros = pika.ConnectionParameters(
    host="localhost",
    port=5672,
    credentials=credenciais,
    heartbeat=30
)

def processar_mensagem(canal, metodo, propriedades, corpo):
    try:
        evento = json.loads(corpo.decode("utf-8"))

        print("\n========== NOVO EVENTO ==========")
        print("Identificador:", evento.get("identificador_demo"))
        print("Autorizado:", evento.get("autorizado"))
        print("Data e hora:", evento.get("data_hora"))
        print("Resultado: EVENTO PROCESSADO")
        print("=================================\n")

        canal.basic_ack(delivery_tag=metodo.delivery_tag)

    except Exception as erro:
        print("Erro ao processar evento:", erro)
        canal.basic_nack(
            delivery_tag=metodo.delivery_tag,
            requeue=False
        )

def iniciar_worker():
    conexao = pika.BlockingConnection(parametros)
    canal = conexao.channel()

    canal.queue_declare(
        queue="eventos_acesso",
        durable=True
    )

    canal.basic_qos(prefetch_count=1)

    canal.basic_consume(
        queue="eventos_acesso",
        on_message_callback=processar_mensagem
    )

    print("WORKER DA CATRACA INICIADO!")
    print("Aguardando eventos do RabbitMQ...\n")

    try:
        canal.start_consuming()
    except KeyboardInterrupt:
        print("\nWorker encerrado.")
        canal.stop_consuming()
    finally:
        conexao.close()

if __name__ == "__main__":
    iniciar_worker()

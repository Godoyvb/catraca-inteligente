import os
import time

import serial

PORTA = os.getenv("ARDUINO_PORTA", "/dev/ttyACM0")
BAUD = 9600

conexao = None


def conectar_arduino():
    """Abre a conexão serial se ainda não estiver aberta."""
    global conexao

    if conexao is not None and conexao.is_open:
        return True

    try:
        conexao = serial.Serial(PORTA, BAUD, timeout=2)
        time.sleep(2)  # o Arduino reinicia ao abrir a serial
        conexao.reset_input_buffer()
        return True
    except serial.SerialException as erro:
        print(f"Erro ao conectar no Arduino: {erro}")
        conexao = None
        return False


def enviar_comando(comando):
    if not conectar_arduino():
        return False

    try:
        conexao.reset_input_buffer()  # descarta linhas antigas
        conexao.write(f"{comando}\n".encode("utf-8"))
        resposta = conexao.readline().decode(
            "utf-8", errors="replace"
        ).strip()

        print("Resposta do Arduino:", resposta)
        return resposta.startswith("CONFIRMADO")

    except serial.SerialException as erro:
        print(f"Erro na comunicação: {erro}")
        return False


def testar_comunicacao():
    if not conectar_arduino():
        return False

    try:
        conexao.reset_input_buffer()
        conexao.write(b"PING\n")
        resposta = conexao.readline().decode(
            "utf-8", errors="replace"
        ).strip()
        return resposta == "PONG"
    except serial.SerialException as erro:
        print(f"Erro na comunicação: {erro}")
        return False


def liberar_catraca():
    return enviar_comando("AUTORIZADO")


def bloquear_catraca():
    return enviar_comando("NEGADO")

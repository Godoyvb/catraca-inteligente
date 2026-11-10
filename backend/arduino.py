import serial
import time

PORTA_ARDUINO = "/dev/ttyACM0"
VELOCIDADE = 9600

conexao = None


def conectar_arduino():
    global conexao

    try:
        if conexao is None or not conexao.is_open:
            conexao = serial.Serial(
                PORTA_ARDUINO,
                VELOCIDADE,
                timeout=2
            )
            time.sleep(2)
            conexao.reset_input_buffer()

        return True

    except serial.SerialException as erro:
        print(f"Arduino indisponível: {erro}")
        return False


def testar_comunicacao():
    if not conectar_arduino():
        return False

    try:
        conexao.write(b"PING\n")
        resposta = conexao.readline().decode(
            "utf-8", errors="replace"
        ).strip()

        print("Resposta do Arduino:", resposta)

        return resposta == "PONG"

    except serial.SerialException as erro:
        print(f"Erro na comunicação: {erro}")
        return False

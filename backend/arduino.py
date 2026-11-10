
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
            return True

        return True

    except serial.SerialException as erro:
        print(f"Arduino indisponível: {erro}")
        return False


def enviar_comando(comando: str):
    if comando not in ("ABRIR", "FECHAR"):
        raise ValueError("Comando inválido")

    if not conectar_arduino():
        raise ConnectionError("Não foi possível conectar ao Arduino")

    conexao.write((comando + "\n").encode("utf-8"))

    return {
        "mensagem": "Comando enviado ao Arduino",
        "comando": comando
    }

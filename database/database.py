
import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).parent / "catraca.db"


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela():
    conexao = conectar()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identificador_demo TEXT NOT NULL,
            autorizado BOOLEAN NOT NULL,
            data_hora TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


def salvar_evento(evento):
    conexao = conectar()

    conexao.execute("""
        INSERT INTO eventos (
            identificador_demo,
            autorizado,
            data_hora
        )
        VALUES (?, ?, ?)
    """, (
        evento["identificador_demo"],
        evento["autorizado"],
        evento["data_hora"]
    ))

    conexao.commit()
    conexao.close()


def listar_eventos():
    conexao = conectar()

    eventos = conexao.execute("""
        SELECT * FROM eventos ORDER BY id DESC
    """).fetchall()

    conexao.close()

    return [dict(evento) for evento in eventos]

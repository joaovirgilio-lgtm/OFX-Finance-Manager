"""Persistência em PostgreSQL com deduplicação por identificador OFX."""
import os
import hashlib
import psycopg2


def _identificador(t):
    # FITID é o identificador da transação fornecido pelo banco.
    fitid = str(getattr(t, "id", "") or "").strip()
    if fitid:
        return fitid
    # Alternativa determinística para arquivos que não possuem FITID.
    dados = f"{t.date.isoformat()}|{t.amount}|{t.memo or t.payee or ''}"
    return hashlib.sha256(dados.encode("utf-8")).hexdigest()


def importar(transacoes):
    configuracao = {
        "host": os.getenv("PG_HOST", "localhost"),
        "port": int(os.getenv("PG_PORT", "5432")),
        "dbname": os.getenv("PG_DB", "projeto_ofx_finance"),
        "user": os.getenv("PG_USER", "postgres"),
        "password": os.getenv("PG_PASSWORD", ""),
    }
    inseridas = repetidas = 0
    with psycopg2.connect(**configuracao) as conexao:
        with conexao.cursor() as cursor:
            for t in transacoes:
                descricao = (t.memo or t.payee or "Sem descrição").strip()[:255]
                cursor.execute("""
                    INSERT INTO transacoes (identificador, data, valor, descricao)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (identificador) DO NOTHING
                    RETURNING identificador
                """, (_identificador(t), t.date.date(), t.amount, descricao))
                if cursor.fetchone():
                    inseridas += 1
                else:
                    repetidas += 1
    return inseridas, repetidas

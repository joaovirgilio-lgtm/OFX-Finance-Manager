"""Extração e apresentação das movimentações financeiras."""
from decimal import Decimal
from ofxparse import OfxParser


def carregar(caminho):
    with open(caminho, "rb") as arquivo:
        documento = OfxParser.parse(arquivo)
    return documento.account.statement.transactions


def moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def exibir(transacoes):
    print("\n=== MOVIMENTAÇÕES DO EXTRATO ===")
    for item in transacoes:
        data = item.date.strftime("%d/%m/%Y")
        descricao = (item.memo or item.payee or "Sem descrição").strip()
        print(f"{data} | {moeda(item.amount):>15} | {descricao}")


def resumir(transacoes):
    entradas = sum((t.amount for t in transacoes if t.amount > 0), Decimal("0"))
    saidas = sum((t.amount for t in transacoes if t.amount < 0), Decimal("0"))
    print("\n=== RESUMO FINANCEIRO ===")
    print(f"Movimentações: {len(transacoes)}")
    print(f"Entradas: {moeda(entradas)}")
    print(f"Saídas:   {moeda(saidas)}")
    print(f"Saldo:    {moeda(entradas + saidas)}")

"""Interface de linha de comando para análise e importação OFX."""
import argparse
from pathlib import Path
from finance.extrato import carregar, resumir, exibir
from finance.banco import importar


def main():
    parser = argparse.ArgumentParser(description="Gerenciador de extratos OFX")
    parser.add_argument("arquivo", nargs="?", default="exemplo.ofx")
    parser.add_argument("--importar", action="store_true", help="Gravar no PostgreSQL")
    args = parser.parse_args()
    caminho = Path(args.arquivo)
    if not caminho.is_file():
        parser.error(f"Arquivo não encontrado: {caminho}")
    transacoes = carregar(caminho)
    exibir(transacoes)
    resumir(transacoes)
    if args.importar:
        inseridas, repetidas = importar(transacoes)
        print(f"Banco: {inseridas} inseridas; {repetidas} já existentes.")


if __name__ == "__main__":
    main()

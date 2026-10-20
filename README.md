# OFX Finance Manager

Aplicação de terminal em Python para ler extratos **OFX**, listar movimentações, calcular entradas, saídas e saldo, e opcionalmente gravar dados no **PostgreSQL**. Projeto didático de ETL (extração, transformação e carga).

## Recursos

- Importação de arquivos OFX com `ofxparse`;
- Exibição de data, valor e descrição de cada operação;
- Contagem das movimentações e cálculo dos totais;
- Persistência opcional em PostgreSQL com `psycopg2`;
- Prevenção de duplicatas por identificador da transação (`FITID`), com alternativa determinística quando ausente;
- Consultas de conferência no DBeaver.

## Organização

```text
OFX-Finance-Manager/
├── app.py
├── finance/
│   ├── __init__.py
│   ├── extrato.py
│   └── banco.py
├── exemplo.ofx
├── banco.sql
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Instalação (Windows / CMD)

```cmd
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Leitura e relatório

```cmd
python app.py exemplo.ofx
```

Também é possível passar outro caminho de arquivo OFX ao comando. **Nunca publique extratos bancários reais no GitHub.** O arquivo `exemplo.ofx` contém dados inventados.

## Banco de dados (desafio extra)

1. Crie um banco vazio chamado `projeto_ofx_finance` no PostgreSQL pelo DBeaver.
2. Conecte o editor SQL a **esse banco** e execute `banco.sql`.
3. No terminal **CMD**, configure a conexão (substitua usuário e senha):

```cmd
set "PG_HOST=localhost"
set "PG_PORT=5432"
set "PG_DB=projeto_ofx_finance"
set "PG_USER=postgres"
set /p "PG_PASSWORD=Senha do PostgreSQL: "
python app.py exemplo.ofx --importar
```

> A senha digitada no CMD ficará visível. Evite compartilhar capturas do terminal com a senha. As variáveis valem apenas para a sessão atual.

Execute o comando novamente: o programa deverá contar os registros existentes como repetidos. A restrição `UNIQUE` no banco também impede inserções duplicadas simultâneas.

## Consultas de validação

```sql
SELECT * FROM transacoes ORDER BY data, id;
SELECT COUNT(*) FROM transacoes;
```

## Dados fictícios do exemplo

O arquivo contém 5 transações, com **entradas de R$ 3.250,00**, **saídas de R$ -1.025,50** e **saldo líquido de R$ 2.224,50**.

## Entrega

Crie um repositório público novo no GitHub, por exemplo `OFX-Finance-Manager`, e envie os arquivos. Não inclua `venv/`, credenciais nem extratos reais.

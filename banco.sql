-- Execute no banco projeto_ofx_finance (não no banco postgres).
CREATE TABLE IF NOT EXISTS transacoes (
    id BIGSERIAL PRIMARY KEY,
    identificador VARCHAR(128) NOT NULL UNIQUE,
    data DATE NOT NULL,
    valor NUMERIC(15,2) NOT NULL,
    descricao VARCHAR(255) NOT NULL
);

-- Validação no DBeaver:
SELECT * FROM transacoes ORDER BY data, id;
SELECT COUNT(*) AS quantidade, SUM(CASE WHEN valor > 0 THEN valor ELSE 0 END) AS entradas,
       SUM(CASE WHEN valor < 0 THEN valor ELSE 0 END) AS saidas,
       SUM(valor) AS saldo FROM transacoes;

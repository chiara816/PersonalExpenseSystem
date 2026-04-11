-- 1. PULIZIA PER RESETTARE IL DATABASE
DROP TABLE IF EXISTS budget CASCADE;
DROP TABLE IF EXISTS spese CASCADE;
DROP TABLE IF EXISTS categorie CASCADE;

-- 2. TABELLA CATEGORIE (Modulo 1)
CREATE TABLE categorie (
    id_categoria SERIAL PRIMARY KEY,
    nome_categoria VARCHAR(100) NOT NULL UNIQUE
);

-- 3. TABELLA SPESE (Modulo 2)
-- Include il vincolo CHECK sull'importo come richiesto [cite: 77, 141]
CREATE TABLE spese (
    id_spesa SERIAL PRIMARY KEY,
    data_movimento DATE NOT NULL,
    valore_spesa DECIMAL(10,2) NOT NULL CHECK (valore_spesa > 0),
    nota_opzionale TEXT,
    id_categoria INTEGER NOT NULL REFERENCES categorie(id_categoria)
);

-- 4. TABELLA BUDGET (Modulo 3)
CREATE TABLE budget (
    id_budget SERIAL PRIMARY KEY,
    mese_riferimento VARCHAR(7) NOT NULL, -- Formato YYYY-MM [cite: 87]
    limite_spesa DECIMAL(10,2) NOT NULL CHECK (limite_spesa > 0),
    id_categoria INTEGER NOT NULL REFERENCES categorie(id_categoria),
    CONSTRAINT uq_budget_categoria_mese UNIQUE (mese_riferimento, id_categoria)
);

-- 5. INSERIMENTO CATEGORIE ORIGINALI (Modulo 1)
INSERT INTO categorie (nome_categoria) VALUES ('Alimentari'), ('Trasporti'), ('Svago');

-- 6. INSERIMENTO DATI DI ESEMPIO (Modulo 8.1b)
INSERT INTO budget (mese_riferimento, limite_spesa, id_categoria) VALUES ('2026-04', 300.00, 1);

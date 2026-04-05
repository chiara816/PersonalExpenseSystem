-- =========================================================
-- PROGETTO: SISTEMA GESTIONE SPESE PERSONALI
-- SCRIPT DI CREAZIONE DATABASE (Rif. Punto 8.1a)
-- =========================================================

-- 1. RIMOZIONE TABELLE SE ESISTONO (Reset per ambiente di test)
DROP TABLE IF EXISTS Budget;
DROP TABLE IF EXISTS Spese;
DROP TABLE IF EXISTS Categorie;

-- 2. TABELLA CATEGORIE (Rif. Modulo 1)
-- Obiettivo: Definire le categorie di spesa (es. Alimentari, Trasporti)
CREATE TABLE Categorie (
    id_categoria SERIAL PRIMARY KEY,            -- Chiave Primaria autoincrementale
    nome_categoria VARCHAR(100) NOT NULL UNIQUE -- Vincoli NOT NULL e UNIQUE come richiesto
);

-- 3. TABELLA SPESE (Rif. Modulo 2)
-- Obiettivo: Registrare i movimenti di spesa collegati alle categorie
CREATE TABLE Spese (
    id_spesa SERIAL PRIMARY KEY,                -- Chiave Primaria
    data_movimento DATE NOT NULL,               -- Formato YYYY-MM-DD
    valore_spesa DECIMAL(10,2) NOT NULL CHECK (valore_spesa > 0), -- Vincolo CHECK: Importo > 0
    nota_opzionale TEXT,                        -- Descrizione facoltativa
    id_categoria INTEGER NOT NULL,
    
    -- Vincolo di Integrità Referenziale (Chiave Esterna)
    CONSTRAINT fk_spesa_categoria 
        FOREIGN KEY (id_categoria) 
        REFERENCES Categorie(id_categoria) 
);

-- 4. TABELLA BUDGET (Rif. Modulo 3)
-- Obiettivo: Definire i limiti di spesa mensili per categoria
CREATE TABLE Budget (
    id_budget SERIAL PRIMARY KEY,
    mese_riferimento VARCHAR(7) NOT NULL,       -- Formato YYYY-MM richiesto
    limite_spesa DECIMAL(10,2) NOT NULL CHECK (limite_spesa > 0), -- Vincolo CHECK
    id_categoria INTEGER NOT NULL,
    
    -- Chiave Esterna verso Categorie
    CONSTRAINT fk_budget_categoria 
        FOREIGN KEY (id_categoria) 
        REFERENCES Categorie(id_categoria),
        
    -- Vincolo UNIQUE: Impedisce duplicati dello stesso budget per mese/categoria
    CONSTRAINT uq_budget_mese UNIQUE (mese_riferimento, id_categoria)
);

-- 5. INSERIMENTO DATI DI ESEMPIO (Rif. Punto 8.1b)
-- Dati sufficienti a dimostrare il funzionamento (es. test superamento budget)
INSERT INTO Categorie (nome_categoria) VALUES ('Alimentari'), ('Trasporti');

-- Esempio Budget per Gennaio 2025
INSERT INTO Budget (mese_riferimento, limite_spesa, id_categoria) 
VALUES ('2025-01', 300.00, 1); 

-- Esempi Spese che portano al superamento del budget (25 + 400 = 425 > 300)
INSERT INTO Spese (data_movimento, valore_spesa, nota_opzionale, id_categoria) 
VALUES ('2025-01-15', 25.00, 'Pranzo veloce', 1),
       ('2025-01-20', 400.00, 'Spesa mensile extra', 1);

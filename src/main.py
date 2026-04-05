import psycopg2

# --- FUNZIONE DI CONNESSIONE AL DATABASE ---
def connetti_db():
    try:
        # Connessione al database PostgreSQL locale
        return psycopg2.connect(
            user="postgres", password="Simbetto1508@", 
            host="127.0.0.1", port="5432", database="SistemaSpese"
        )
    except Exception as e:
        print(f"Errore connessione: {e}")
        return None

# --- MODULO 1: Gestione Categorie ---
def modulo_categorie(conn):
    print("\n--- MODULO 1: Inserimento Categoria ---")
    nome = input("Nome della categoria: ")
    
    # Validazione: il nome non deve essere vuoto
    if not nome.strip():
        print("Errore: il nome non può essere vuoto.")
        return
        
    cur = conn.cursor()
    # Controllo preventivo per evitare duplicati (Vincolo UNIQUE)
    cur.execute("SELECT id_categoria FROM Categorie WHERE nome_categoria = %s", (nome,))
    if cur.fetchone():
        print("Messaggio di errore: La categoria esiste già.")
    else:
        cur.execute("INSERT INTO Categorie (nome_categoria) VALUES (%s)", (nome,))
        conn.commit()
        print("Messaggio di successo: Categoria inserita correttamente.")
    cur.close()

# --- MODULO 2: Inserimento Spesa (Con gestione Errore Data - Caso 4) ---
def modulo_spese(conn):
    print("\n--- MODULO 2: Inserimento Spesa ---")
    try:
        data = input("Data (YYYY-MM-DD): ")
        importo = float(input("Importo: "))
        
        # Validazione robustezza: importo > 0
        if importo <= 0:
            print("Errore: l'importo deve essere maggiore di zero.")
            return
            
        cat_nome = input("Nome della categoria: ")
        desc = input("Descrizione facoltativa: ")
        
        cur = conn.cursor()
        # Verifica esistenza categoria (Integrità Referenziale)
        cur.execute("SELECT id_categoria FROM Categorie WHERE nome_categoria = %s", (cat_nome,))
        ris = cur.fetchone()
        
        if ris:
            try:
                # Inserimento con gestione errore formato data
                cur.execute("INSERT INTO Spese (data_spesa, importo, descrizione, id_categoria) VALUES (%s,%s,%s,%s)", (data, importo, desc, ris[0]))
                conn.commit()
                print("Successo: Spesa inserita correttamente.")
            except psycopg2.DataError:
                # Caso 4: Gestione formato data errato (es. '9 gennaio')
                print("Errore: Formato data non valido. Usa il formato YYYY-MM-DD.")
                conn.rollback()
        else:
            print("Errore: la categoria non esiste.")
        cur.close()
    except ValueError: 
        print("Errore: Inserire un numero valido per l'importo.")

# --- MODULO 3: Definizione Budget (Con gestione Errore Formato) ---
def modulo_budget(conn):
    print("\n--- MODULO 3: Definizione Budget ---")
    mese = input("Mese (YYYY-MM): ")
    cat_nome = input("Nome della categoria: ")
    try:
        importo = float(input("Importo del budget: "))
        if importo <= 0:
            print("Errore: il budget deve essere maggiore di zero.")
            return
            
        cur = conn.cursor()
        cur.execute("SELECT id_categoria FROM Categorie WHERE nome_categoria = %s", (cat_nome,))
        ris = cur.fetchone()
        
        if ris:
            try:
                cur.execute("INSERT INTO Budget (mese_riferimento, importo_limite, id_categoria) VALUES (%s,%s,%s)", (mese, importo, ris[0]))
                conn.commit()
                print("Output: Budget mensile salvato correttamente.")
            except psycopg2.Error:
                print("Errore: Verificare il formato del mese o budget esistente.")
                conn.rollback()
        else:
            print("Errore: la categoria non esiste.")
        cur.close()
    except ValueError: 
        print("Errore: Inserire un numero valido.")

# --- MODULO 4: Report (Caso 3: Gestione Report Vuoti) ---
def report_1(conn):
    cur = conn.cursor()
    cur.execute("SELECT c.nome_categoria, SUM(s.importo) FROM Spese s JOIN Categorie c ON s.id_categoria = c.id_categoria GROUP BY c.nome_categoria")
    print("\n--- REPORT 1: TOTALE PER CATEGORIA ---")
    risultati = cur.fetchall()
    if not risultati:
        print("Nessuna spesa presente nel sistema.")
    for r in risultati: 
        print(f"{r[0]}: {r[1]:.2f}")
    cur.close()

import psycopg2

def connetti_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="SistemaSpese", 
            user="postgres",
            password="Simbetto1508@",
            port="5432"
        )
        conn.autocommit = True
        return conn
    except Exception as e:
        print(f"ERRORE DI CONNESSIONE: {e}")
        return None

# MODULO 1 - Gestione Categorie
def gestione_categorie():
    nome = input("Inserisci il nome della nuova categoria: ")
    if not nome:
        print("Errore: Il nome non può essere vuoto.") 
        return
    conn = connetti_db()
    if conn:
        cur = conn.cursor()
        try:
            # Controllo esistenza (SQL SELECT) [cite: 7, 8]
            cur.execute("SELECT nome_categoria FROM categorie WHERE nome_categoria = %s", (nome,))
            if cur.fetchone():
                print("Errore: La categoria esiste già.") 
            else:
                # Inserimento categoria (SQL INSERT) [cite: 8]
                cur.execute("INSERT INTO categorie (nome_categoria) VALUES (%s)", (nome,))
                print("Categoria inserita correttamente.") 
        except Exception as e:
            print(f"Errore: {e}")
        finally:
            cur.close()
            conn.close()

# MODULO 2 - Inserimento Spesa
def inserisci_spesa():
    print("\n--- Inserimento Spesa ---")
    data = input("Data (YYYY-MM-DD): ")
    try:
        importo = float(input("Importo: "))
        if importo <= 0:
            print("Errore: l'importo deve essere maggiore di zero.") 
            return
        cat_nome = input("Nome della categoria: ")
        desc = input("Descrizione facoltativa: ")
        
        conn = connetti_db()
        if conn:
            cur = conn.cursor()
            # Verifica esistenza categoria 
            cur.execute("SELECT id_categoria FROM categorie WHERE nome_categoria = %s", (cat_nome,))
            res = cur.fetchone()
            if not res:
                print("Errore: la categoria non esiste.") 
            else:
                # SQL INSERT con chiave esterna 
                cur.execute("INSERT INTO spese (data_movimento, valore_spesa, nota_opzionale, id_categoria) VALUES (%s, %s, %s, %s)", 
                            (data, importo, desc, res[0]))
                print("Spesa inserita correttamente.") 
            cur.close()
            conn.close()
    except ValueError:
        print("Errore: Inserire un valore numerico valido.")

# MODULO 3 - Definizione Budget
def definisci_budget():
    mese = input("Mese (YYYY-MM): ")
    cat_nome = input("Nome della categoria: ")
    try:
        importo = float(input("Importo del budget: "))
        if importo <= 0:
            print("Errore: il budget deve essere maggiore di zero.") 
            return
        
        conn = connetti_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT id_categoria FROM categorie WHERE nome_categoria = %s", (cat_nome,))
            res = cur.fetchone()
            if not res:
                print("Errore: la categoria non esiste.")
            else:
                # Inserimento o aggiornamento (SQL INSERT/UPDATE) [cite: 13]
                cur.execute("""INSERT INTO budget (mese_riferimento, limite_spesa, id_categoria) 
                               VALUES (%s, %s, %s) ON CONFLICT (mese_riferimento, id_categoria) 
                               DO UPDATE SET limite_spesa = EXCLUDED.limite_spesa""", (mese, importo, res[0]))
                print("Budget mensile salvato correttamente.") 
            cur.close()
            conn.close()
    except ValueError:
        print("Errore: Inserire un numero valido.")

# MODULO 4 - Reportistica
def sottomenu_report():
    while True:
        print("\n--- MENU DEI REPORT ---") 
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese")
        print("4. Ritorna al menu principale")
        scelta = input("Scegli un'opzione: ")
        
        conn = connetti_db()
        if not conn: break
        cur = conn.cursor()
        
        if scelta == '1': # REPORT 1 [cite: 16]
            cur.execute("SELECT c.nome_categoria, SUM(s.valore_spesa) FROM spese s JOIN categorie c ON s.id_categoria = c.id_categoria GROUP BY c.nome_categoria")
            print("\nCategoria | Totale Speso")
            for row in cur.fetchall():
                print(f"{row[0]} | {row[1]}")
        elif scelta == '2': # REPORT 2 
            cur.execute("""SELECT b.mese_riferimento, c.nome_categoria, b.limite_spesa, COALESCE(SUM(s.valore_spesa), 0)
                           FROM budget b JOIN categorie c ON b.id_categoria = c.id_categoria
                           LEFT JOIN spese s ON c.id_categoria = s.id_categoria AND b.mese_riferimento = to_char(s.data_movimento, 'YYYY-MM')
                           GROUP BY b.mese_riferimento, c.nome_categoria, b.limite_spesa""")
            for row in cur.fetchall():
                stato = "SUPERAMENTO BUDGET" if row[3] > row[2] else "OK" 
                print(f"Mese: {row[0]} | Cat: {row[1]} | Budget: {row[2]} | Speso: {row[3]} | Stato: {stato}")
        elif scelta == '3': # REPORT 3 
            cur.execute("SELECT s.data_movimento, c.nome_categoria, s.valore_spesa, s.nota_opzionale FROM spese s JOIN categorie c ON s.id_categoria = c.id_categoria ORDER BY s.data_movimento")
            print("\nData | Categoria | Importo | Descrizione")
            for row in cur.fetchall():
                print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
        elif scelta == '4':
            cur.close()
            conn.close()
            break
        else:
            print("Scelta non valida.")
        cur.close()
        conn.close()

# MAIN - Menu Principale [cite: 4]
def main():
    print("BENVENUTO NEL SISTEMA SPESE") 
    while True:
        print("\nSISTEMA SPESE PERSONALI") 
        print("1. Gestione Categorie")
        print("2. Inserisci Spesa")
        print("3. Definisci Budget Mensile")
        print("4. Visualizza Report")
        print("5. Esci")
        scelta = input("Inserisci la tua scelta: ") 
        
        if scelta == '1': gestione_categorie()
        elif scelta == '2': inserisci_spesa()
        elif scelta == '3': definisci_budget()
        elif scelta == '4': sottomenu_report()
        elif scelta == '5': break
        else: print("Scelta non valida. Riprovare.") 

if __name__ == "__main__":
    main()

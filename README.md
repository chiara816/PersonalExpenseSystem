# PersonalExpenseSystem
# Sistema Gestione Spese Personali

Questo progetto è un applicativo Python per la gestione delle finanze personali, interfacciato con un database relazionale PostgreSQL.

## 8.4 Informazioni per l'esecuzione

### Requisiti per l'esecuzione
* **Interprete:** Python 3.12 o superiore.
* **Database:** PostgreSQL 16.
* **Librerie esterne:** `psycopg2` (per la connessione tra Python e PostgreSQL).

### Istruzioni dettagliate per eseguire il programma
1. **Configurazione Database:** Accedere a pgAdmin o psql ed eseguire lo script contenuto nel file `sql/database.sql` per creare le tabelle e i vincoli.
2. **Configurazione Python:** Aprire il file `src/main.py` e inserire le proprie credenziali di accesso al database (username, password, host).
3. **Avvio del programma:** Da terminale, posizionarsi nella cartella del progetto ed eseguire il comando:
   ```bash
   python src/main.py
   In alternativa, avviare il file main.py direttamente dall'IDE Eclipse tramite il tasto "Run".

8.5 Struttura del Repository
Il repository è organizzato come richiesto dalle specifiche:

/src: contiene il codice sorgente Python (main.py).

/sql: contiene lo script SQL per la creazione del database (database.sql).

/demo: il video dimostrativo e disponibile al seguente link: 
https://drive.google.com/file/d/1AaWmhxukbpr2MruUzKlbjr_r-qXvDQQ_/view?usp=sharing

README.md: istruzioni e documentazione del progetto.

Demo del funzionamento
Nella cartella demo/ è presente un video che mostra:

Avvio del programma e connessione al database.

Utilizzo del menu principale.

Inserimento di nuovi dati (Spese/Budget) con gestione degli errori (Robustezza).

Generazione di un report di riepilogo.

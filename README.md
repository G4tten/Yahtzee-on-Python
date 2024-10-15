# Yahtzee-on-Python (su terminale per il momento)

# Consegna
Creare un programma Python funzionante che consenta a due giocatori di giocare una partita completa a Yahtzee tramite il terminale, con calcolo automatico dei punteggi e dichiarazione del vincitore.

## Una volta finito il lavoro:
Cambiare il README e rendere PUBBLICO il repository in modo da aggiungere questo lavoro ai nostri profili GitHub per un prossimo futuro da programmatori (daje Lulu)

## Obiettivo
Creare un gioco Yahtzee a due giocatori che permetta di lanciare i dadi, selezionare i dadi da conservare, calcolare i punteggi e determinare un vincitore, tutto all'interno del terminale.

## Meccaniche
- Il gioco deve supportare 2 giocatori
- Ogni giocatore deve avere una tabella di punteggi con tutte le categorie di Yahtzee
- Ogni giocatore può ***lanciare 5 dadi fino a un massimo di 3 volte a turno***
- Dopo ogni lancio il giocatore può ***scegliere quali dadi tenere e quali rilanciare***
- ***Dopo i 3 lanci O QUANDO IL GIOCATORE DECIDE DI FERMARSI***, il giocatore deve scegliere una delle categorie per segnare il punteggio (*non è possibile sovrascrivere un punteggio già registrato*)
- Il punteggio deve essere calcolato in base ai dadi attuali e alla categoria scelta
- Il gioco termina quando tutte le categorie di punteggio di ***entrambi i giocatori*** sono state completate
- Il vincitore viene determinato in base al punteggio totale più alto

## Possibile svolgimento
- Classe *GIOCATORE*
  - Memorizza il nome del giocatore
  - Contiene il tabellone con tutte le categorie
  - Contiene il punteggio totale del giocatore
 
- Funzione *LANCIO DADI*
  - Simula il lancio di 5 dadi
  - Consente di rilanciare alcuni dadi fino a 2 volte a turno

- Funzione *CALCOLO PUNTEGGIO*
  - Calcola il punteggio in base ai dadi attuali e alla categoria scelta
 
- Funzione *STAMPA TABELLONE*
  - Mostra il tabellone aggiornato con i punteggi
 
- Funzione *GIOCA TURNO*
  - Gestisce l'intero turno per un giocatore, inclusi i lanci dei dadi e la scelta della categoria di punteggio.
 
- Funzione *GIOCA PARTITA*
  - Gestisce l'intero flusso del gioco per entrambi i giocatori fino alla fine della partita.

 ## Suggerimenti Chat GPT (magari questo dopo lo togliamo quando lo pubblichiamo XD)
 - Usa liste per memorizzare i valori dei dadi e i punteggi parziali.
 - Utilizza un ciclo per alternare i turni tra i giocatori.

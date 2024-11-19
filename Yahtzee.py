import random
import pygame

# Inizializzazione di Pygame
pygame.init()

# Configurazione dello schermo e delle dimensioni
screen_width = 600 
screen_height = 900 

screen = pygame.display.set_mode((screen_width, screen_height))  # Creazione della finestra di gioco
pygame.display.set_caption("Yahtzee Game")  # Titolo della finestra

# Configurazione del font per il testo
font = pygame.font.Font('font/casino.ttf', 28)  # Font personalizzato per il testo (stile e grandezza)

# Palette di colori
teal = (37, 113, 128)
beige = (242, 229, 191)
orange = (253, 139, 81)
dark_orange = (180, 100, 50)
bordeaux = (203, 96, 64)
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)

# Imposta il colore di sfondo
background = beige

# Caricamento delle immagini dei dadi
immagini_dadi = [
    pygame.image.load("immagini/dadi/1.png"),
    pygame.image.load("immagini/dadi/2.png"),
    pygame.image.load("immagini/dadi/3.png"),
    pygame.image.load("immagini/dadi/4.png"),
    pygame.image.load("immagini/dadi/5.png"),
    pygame.image.load("immagini/dadi/6.png")
]

# Ridimensiona le immagini dei dadi a 100x100 pixel
resize_immagine = [pygame.transform.scale(img, (100, 100)) for img in immagini_dadi]

# Ottieni le dimensioni delle immagini ridimensionate
size_immagine = [img.get_size() for img in resize_immagine]

# Variabili per la gestione del tiro
tiro = False  # Stato del tiro (attivo o no)
counter = 0  # Numero di tiri effettuati
max_tiri = 3  # Numero massimo di tiri per turno

# Classe per rappresentare i dadi
class Dado:
    def __init__(self, x_pos, y_pos, num, key):
        # Posizione, numero attuale e identificativo del dado
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.numero = num
        self.key = key

    def draw(self):
        # Disegna l'immagine del dado corrispondente al numero attuale
        screen.blit(resize_immagine[self.numero - 1], (self.x_pos, self.y_pos))

    def lancio_dadi(self):
        # Genera un nuovo valore casuale per il dado
        self.numero = random.randint(1, 6)

# Creazione di 5 dadi con posizioni iniziali e numeri
dado1 = Dado(10, 50, 1, 0)
dado2 = Dado(130, 50, 2, 1)
dado3 = Dado(250, 50, 3, 2)
dado4 = Dado(370, 50, 4, 3)
dado5 = Dado(490, 50, 5, 4)

# Lista contenente tutti i dadi
dadi = [dado1, dado2, dado3, dado4, dado5]

# Configurazione del pulsante "Tira!"
btn_testo = font.render("Tira!", True, white)
fine_btn = pygame.draw.rect(screen, bordeaux, [300, 180, 280, 50])  # Pulsante di fine turno
tira_btn_colore = orange

# Font e combinazioni del tabellone
font = pygame.font.Font('font/casino.ttf', 36)
combinazioni = [
    "Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", 
    "Tris", "Quadris", "Full", "Scala", "Yahtzee", "Totale"
]

# Funzione per disegnare la griglia del tabellone
def disegna_griglia(schermo, righe, colonne, larghezza_cella, altezza_cella, x_inizio, y_inizio):
    colore_griglia = black

    # Sfondo della griglia
    sfondo_griglia = pygame.Rect(x_inizio, y_inizio, colonne * larghezza_cella, righe * altezza_cella)
    pygame.draw.rect(schermo, white, sfondo_griglia)

    # Disegna le celle della griglia
    for riga in range(righe):
        for colonna in range(colonne):
            rettangolo = pygame.Rect(
                x_inizio + colonna * larghezza_cella,
                y_inizio + riga * altezza_cella,
                larghezza_cella, altezza_cella
            )
            pygame.draw.rect(schermo, colore_griglia, rettangolo, 3)
    
    # Aggiungi i nomi delle combinazioni nella prima colonna
    for indice, combinazione in enumerate(combinazioni):
        if indice < righe:
            testo = font.render(combinazione, True, black)
            schermo.blit(testo, (x_inizio + 10, y_inizio + indice * altezza_cella + 10))

# Configurazione griglia del tabellone
larghezza_cella = 150
altezza_cella = 50
righe = 12
colonne = 3
offset_x = 65  # Offset griglia (sinistra)
offset_y = 280  # Offset griglia (alto)

# Funzione per rilevare clic sulla griglia
def rileva_clic(x, y):
    if offset_x <= x <= offset_x + colonne * larghezza_cella and \
       offset_y <= y <= offset_y + righe * altezza_cella:
        x_relativo = x - offset_x
        y_relativo = y - offset_y
        colonna = x_relativo // larghezza_cella
        riga = y_relativo // altezza_cella
        return colonna, riga
    else:
        return None, None

# Dizionario dei punteggi
punteggi = {}
def calcola_punteggi(dadi):
    conteggio_dadi = [0] * 6  # Occorrenze di ogni numero (1-6)
    for dado in dadi:
        conteggio_dadi[dado.numero - 1] += 1

        # Calcola i punteggi per ogni combinazione
        punteggi["Uno"] = conteggio_dadi[0] * 1
        punteggi["Due"] = conteggio_dadi[1] * 2
        punteggi["Tre"] = conteggio_dadi[2] * 3
        punteggi["Quattro"] = conteggio_dadi[3] * 4
        punteggi["Cinque"] = conteggio_dadi[4] * 5
        punteggi["Sei"] = conteggio_dadi[5] * 6

        punteggi["Tris"] = sum([dado.numero for dado in dadi]) if max(conteggio_dadi) >= 3 else 0
        punteggi["Quadris"] = sum([dado.numero for dado in dadi]) if max(conteggio_dadi) >= 4 else 0
        punteggi["Full"] = 25 if 3 in conteggio_dadi and 2 in conteggio_dadi else 0
        punteggi["Scala"] = 40 if sorted(set([dado.numero for dado in dadi])) in [list(range(1, 6)), list(range(2, 7))] else 0
        punteggi["Yahtzee"] = 50 if max(conteggio_dadi) == 5 else 0

    return punteggi

# Tabellone con i punteggi definitivi
tabellone = {}
def salva_punteggi(colonna, riga, punteggi):
    # Salva i punteggi selezionati nel tabellone
    if colonna == 1:
        chiave = combinazioni[riga]
        tabellone[chiave] = punteggi.get(chiave, 0)
    return tabellone

# Calcola il totale dei punti
def totale(tabellone):
    return sum(tabellone.values())




#########################################################################################
# Variabili di inizializzazione e configurazioni Pygame
run = True  # Variabile per mantenere attivo il ciclo di gioco
tiro = False  # Stato del tiro di dadi
counter = 0  # Conteggio dei tiri effettuati

while run:  # Inizio del ciclo principale del gioco (game loop)

    # Aggiorna lo sfondo
    screen.fill(background)
    
    # Disegna la griglia del tabellone
    disegna_griglia(screen, righe, colonne, larghezza_cella, altezza_cella, 65, 280)

    # Disegna i dadi sullo schermo
    for dado in dadi:
        dado.draw()

    # Imposta il pulsante "Tira!" o "Tiri finiti" in base al numero di lanci rimanenti
    if counter >= max_tiri:
        tira_btn_colore = dark_orange
        btn_testo = font.render("Tiri finiti", True, white)
    else:
        tira_btn_colore = orange
        btn_testo = font.render("Tira!", True, white)

    # Disegna il pulsante di fine tiri se il numero massimo di lanci è stato raggiunto
    if counter == max_tiri:
        fine_btn = pygame.draw.rect(screen, bordeaux, [330, 180, 160, 50])

    # Disegna il pulsante "Tira!" con il colore e testo aggiornati
    tira_btn = pygame.draw.rect(screen, tira_btn_colore, [150, 180, 160, 50])

    # Mostra il testo del pulsante "Tira!" sopra il pulsante
    screen.blit(btn_testo, [155, 190])

    # Gestore degli eventi Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Se l'utente chiude la finestra
            run = False

        # Gestione dei click del mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Controlla se il pulsante "Tira!" è stato cliccato e se ci sono tiri disponibili
            if tira_btn.collidepoint(event.pos) and counter < max_tiri:
                tiro = True
                counter += 1

            # Controlla se il pulsante "Fine Tiri" è stato cliccato (dopo il numero massimo di lanci)
            if fine_btn.collidepoint(event.pos) and counter == max_tiri:
                counter = 0  # Resetta il conteggio dei tiri per il prossimo turno

            # Controlla se è stata cliccata una cella del tabellone e salva il punteggio
            colonna, riga = rileva_clic(mouse_x, mouse_y)
            if colonna is not None and riga is not None:
                print(f"Hai cliccato sulla cella ({riga}, {colonna})")
                salva_punteggi(colonna, riga, punteggi)  # Salva il punteggio nella cella specificata
                print(f"Tabellone aggiornato: {tabellone}")

    # Se il tiro è stato effettuato
    if tiro:
        for dado in dadi:
            dado.lancio_dadi()  # Lancia i dadi
        punteggi = calcola_punteggi(dadi)  # Calcola i punteggi in base ai risultati del lancio
        tiro = False  # Reimposta lo stato del tiro per il prossimo turno

    # Mostra i punteggi sul tabellone
    y_offset = 290  # Posizione iniziale del testo
    for combinazione, punteggio in punteggi.items():
        if combinazione in tabellone:
            # Mostra il punteggio definitivo in nero se confermato nel tabellone
            testo_punteggio = font.render(f"{tabellone[combinazione]}", True, black)
        else:
            # Mostra il punteggio provvisorio in grigio se non confermato
            testo_punteggio = font.render(f"{punteggio}", True, gray)
        
        screen.blit(testo_punteggio, (280, y_offset))  # Visualizza il punteggio sulla griglia
        y_offset += 50  # Spaziatura tra le righe

    # Calcola il totale dei punteggi e lo visualizza sul tabellone
    totale_punteggi = totale(tabellone)  # Funzione per calcolare il totale nel dizionario `tabellone`
    totale_text = font.render(f"{totale_punteggi}", True, black)
    screen.blit(totale_text, (280, y_offset))  # Visualizza il totale dei punti

    # Aggiorna lo schermo di gioco
    pygame.display.flip()

# Uscita dal programma
pygame.quit()



import random
import pygame

pygame.init()  # Inizializzazione del modulo Pygame
 
# Dimensioni dello schermo di gioco
screen_width = 600 
screen_height = 900 

# Creazione della finestra di gioco
screen = pygame.display.set_mode((screen_width, screen_height))  
pygame.display.set_caption("Yahtzee Game")  # Titolo della finestra
font = pygame.font.Font('font/casino.ttf', 28)  # Imposta il font per il testo

# Palette di colori da utilizzare nel gioco
teal = (37, 113, 128)
beige = (242, 229, 191)
orange = (253, 139, 81)
dark_orange = (180, 100, 50)
bordeaux = (203, 96, 64)
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)

background = beige  # Colore di sfondo

# Caricamento delle immagini dei dadi
immagini_dadi = [
    pygame.image.load("immagini/dadi/1.png"), 
    pygame.image.load("immagini/dadi/2.png"), 
    pygame.image.load("immagini/dadi/3.png"), 
    pygame.image.load("immagini/dadi/4.png"), 
    pygame.image.load("immagini/dadi/5.png"), 
    pygame.image.load("immagini/dadi/6.png")
]

# Ridimensionamento delle immagini dei dadi
resize_immagine = [pygame.transform.scale(img, (100, 100)) for img in immagini_dadi]
size_immagine = [img.get_size() for img in resize_immagine]  # Ottieni le dimensioni ridimensionate

tiro = False  # Variabile per tracciare se i dadi sono stati tirati
counter = 0  # Conteggio dei tiri effettuati
max_tiri = 3  # Numero massimo di tiri consentiti

# Classe per definire il comportamento di un dado
class Dado:
    def __init__(self, x_pos, y_pos, num, selezionato):
        self.x_pos = x_pos  # Posizione X del dado
        self.y_pos = y_pos  # Posizione Y del dado
        self.numero = num  # Numero mostrato dal dado
        self.selezionato = selezionato  #controlla se il dado è stato selezionato o no

    # Metodo per disegnare il dado sullo schermo
    def draw(self):
        if self.numero == 1:
            screen.blit(resize_immagine[0], (self.x_pos, self.y_pos))
        elif self.numero == 2:
            screen.blit(resize_immagine[1], (self.x_pos, self.y_pos))
        elif self.numero == 3:
            screen.blit(resize_immagine[2], (self.x_pos, self.y_pos))
        elif self.numero == 4:
            screen.blit(resize_immagine[3], (self.x_pos, self.y_pos))
        elif self.numero == 5:
            screen.blit(resize_immagine[4], (self.x_pos, self.y_pos))
        elif self.numero == 6:
            screen.blit(resize_immagine[5], (self.x_pos, self.y_pos))
        
        if self.selezionato:
            bordo_dado = pygame.Rect(self.x_pos, self.y_pos, 100, 100)
            pygame.draw.rect(screen, bordeaux, bordo_dado, 10)

    def seleziona_dadi(self, pos, dadi):
        larghezza_dado = 100
        margine = 20 #margine per ogni dado

        for dado in dadi:
            if dado.x_pos <= pos[0] <= dado.x_pos + larghezza_dado + margine and dado.y_pos <= pos[1] <= dado.y_pos + larghezza_dado:
                dado.selezionato = not dado.selezionato

    # Metodo per lanciare il dado e generare un nuovo numero casuale
    def lancio_dadi(self):
        self.numero = random.randint(1, 6)

# Creazione di cinque dadi con posizioni iniziali
dado1 = Dado(10, 50, 1, False)
dado2 = Dado(130, 50, 2, False)
dado3 = Dado(250, 50, 3, False)
dado4 = Dado(370, 50, 4, False)
dado5 = Dado(490, 50, 5, False)

dadi = [dado1, dado2, dado3, dado4, dado5]  # Lista dei dadi

btn_testo = font.render("Tira!", True, white)  # Testo per il pulsante "Tira!"

fine_btn = pygame.draw.rect(screen, bordeaux, [300, 180, 280, 50])  # Pulsante "Fine Tiri"
tira_btn_colore = orange  # Colore iniziale del pulsante "Tira!"

# Lista delle combinazioni visualizzate nel tabellone
combinazioni = [
    "Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", 
    "Tris", "Quadris", "Full", "Scala", "Yahtzee", "Totale"
]

# Funzione per disegnare la griglia del tabellone
def disegna_griglia(schermo, righe, colonne, larghezza_cella, altezza_cella, x_inizio, y_inizio):
    colore_griglia = black  # Colore delle linee della griglia

    # Disegna lo sfondo del tabellone
    sfondo_griglia = pygame.Rect(x_inizio, y_inizio, colonne * larghezza_cella, righe * altezza_cella)
    pygame.draw.rect(schermo, white, sfondo_griglia)

    # Disegna ogni cella della griglia
    for riga in range(righe):
        for colonna in range(colonne):
            rettangolo = pygame.Rect(
                x_inizio + colonna * larghezza_cella, 
                y_inizio + riga * altezza_cella, 
                larghezza_cella, 
                altezza_cella
            )
            pygame.draw.rect(schermo, colore_griglia, rettangolo, 3)

    # Aggiungi il testo delle combinazioni nella prima colonna
    for indice, combinazione in enumerate(combinazioni):
        if indice < righe:  # Assicurati di non eccedere il numero di righe
            testo = font.render(combinazione, True, black)  # Renderizza il testo
            schermo.blit(testo, (x_inizio + 10, y_inizio + indice * altezza_cella + 10))  # Posiziona il testo con un piccolo margine

# Dimensioni e posizione del tabellone
larghezza_cella = 150
altezza_cella = 50
righe = 12
colonne = 3
offset_x = 65  # Offset orizzontale della griglia
offset_y = 280  # Offset verticale della griglia

# Funzione per rilevare il click sulla griglia
def rileva_clic(x, y):
    if offset_x <= x <= offset_x + colonne * larghezza_cella and \
       offset_y <= y <= offset_y + righe * altezza_cella:
        
        x_relativo = x - offset_x
        y_relativo = y - offset_y
        
        # Calcola la colonna e la riga cliccate
        colonna = x_relativo // larghezza_cella
        riga = y_relativo // altezza_cella
        
        print(f'Cella cliccata: Colonna {colonna}, Riga {riga}')
        return colonna, riga
    
    else:
        print('Clic fuori dalla griglia')
        return None, None
            
# Dizionario per tracciare i punteggi
punteggi = {}  

# Funzione per calcolare i punteggi basati sui dadi tirati
def calcola_punteggi(dadi):
    conteggio_dadi = [0] * 6  # Contatore delle occorrenze di ogni numero
    for dado in dadi:
        conteggio_dadi[dado.numero - 1] += 1

    # Calcolo dei punteggi per ogni combinazione
    punteggi["Uno"] = conteggio_dadi[0] * 1
    punteggi["Due"] = conteggio_dadi[1] * 2
    punteggi["Tre"] = conteggio_dadi[2] * 3
    punteggi["Quattro"] = conteggio_dadi[3] * 4
    punteggi["Cinque"] = conteggio_dadi[4] * 5
    punteggi["Sei"] = conteggio_dadi[5] * 6
    
    if max(conteggio_dadi) >= 3:
        punteggi["Tris"] = sum([dado.numero for dado in dadi]) 
    else:
        punteggi["Tris"] = 0

    if max(conteggio_dadi) >= 4:
        punteggi["Quadris"] = sum([dado.numero for dado in dadi])
    else:
        punteggi["Quadris"] = 0

    if 3 in conteggio_dadi and 2 in conteggio_dadi:
        punteggi["Full"] = 25
    else:
        punteggi["Full"] = 0
    
    if sorted(set([dado.numero for dado in dadi])) in [list(range(1, 6)), list(range(2, 7))]: 
        punteggi["Scala"] = 40
    else:
        punteggi["Scala"] = 0
    
    if max(conteggio_dadi) == 5:
        punteggi["Yahtzee"] = 50
    else:
        punteggi["Yahtzee"] = 0

    return punteggi

tabellone = {}
def salva_punteggi(colonna, riga, punteggi):
    if colonna == 1 and riga == 0 :
            tabellone["Uno"] = punteggi["Uno"]
    
    if colonna == 1 and riga == 1 :
            tabellone["Due"] = punteggi["Due"]
    
    if colonna == 1 and riga == 2 :
            tabellone["Tre"] = punteggi["Tre"]
    
    if colonna == 1 and riga == 3 :
            tabellone["Quattro"] = punteggi["Quattro"]
    
    if colonna == 1 and riga == 4 :
            tabellone["Cinque"] = punteggi["Cinque"]
    
    if colonna == 1 and riga == 5 :
            tabellone["Sei"] = punteggi["Sei"]  
    
    if colonna == 1 and riga == 6 :
            tabellone["Tris"] = punteggi["Tris"]
    
    if colonna == 1 and riga == 7 :
            tabellone["Quadris"] = punteggi["Quadris"]
    
    if colonna == 1 and riga == 8 :
            tabellone["Full"] = punteggi["Full"]
    
    if colonna == 1 and riga == 9 :
            tabellone["Scala"] = punteggi["Scala"]
    
    if colonna == 1 and riga == 10 :
            tabellone["Yahtzee"] = punteggi["Yahtzee"]

    
    for combinazione in punteggi:
        if combinazione not in tabellone:  # mantiene solo il valore salvato
            punteggi[combinazione] = " "


    return tabellone


def totale(tabellone):
    totale=0
    for punteggio in tabellone.values():
        totale += punteggio
    
    return totale


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

            for dado in dadi:
                dado.seleziona_dadi((mouse_x, mouse_y), dadi)

            

    # Se il tiro è stato effettuato
    if tiro:
        for dado in dadi:
            if dado.selezionato == False:
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
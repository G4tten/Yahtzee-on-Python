import random
import pygame

pygame.init()  # Inizializzazione del modulo Pygame

#Schermo
info = pygame.display.Info()
screen_widht = 600
screen_height = info.current_h - 100

# Creazione della finestra di gioco
screen = pygame.display.set_mode((screen_widht, screen_height))
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

immagine_QUIT = pygame.image.load("immagini/immagine_x.png")
immagine_QUIT = pygame.transform.scale(immagine_QUIT, (50, 50))

rect_quit = immagine_QUIT.get_rect()
rect_quit.topright = (screen_widht - 10, 10) #aggiungi un margine di 10 pixel 

# Ridimensionamento delle immagini dei dadi
resize_immagine = [pygame.transform.scale(img, (100, 100)) for img in immagini_dadi]
size_immagine = [img.get_size() for img in resize_immagine]  # Ottieni le dimensioni ridimensionate

tiro = False  # Variabile per tracciare se i dadi sono stati tirati
counter = 0  # Conteggio dei tiri effettuati
max_tiri = 3  # Numero massimo di tiri consentiti

class Giocatore:
    def __init__(self, nome):
        self.nome = nome  # Nome del giocatore
        self.tabellone = {}  # Tabellone personale
        self.totale = 0  # Totale punti

    def salva_punteggi(self, riga, punteggi):
        # Mappa delle righe per associare il rigo a una chiave del tabellone
        riga_to_chiave = {
            0: "Uno", 1: "Due", 2: "Tre", 3: "Quattro", 
            4: "Cinque", 5: "Sei", 6: "Tris", 7: "Quadris", 
            8: "Full", 9: "Scala", 10: "Yahtzee"
        }

        # Controllare che la riga sia valida
        if riga in riga_to_chiave:
            chiave = riga_to_chiave[riga]

            # Aggiungere solo se la chiave non è già presente nel tabellone
            if chiave not in self.tabellone:
                self.tabellone[chiave] = punteggi.get(chiave)  # Preleva il punteggio
                self.totale += punteggi.get(chiave)  # Aggiorna il totale punti
            else:
                print(f"La combinazione '{chiave}' è già stata utilizzata.")

        # Ripulire le combinazioni non selezionate
        for combinazione in punteggi:
            if combinazione not in self.tabellone:
                punteggi[combinazione] = " "

        return self.tabellone

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
dado1 = Dado(10, 50, 6, False)
dado2 = Dado(130, 50, 6, False)
dado3 = Dado(250, 50, 6, False)
dado4 = Dado(370, 50, 6, False)
dado5 = Dado(490, 50, 6, False)

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


giocatore1= Giocatore("Luigi")
giocatore2= Giocatore ("Ludovica")


#########################################################################################
# Inizializzazione delle variabili di gioco
run = True  # Variabile per mantenere attivo il ciclo di gioco
tiro = False  # Stato del tiro dei dadi
counter = 0  # Conteggio dei tiri effettuati
turno = True  # True: Giocatore 1, False: Giocatore 2

pygame.mixer.music.load("suoni/suono_gioco.mp3")
pygame.mixer.music.play(-1, 0.0)  # Riproduce la musica in loop
pygame.mixer.music.set_volume(0.3)

suono_roll= pygame.mixer.Sound("suoni/rolls.mp3")
# Ciclo principale del gioco (game loop)
while run:

    
    # 1. Aggiornamento dello sfondo
    screen.fill(background)
    
    # 2. Disegno della griglia del tabellone
    disegna_griglia(screen, righe, colonne, larghezza_cella, altezza_cella, 65, 280)
    
    # 3. Disegno dei dadi sullo schermo
    for dado in dadi:
        dado.draw()
    
    # 4. Disegno del pulsante "Quit"
    screen.blit(immagine_QUIT, rect_quit)
    
    # 5. Impostazione del pulsante "Tira!" o "Tiri finiti"
    if counter >= max_tiri:
        tira_btn_colore = dark_orange
        btn_testo = font.render("Tiri finiti", True, white)
    else:
        tira_btn_colore = orange
        btn_testo = font.render("Tira!", True, white)

    # 6. Disegno del pulsante "Fine Tiri" se il numero massimo di tiri è stato raggiunto
    if counter == max_tiri:
        fine_btn = pygame.draw.rect(screen, bordeaux, [330, 180, 160, 50])
    
    # 7. Disegno del pulsante "Tira!" con colore e testo aggiornati
    tira_btn = pygame.draw.rect(screen, tira_btn_colore, [150, 180, 160, 50])
    screen.blit(btn_testo, [155, 190])
    
    # Gestione degli eventi Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False  # Esci dal gioco se viene chiusa la finestra
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # 8. Controllo se il pulsante "Quit" è stato cliccato
            if rect_quit.collidepoint(event.pos):
                run = False  # Esci dal gioco
            
            # 9. Controllo se il pulsante "Tira!" è stato cliccato
            if tira_btn.collidepoint(event.pos) and counter < max_tiri:
                tiro = True  # Avvia il tiro dei dadi
                counter += 1  # Incrementa il numero di tiri
                # Lancia i dadi non selezionati
                for dado in dadi:
                    if not dado.selezionato:
                        dado.lancio_dadi()
                suono_roll.play()

                # Calcola i punteggi dopo il lancio
                punteggi = calcola_punteggi(dadi)
            
            # 10. Controllo se il pulsante "Fine Tiri" è stato cliccato
            if fine_btn.collidepoint(event.pos) and counter == max_tiri:
                counter = 0  # Resetta il conteggio dei tiri
                turno = not turno  # Cambia il turno del giocatore

                # Resetta i dadi (non selezionati e valore a uno)
                for dado in dadi:
                    dado.selezionato = False
                    dado.numero = 6
            
            # 11. Gestione della selezione dei dadi
            for dado in dadi:
                dado.seleziona_dadi((mouse_x, mouse_y), dadi)

            # 12. Controllo se è stata cliccata una cella del tabellone
            colonna, riga = rileva_clic(mouse_x, mouse_y)
            
            if turno:
                if colonna is not None and riga is not None:
                    print(f"Hai cliccato sulla cella ({riga}, {colonna})")
                    giocatore1.salva_punteggi(riga, punteggi)  # Salva il punteggio
                    turno = not turno
                    counter=0
                    for dado in dadi:
                        dado.selezionato = False
                        dado.numero = 6
                    print(f"Tabellone 1 aggiornato: {giocatore1.tabellone}")
            else:
                if colonna is not None and riga is not None:
                    print(f"Hai cliccato sulla cella ({riga}, {colonna})")
                    giocatore2.salva_punteggi(riga, punteggi)  # Salva il punteggio
                    turno = not turno
                    counter= 0
                    for dado in dadi:
                        dado.selezionato = False
                        dado.numero = 6
                    print(f"Tabellone 2 aggiornato: {giocatore2.tabellone}")
    
    #scritta del turno corrente
    if turno:
        testo_giocatore1= font.render (f"Turno giocatore 1", True, black)
        screen.blit(testo_giocatore1, (18,20))
    else:
        testo_giocatore2= font.render (f"Turno giocatore 2", True, black)
        screen.blit(testo_giocatore2, (18,20))
    
    # 13. Mostra i punteggi sul tabellone per entrambi i giocatori
    y1_offset = 290
    y2_offset = 290
    x_pos1 = 280
    x_pos2 = 430

    if turno:  # Turno giocatore 1
        for combinazione, punteggio in punteggi.items():
            # Mostra punteggi del giocatore 1
            if combinazione in giocatore1.tabellone:
                testo_punteggio1 = font.render(f"{giocatore1.tabellone[combinazione]}", True, black)
                screen.blit(testo_punteggio1, (x_pos1, y1_offset))
            else:  # Mostra anteprima punteggi solo per giocatore corrente
                testo_punteggio1 = font.render(f"{punteggio}", True, gray)
                screen.blit(testo_punteggio1, (x_pos1, y1_offset))
            y1_offset += 50

            # Mostra punteggi del giocatore 2 SOLO se sono stati assegnati
            if combinazione in giocatore2.tabellone:
                testo_punteggio2 = font.render(f"{giocatore2.tabellone[combinazione]}", True, black)
                screen.blit(testo_punteggio2, (x_pos2, y2_offset))
            y2_offset += 50

    else:  # Turno giocatore 2
        for combinazione, punteggio in punteggi.items():
            # Mostra punteggi del giocatore 2
            if combinazione in giocatore2.tabellone:
                testo_punteggio2 = font.render(f"{giocatore2.tabellone[combinazione]}", True, black)
                screen.blit(testo_punteggio2, (x_pos2, y2_offset))
            else:  # Mostra anteprima punteggi solo per giocatore corrente
                testo_punteggio2 = font.render(f"{punteggio}", True, gray)
                screen.blit(testo_punteggio2, (x_pos2, y2_offset))
            y2_offset += 50

            # Mostra punteggi del giocatore 1 SOLO se sono stati assegnati
            if combinazione in giocatore1.tabellone:
                testo_punteggio1 = font.render(f"{giocatore1.tabellone[combinazione]}", True, black)
                screen.blit(testo_punteggio1, (x_pos1, y1_offset))
            y1_offset += 50



    # Calcola e mostra il totale dei punteggi
    totale_punteggi1 = giocatore1.totale
    totale_text1 = font.render(f"{totale_punteggi1}", True, black)
    screen.blit(totale_text1, (x_pos1, 840))

    totale_punteggi2 = giocatore2.totale
    totale_text2 = font.render(f"{totale_punteggi2}", True, black)
    screen.blit(totale_text2, (x_pos2, 840))



    

    
    # Aggiornamento dello schermo di gioco
    pygame.display.flip()

# Uscita dal programma Pygame
pygame.quit()


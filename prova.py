import random
import pygame

pygame.init()  # Inizializzazione del modulo Pygame

#Schermo
info = pygame.display.Info()
screen_widht = 1200
screen_height = 750

# Creazione della finestra di gioco
screen = pygame.display.set_mode((screen_widht, screen_height))
pygame.display.set_caption("Yahtzee Game")  # Titolo della finestra
font = pygame.font.Font('font/VCR_OSD_MONO_1.001.ttf', 28)  # Imposta il font per il testo
font_turno = pygame.font.Font('font/Daydream.ttf', 35)
font_tira = pygame.font.Font('font/Daydream.ttf', 28)

# Palette di colori da utilizzare nel gioco
teal = (37, 113, 128)
beige = (242, 229, 191)
dark_beige = (194, 183, 153)
# orange = (253, 139, 81)
# dark_orange = (180, 100, 50)
bordeaux = (203, 96, 64)
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
# background = beige  # Colore di sfondo

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
            pygame.draw.rect(screen, beige, bordo_dado, 10)

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
dado1 = Dado(550, 350, 6, False)
dado2 = Dado(670, 350, 6, False)
dado3 = Dado(790, 350, 6, False)
dado4 = Dado(910, 350, 6, False)
dado5 = Dado(1030, 350, 6, False)

dadi = [dado1, dado2, dado3, dado4, dado5]  # Lista dei dadi

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
offset_y = 100  # Offset verticale della griglia

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

# Aggiungi questa funzione per creare caselle di input
class InputBox:
    def __init__(self, x, y, w, h, font, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('gray')
        self.text = text
        self.font = font
        self.txt_surface = font.render(text, True, pygame.Color('black'))
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Controlla se il mouse è sopra la casella
            self.active = self.rect.collidepoint(event.pos)
            self.color = pygame.Color('dodgerblue') if self.active else pygame.Color('gray')
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                pass  # Premi INVIO per confermare
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, pygame.Color('black'))

    def draw(self, screen):
        # Disegna il testo e la casella
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


# Configura la finestra
screen = pygame.display.set_mode((1200,750))
font = pygame.font.Font(None, 50)

# Variabili del menu
nome_giocatore1 = InputBox(300, 200, 400, 50, font)
nome_giocatore2 = InputBox(300, 300, 400, 50, font)
pulsante_inizia = pygame.Rect(400, 400, 200, 50)
menu_attivo = True
stato_gioco = "menu"
clock = pygame.time.Clock()

# Ciclo principale
while menu_attivo:
    screen.fill((173, 216, 230))  # Colore sfondo (azzurro chiaro)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_attivo = False
            run = False  # Esci dal gioco

        nome_giocatore1.handle_event(event)
        nome_giocatore2.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pulsante_inizia.collidepoint(event.pos):
                # Passa al gioco solo se i nomi sono inseriti
                if nome_giocatore1.text and nome_giocatore2.text:
                    giocatore1_nome = nome_giocatore1.text
                    giocatore2_nome = nome_giocatore2.text
                    stato_gioco = "giocando"
                    menu_attivo = False

    # Disegna gli elementi del menu
    titolo = font.render("Inserisci i nomi dei giocatori", True, pygame.Color('black'))
    screen.blit(titolo, (250, 100))

    nome_giocatore1.draw(screen)
    nome_giocatore2.draw(screen)

    pygame.draw.rect(screen, pygame.Color('green'), pulsante_inizia)
    testo_pulsante = font.render("Inizia", True, pygame.Color('white'))
    screen.blit(testo_pulsante, (450, 410))

    # Aggiorna lo schermo
    pygame.display.flip()
    clock.tick(30)



# Ciclo principale del gioco (game loop)
while run:


    
    # 1. Aggiornamento dello sfondo
    if turno:
        screen.fill(teal)
    else:
        screen.fill(bordeaux)
    
    # Disegna la griglia del tabellone
    disegna_griglia(screen, righe, colonne, larghezza_cella, altezza_cella, 65, 100)

    # Disegna i dadi sullo schermo
    for dado in dadi:
        dado.draw()
    
    # 5. Impostazione del pulsante "Tira!" o "Tiri finiti"
    if counter == max_tiri:
        tira_btn_colore = dark_beige
        btn_testo = font_tira.render("Tiri finiti", True, gray) #gray, white o più chiaro lo sfondo?
        btn_pos = [705, 580]
    else:
        tira_btn_colore = beige
        btn_testo = font_tira.render("Tira!", True, gray)
        btn_pos = [760, 580]

    # Disegna il pulsante "Tira!" con il colore e testo aggiornati
    tira_btn = pygame.draw.rect(screen, tira_btn_colore, [700, 550, 250, 100])

    # Mostra il testo del pulsante "Tira!" sopra il pulsante
    screen.blit(btn_testo, btn_pos)

    # Gestore degli eventi Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False  # Esci dal gioco se viene chiusa la finestra
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # 8. Controllo se il pulsante "Tira!" è stato cliccato
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
            
            # 10. Gestione della selezione dei dadi
            if tiro:
                for dado in dadi:
                    dado.seleziona_dadi((mouse_x, mouse_y), dadi)

            # 11. Controllo se è stata cliccata una cella del tabellone
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
                        tiro= False       
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
                        tiro= False
                    print(f"Tabellone 2 aggiornato: {giocatore2.tabellone}")
    
    #scritta del turno corrente
    if turno:
        testo_giocatore1= font_turno.render (f"Turno Giocatore 1", True, white)
        screen.blit(testo_giocatore1, (550,200))
    else:
        testo_giocatore2= font_turno.render (f"Turno giocatore 2", True, white)
        screen.blit(testo_giocatore2, (550,200))
    
    # 12. Mostra i punteggi sul tabellone per entrambi i giocatori
    y1_offset = 110
    y2_offset = 110
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
    screen.blit(totale_text1, (x_pos1, 660))

    totale_punteggi2 = giocatore2.totale
    totale_text2 = font.render(f"{totale_punteggi2}", True, black)
    screen.blit(totale_text2, (x_pos2, 660))
    
    # Aggiornamento dello schermo di gioco
    pygame.display.flip()

# Uscita dal programma Pygame
pygame.quit()

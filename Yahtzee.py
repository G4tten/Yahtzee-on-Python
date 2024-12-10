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

#Caricamento delle immagini dei tiri
immagini_tiri = [
    pygame.image.load("immagini/tiri/tiro_non_fatto.png"),
    pygame.image.load("immagini/tiri/tiro_fatto.png")
]

check_tiro = [False, False, False]

# Ridimensionamento delle immagini dei dadi
resize_immagine = [pygame.transform.scale(img, (100, 100)) for img in immagini_dadi]
resize_immagine_t = [pygame.transform.scale(img, (30,30)) for img in immagini_tiri]

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

suono_select = pygame.mixer.Sound("suoni/selezione.mp3")
suono_deselect = pygame.mixer.Sound("suoni/deselezione.mp3")
suono_select.set_volume(0.3)
suono_deselect.set_volume(0.3)

# Classe per definire il comportamento di un dado
class Dado:
    def __init__(self, x_pos, y_pos, num, selezionato):
        self.x_pos = x_pos  # Posizione X del dado
        self.y_pos = y_pos  # Posizione Y del dado
        self.numero = num  # Numero mostrato dal dado
        self.selezionato = selezionato  #controlla se il dado è stato selezionato o no

    # Metodo per disegnare il dado sullo schermo
    def draw(self):
        screen.blit(resize_immagine[self.numero - 1], (self.x_pos, self.y_pos))
        
        if self.selezionato:
            bordo_dado = pygame.Rect(self.x_pos, self.y_pos, 100, 100)
            pygame.draw.rect(screen, beige, bordo_dado, 10, border_radius=11)

    def seleziona_dadi(self, pos, dadi):
        larghezza_dado = 100
        margine = 20 #margine per ogni dado

        for dado in dadi:
            if dado.x_pos <= pos[0] <= dado.x_pos + larghezza_dado + margine and dado.y_pos <= pos[1] <= dado.y_pos + larghezza_dado:
                if not dado.selezionato:
                    suono_select.play()
                else:
                    suono_deselect.play()
                dado.selezionato = not dado.selezionato

    # Metodo per lanciare il dado e generare un nuovo numero casuale
    def lancio_dadi(self):
        self.numero = random.randint(1, 6)

# Creazione di cinque dadi con posizioni iniziali
dadi = [Dado(550 + i * 120, 350, 6, False) for i in range(5)] 

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

def aggiorna_tiri(check_tiro):
    x_base = 740
    y = 680

    for i in range(len(check_tiro)):
        x = x_base + i * 70

        if check_tiro[i]:
            screen.blit(resize_immagine_t[1], (x,y))
        else:
            screen.blit(resize_immagine_t[0], (x,y))



#########################################################################################
# Inizializzazione delle variabili di gioco
run = True  # Variabile per mantenere attivo il ciclo di gioco
tiro = False  # Stato del tiro dei dadi
counter = 0  # Conteggio dei tiri effettuati
turno = True  # True: Giocatore 1, False: Giocatore 2
schermata= "menu" #menu o gioco (le due fasi)

# oggetto dei giocatori
giocatore1= Giocatore("")
giocatore2= Giocatore ("")

# Variabili di stato
input_attivo1 = False  # Campo attivo per Giocatore 1
input_attivo2 = False  # Campo attivo per Giocatore 2

# pygame.mixer.music.load("suoni/suono_gioco.mp3")  # Caricamento della musica di sottofondo
# pygame.mixer.music.play(-1, 0.0)  # Riproduzione in loop della musica di sottofondo
pygame.mixer.music.set_volume(0.3)  #volume della musica (da 0 a 1)

suono_roll = pygame.mixer.Sound("suoni/rolls.mp3")  # Caricamento del suono per il tiro dei dadi

# Ciclo principale del gioco (game loop)
while run:

    if len(giocatore1.tabellone) == len(combinazioni) - 1 and len(giocatore2.tabellone) == len(combinazioni) - 1:

        if giocatore1.totale > giocatore2.totale:
            screen.fill(teal)
            vittoria = font_turno.render(f"{giocatore1.nome}, hai vinto ! !", True, white)
            screen.blit(vittoria, (300,350))
        elif giocatore2.totale > giocatore1.totale:
            screen.fill(bordeaux)
            vittoria = font_turno.render(f"{giocatore2.nome}, hai vinto ! !", True, white)
            screen.blit(vittoria, (300,350))
        else:
            screen.fill(beige)
            vittoria = font_turno.render("Pareggio ! : (", True, gray)
            screen.blit(vittoria, (400,350))

        pygame.display.flip()
        pygame.time.wait(5000)

        run = False
        break
    
    if schermata== "menu" :

        sfondo = pygame.image.load("immagini/Sfondo.png")
        screen.blit(sfondo, (0, 0))

        # Titolo
        font_grande = pygame.font.Font("font/VCR_OSD_MONO_1.001.ttf", 100)  # Imposta la dimensione del font a 100
        title_text = font_grande.render("Yatzee", True, white)
        screen.blit(title_text, (screen_widht // 2 - title_text.get_width() // 2, 50))

        # Istruzione
        instruction_text = font.render("Inserisci giocatori:", True, white)
        screen.blit(instruction_text, (screen_widht // 2 - instruction_text.get_width() // 2, 180))

        # Rettangoli per i campi di input e il pulsante Play
        rect_giocatore1 = pygame.Rect((screen_widht - 300) // 2 , 250 , 300, 60)
        rect_giocatore2 = pygame.Rect((screen_widht - 300) // 2, 350, 300, 60)
        rect_play = pygame.Rect((screen_widht- 100)//2, 450, 100, 50)

        # Disegna i campi di input
        color_giocatore1 = teal if input_attivo1 else white
        color_giocatore2 = teal if input_attivo2 else white
        pygame.draw.rect(screen, color_giocatore1, rect_giocatore1, 3,8)
        pygame.draw.rect(screen, color_giocatore2, rect_giocatore2, 3,8)

        # Disegna il testo nei campi di input
        text_giocatore1 = font.render(giocatore1.nome, True, white)
        screen.blit(text_giocatore1, (rect_giocatore1.x + 10, rect_giocatore1.y + 10))

        text_giocatore2 = font.render(giocatore2.nome, True, white)
        screen.blit(text_giocatore2, (rect_giocatore2.x + 10, rect_giocatore2.y + 10))
        
        # Disegna il pulsante Play
        pygame.draw.rect(screen, teal, rect_play, 0, 8)
        play_text = font.render("Play", True, white)
        screen.blit(play_text, (rect_play.x + 15, rect_play.y + 10))

            # Gestione degli eventi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Controlla quale campo è stato cliccato
                if rect_giocatore1.collidepoint(event.pos):
                    input_attivo1 = True
                    input_attivo2 = False
                elif rect_giocatore2.collidepoint(event.pos):
                    input_attivo2 = True
                    input_attivo1 = False
                elif rect_play.collidepoint(event.pos):
                    schermata = "gioco"  
                else:
                    input_attivo1 = False
                    input_attivo2 = False

            if event.type == pygame.KEYDOWN:
                # Scrittura nel campo attivo
                if input_attivo1:
                    if event.key == pygame.K_BACKSPACE:
                        giocatore1.nome = giocatore1.nome[:-1]
                    else:
                        giocatore1.nome += event.unicode
                elif input_attivo2:
                    if event.key == pygame.K_BACKSPACE:
                        giocatore2.nome = giocatore2.nome[:-1]
                    else:
                        giocatore2.nome += event.unicode

        # Aggiorna la finestra
        pygame.display.flip()


    elif schermata == "gioco" : 
        # Aggiornamento dello sfondo in base al turno del giocatore
        if turno:
            screen.fill(teal)  # Sfondo per Giocatore 1
        else:
            screen.fill(bordeaux)  # Sfondo per Giocatore 2
        
        # Disegna la griglia del tabellone
        disegna_griglia(screen, righe, colonne, larghezza_cella, altezza_cella, 65, 100)

        # Disegna i dadi sullo schermo
        for dado in dadi:
            dado.draw()  # Metodo draw per mostrare ciascun dado

        aggiorna_tiri(check_tiro)  # Aggiorna lo stato visivo dei tiri effettuati
        
        # Impostazione del pulsante "Tira!" o "Tiri finiti" in base al numero di tiri
        if counter == max_tiri:
            tira_btn_colore = dark_beige  # Colore del pulsante quando i tiri sono finiti
            btn_testo = font_tira.render("Tiri finiti", True, gray)  # Testo del pulsante disabilitato
            btn_pos = [705, 580]  # Posizione del testo
        else:
            tira_btn_colore = beige  # Colore del pulsante attivo
            btn_testo = font_tira.render("Tira!", True, gray)  # Testo del pulsante attivo
            btn_pos = [760, 580]  # Posizione del testo

        # Disegna il pulsante "Tira!" con il colore e testo aggiornati
        tira_btn = pygame.draw.rect(screen, tira_btn_colore, [700, 550, 250, 100])  # Rettangolo del pulsante

        # Mostra il testo del pulsante "Tira!" sopra il pulsante
        screen.blit(btn_testo, btn_pos)

        # Gestore degli eventi Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Evento di uscita
                run = False  # Esci dal gioco se viene chiusa la finestra
            
            if event.type == pygame.MOUSEBUTTONDOWN:  # Evento di clic del mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Ottieni la posizione del mouse
                
                # Controllo se il pulsante "Tira!" è stato cliccato
                if tira_btn.collidepoint(event.pos) and counter < max_tiri:
                    tiro = True  # Avvia il tiro dei dadi
                    counter += 1  # Incrementa il numero di tiri
                    check_tiro[counter - 1] = True  # Aggiorna l'indicatore dei tiri
                    aggiorna_tiri(check_tiro)  # Aggiorna la visualizzazione dei tiri
                    # Lancia i dadi non selezionati
                    for dado in dadi:
                        if not dado.selezionato:
                            dado.lancio_dadi()  # Metodo per lanciare i dadi
                    suono_roll.play()  # Riproduce il suono del tiro

                    # Calcola i punteggi dopo il lancio
                    punteggi = calcola_punteggi(dadi)
                
                # Gestione della selezione dei dadi
                if tiro:
                    for dado in dadi:
                        dado.seleziona_dadi((mouse_x, mouse_y), dadi)  # Metodo per selezionare i dadi

                # Controllo se è stata cliccata una cella del tabellone
                colonna, riga = rileva_clic(mouse_x, mouse_y)  # Determina riga e colonna cliccate
                
                if turno:  # Azioni per il turno del Giocatore 1
                    if colonna is not None and riga is not None:  # Controllo valido
                        print(f"Hai cliccato sulla cella ({riga}, {colonna})")
                        giocatore1.salva_punteggi(riga, punteggi)  # Salva il punteggio per il Giocatore 1
                        turno = not turno  # Cambia turno
                        counter = 0  # Resetta il conteggio dei tiri
                        check_tiro = [False, False, False]  # Resetta i tiri
                        aggiorna_tiri(check_tiro)  # Aggiorna visivamente i tiri
                        for dado in dadi:  # Resetta lo stato dei dadi
                            dado.selezionato = False
                            dado.numero = 6
                            tiro = False       
                        print(f"Tabellone 1 aggiornato: {giocatore1.tabellone}")
                else:  # Azioni per il turno del Giocatore 2
                    if colonna is not None and riga is not None:  # Controllo valido
                        print(f"Hai cliccato sulla cella ({riga}, {colonna})")
                        giocatore2.salva_punteggi(riga, punteggi)  # Salva il punteggio per il Giocatore 2
                        turno = not turno  # Cambia turno
                        counter = 0  # Resetta il conteggio dei tiri
                        check_tiro = [False, False, False]  # Resetta i tiri
                        aggiorna_tiri(check_tiro)  # Aggiorna visivamente i tiri
                        for dado in dadi:  # Resetta lo stato dei dadi
                            dado.selezionato = False
                            dado.numero = 6
                            tiro = False
                        print(f"Tabellone 2 aggiornato: {giocatore2.tabellone}")
        
        # Mostra il turno corrente sullo schermo
        if turno:
            testo_giocatore1 = font_turno.render(f"Turno di : {giocatore1.nome}", True, white)
            screen.blit(testo_giocatore1, (550, 200))  # Testo per il Giocatore 1
        else:
            testo_giocatore2 = font_turno.render(f"Turno di : {giocatore2.nome}", True, white)
            screen.blit(testo_giocatore2, (550, 200))  # Testo per il Giocatore 2
        
        # Mostra i punteggi sul tabellone per entrambi i giocatori
        y1_offset = 110  # Offset verticale per il Giocatore 1
        y2_offset = 110  # Offset verticale per il Giocatore 2
        x_pos1 = 280  # Posizione orizzontale per il Giocatore 1
        x_pos2 = 430  # Posizione orizzontale per il Giocatore 2

        if turno:  # Mostra i punteggi per il turno del Giocatore 1
            for combinazione, punteggio in punteggi.items():
                if combinazione in giocatore1.tabellone:  # Punteggi assegnati
                    testo_punteggio1 = font.render(f"{giocatore1.tabellone[combinazione]}", True, black)
                    screen.blit(testo_punteggio1, (x_pos1, y1_offset))
                else:  # Anteprima dei punteggi non assegnati
                    testo_punteggio1 = font.render(f"{punteggio}", True, gray)
                    screen.blit(testo_punteggio1, (x_pos1, y1_offset))
                y1_offset += 50

                if combinazione in giocatore2.tabellone:  # Mostra punteggi assegnati del Giocatore 2
                    testo_punteggio2 = font.render(f"{giocatore2.tabellone[combinazione]}", True, black)
                    screen.blit(testo_punteggio2, (x_pos2, y2_offset))
                y2_offset += 50

        else:  # Mostra i punteggi per il turno del Giocatore 2
            for combinazione, punteggio in punteggi.items():
                if combinazione in giocatore2.tabellone:  # Punteggi assegnati
                    testo_punteggio2 = font.render(f"{giocatore2.tabellone[combinazione]}", True, black)
                    screen.blit(testo_punteggio2, (x_pos2, y2_offset))
                else:  # Anteprima dei punteggi non assegnati
                    testo_punteggio2 = font.render(f"{punteggio}", True, gray)
                    screen.blit(testo_punteggio2, (x_pos2, y2_offset))
                y2_offset += 50

                if combinazione in giocatore1.tabellone:  # Mostra punteggi assegnati del Giocatore 1
                    testo_punteggio1 = font.render(f"{giocatore1.tabellone[combinazione]}", True, black)
                    screen.blit(testo_punteggio1, (x_pos1, y1_offset))
                y1_offset += 50

        # Calcola e mostra il totale dei punteggi
        totale_punteggi1 = giocatore1.totale
        totale_text1 = font.render(f"{totale_punteggi1}", True, black)
        screen.blit(totale_text1, (x_pos1, 660))  # Mostra il totale del Giocatore 1

        totale_punteggi2 = giocatore2.totale
        totale_text2 = font.render(f"{totale_punteggi2}", True, black)
        screen.blit(totale_text2, (x_pos2, 660))  # Mostra il totale del Giocatore 2
        
        pygame.display.flip()  # Aggiorna la finestra del gioco

# Uscita dal programma Pygame
pygame.quit()

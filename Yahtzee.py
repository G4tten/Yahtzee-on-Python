import random
import pygame

pygame.init()  # Inizializzazione del modulo Pygame

#Schermo
screen_widht = 1200 #larghezza schermo
screen_height = 750 #altezza schermo

# Creazione della finestra di gioco
screen = pygame.display.set_mode((screen_widht, screen_height)) #impostiamo lo schermo con le grandezze precedentemente definite
pygame.display.set_caption("Yahtzee Game")  # Titolo della finestra

# Font
font = pygame.font.Font('font/Casino.ttf', 28) # Imposta la dimensione del font a 28
font_grande = pygame.font.Font('font/Casino.ttf',60) # Imposta la dimensione del font a 60
font_titolo = pygame.font.Font("font/Casino.ttf", 120)  # Imposta la dimensione del font a 120

# Palette di colori da utilizzare nel gioco
teal = (37, 113, 128)
beige = (242, 229, 191)
dark_beige = (194, 183, 153)
red= (191,37,57)
blu= (36,79,131)
# orange = (253, 139, 81)
# dark_orange = (180, 100, 50)
bordeaux = (203, 96, 64)
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
# background = beige  # Colore di sfondo

#Musica di sottofondo
pygame.mixer.music.load("suoni/suono_gioco.mp3")  # Caricamento della musica di sottofondo
pygame.mixer.music.play(-1, 0.0)  # Riproduzione in loop della musica di sottofondo
pygame.mixer.music.set_volume(0.3)  #volume della musica (da 0 a 1)
#Effetti
suono_inizio= pygame.mixer.Sound("suoni/game-start-6104.mp3")
suono_vittoria= pygame.mixer.Sound("suoni/winning-218995.mp3")
suono_roll = pygame.mixer.Sound("suoni/rolls.mp3")  # Caricamento del suono per il tiro dei dadi
suono_selezionepunteggio= pygame.mixer.Sound("suoni/collect-points-190037.mp3")
#Effetto select
suono_select = pygame.mixer.Sound("suoni/selezione.mp3")
suono_select.set_volume(0.3)
#Effetto deselect
suono_deselect = pygame.mixer.Sound("suoni/deselezione.mp3")
suono_deselect.set_volume(0.3)

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

#Caricamento delle immagini dei tiri
immagini_tiri = [
    pygame.image.load("immagini/tiri/tiro_non_fatto.png"),
    pygame.image.load("immagini/tiri/tiro_fatto.png")
]

# Ridimensionamento delle immagini del numero di tiri disponibili
resize_immagine_t = [pygame.transform.scale(img, (30,30)) for img in immagini_tiri]

check_tiro = [False, False, False] #lista per verificare quanti tiri sono stati fatti

###################################################################################################################################################

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

        controllo = True

        #DA RIVEDERE IL CONTROLLO SE è STATA GIA' SALVATA O MENO (magari invece di return si potrebbe impostare una variabile)
        # Controllare che la riga sia valida
        if riga in riga_to_chiave:
            chiave = riga_to_chiave[riga]

            # Aggiungere solo se la chiave non è già presente nel tabellone
            if chiave not in self.tabellone:
                self.tabellone[chiave] = punteggi.get(chiave)  # Preleva il punteggio
                self.totale += punteggi.get(chiave)  # Aggiorna il totale punti
                controllo = True
            else:
                controllo = False

        # Ripulire le combinazioni non selezionate
        for combinazione in punteggi:
            if combinazione not in self.tabellone:
                punteggi[combinazione] = " "

        return self.tabellone, controllo

###################################################################################################################################################

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

################################################################################################################################################### 

# Dimensioni e posizione del tabellone
larghezza_cella = 150
altezza_cella = 50
righe = 12
colonne = 3
offset_x = 65  # Offset orizzontale della griglia
offset_y = 100  # Offset verticale della griglia

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
    
###################################################################################################################################################

# Lista delle combinazioni visualizzate nel tabellone
combinazioni = [
    "Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", 
    "Tris", "Quadris", "Full", "Scala", "Yahtzee", "Totale"
]

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

###################################################################################################################################################

def aggiorna_tiri(check_tiro):
    x_base = 740 #x di partenza
    y = 680 #y fisso

    for i in range(len(check_tiro)):
        x = x_base + i * 70 #aumenta la x di partenza in modo che i puntini siano distanziati equamentre tra loro

        if check_tiro[i]: #se l'elemento i di check tiro è == True, allora...
            screen.blit(resize_immagine_t[1], (x,y)) #... stampa a schermo il puntino verde altrimenti...
        else:
            screen.blit(resize_immagine_t[0], (x,y)) #... se check tiro è == a False stampa a schermo il puntino bianco

#########################################################################################
# Inizializzazione delle variabili di gioco
run = True  # Variabile per mantenere attivo il ciclo di gioco
tiro = False  # Stato del tiro dei dadi
counter = 0  # Conteggio dei tiri effettuati
max_tiri = 3  # Numero massimo di tiri consentiti
turno = True  # True: Giocatore 1, False: Giocatore 2
schermata= "gioco" #menu o gioco (le due fasi)
messaggio_errore = None
inizio_errore = None

# oggetto dei giocatori
giocatore1= Giocatore("")
giocatore2= Giocatore ("")

# Variabili di stato
input_attivo1 = False  # Campo attivo per Giocatore 1
input_attivo2 = False  # Campo attivo per Giocatore 2 

# Ciclo principale del gioco (game loop)
while run:

    if len(giocatore1.tabellone) == len(combinazioni) - 1 and len(giocatore2.tabellone) == len(combinazioni) - 1:

        if giocatore1.totale > giocatore2.totale:
            screen.fill(blu)
            suono_vittoria.play()
            vittoria = font_grande.render(f"{giocatore1.nome}, hai vinto ! !", True, white)
            screen.blit(vittoria, (300,350))
        elif giocatore2.totale > giocatore1.totale:
            screen.fill(red)
            suono_vittoria.play()
            vittoria = font_grande.render(f"{giocatore2.nome}, hai vinto ! !", True, white)
            screen.blit(vittoria, (300,350))
        else:
            screen.fill(beige)
            vittoria = font_grande.render("Pareggio ! : (", True, gray)
            screen.blit(vittoria, (400,350))

        pygame.display.flip()
        pygame.time.wait(5000)

        run = False
        break
    
    if schermata== "menu" :

        # Carica lo sfondo
        sfondo = pygame.image.load("immagini/sfondo.png")
        screen.blit(sfondo, (0, 0))

        # Crea una superficie trasparente per il contenitore
        surface = pygame.Surface((screen_widht, screen_height), pygame.SRCALPHA)  # Supporto trasparenza

        # Rettangoli per i campi di input e il pulsante Play
        rect_contenitore = pygame.Rect((screen_widht - 450) // 2, 200, 450, 350)
        rect_giocatore1 = pygame.Rect((screen_widht - 300) // 2, 280, 300, 60)
        rect_giocatore2 = pygame.Rect((screen_widht - 300) // 2, 360, 300, 60)
        rect_play = pygame.Rect((screen_widht - 120) // 2, 450, 120, 60)

        # Colori
        color_giocatore1 = teal if input_attivo1 else white
        color_giocatore2 = bordeaux if input_attivo2 else white
        color_contenitore = (255,255, 255, 90)  # bianco semi-trasparente

        # Disegna il rettangolo trasparente sulla superficie
        pygame.draw.rect(surface, color_contenitore, rect_contenitore, 0, 8)

        # Blitta la superficie trasparente sullo schermo
        screen.blit(surface, (0, 0))

        # Disegna gli altri rettangoli direttamente sullo schermo
        pygame.draw.rect(screen, color_giocatore1, rect_giocatore1, 0, 8)
        pygame.draw.rect(screen, color_giocatore2, rect_giocatore2, 0, 8)

        # Disegna il titolo
        title_text = font_titolo.render("YAHTZEE", True, white)
        screen.blit(title_text, (screen_widht // 2 - title_text.get_width() // 2, 50))

        # Inserimento dei nomi sottotitolo
        instruction_text = font.render("INSERISCI GIOCATORI:", True, black)
        screen.blit(instruction_text, (screen_widht // 2 - instruction_text.get_width() // 2, 230))

        # Disegna il testo nei campi di input
        text_giocatore1 = font.render(giocatore1.nome, True, black)
        screen.blit(text_giocatore1, (rect_giocatore1.x + 18, rect_giocatore1.y + 15))

        text_giocatore2 = font.render(giocatore2.nome, True, black)
        screen.blit(text_giocatore2, (rect_giocatore2.x + 18, rect_giocatore2.y + 15))
        
        # Disegna il pulsante Play
        pygame.draw.rect(screen, teal, rect_play, 0, 8)
        play_text = font.render("PLAY", True, white)
        screen.blit(play_text, (rect_play.x + 30, rect_play.y + 20))

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
                    suono_inizio.play()
                else:
                    input_attivo1 = False
                    input_attivo2 = False

            if event.type == pygame.KEYDOWN:
                # Scrittura nel campo attivo
                if input_attivo1:
                    if event.key == pygame.K_BACKSPACE:
                        giocatore1.nome = giocatore1.nome[:-1]
                    elif event.key == pygame.K_TAB:  # Passa al campo giocatore 2
                        input_attivo1 = False
                        input_attivo2 = True
                    else:
                        giocatore1.nome += event.unicode
                elif input_attivo2:
                    if event.key == pygame.K_BACKSPACE:
                        giocatore2.nome = giocatore2.nome[:-1]
                    elif event.key == pygame.K_TAB:  # Torna al campo giocatore 1
                        input_attivo2 = False
                        input_attivo1 = True
                    else:
                        giocatore2.nome += event.unicode
                if event.key == pygame.K_RETURN:
                    schermata = "gioco"
                    suono_inizio.play()

        # Aggiorna la finestra
        pygame.display.flip()
    
    elif schermata == "opzioni":
        
        # Carica lo sfondo
        sfondo = pygame.image.load("immagini/sfondo.png")
        screen.blit(sfondo, (0, 0))
         
    elif schermata == "gioco" : 
        # Aggiornamento dello sfondo in base al turno del giocatore
        if turno:
            # Carica lo sfondo 1
            sfondo = pygame.image.load("immagini/sfondo_giocatore1.png")
            screen.blit(sfondo, (0, 0))
        else:
            # Carica lo sfondo 2
            sfondo = pygame.image.load("immagini/sfondo_giocatore2.png")
            screen.blit(sfondo, (0, 0))
   
        # Disegna la griglia del tabellone
        disegna_griglia(screen, righe, colonne, larghezza_cella, altezza_cella, 65, 100)

        # Disegna i dadi sullo schermo
        for dado in dadi:
            dado.draw()  # Metodo draw per mostrare ciascun dado

        aggiorna_tiri(check_tiro)  # Aggiorna lo stato visivo dei tiri effettuati
        
        # Impostazione del pulsante "Tira!" o "Tiri finiti" in base al numero di tiri
        if counter == max_tiri:
            tira_btn_colore = dark_beige  # Colore del pulsante quando i tiri sono finiti
            btn_testo = font_grande.render("Tiri finiti", True, gray)  # Testo del pulsante disabilitato
            btn_pos = [705, 580]  # Posizione del testo
        else:
            tira_btn_colore = beige  # Colore del pulsante attivo
            btn_testo = font_grande.render("Tira!", True, gray)  # Testo del pulsante attivo
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
                        _, controllo = giocatore1.salva_punteggi(riga,punteggi)
                        if controllo:
                            if giocatore1.salva_punteggi(riga, punteggi):  # Salva il punteggio per il Giocatore 1
                                suono_selezionepunteggio.play()
                                turno = not turno  # Cambia turno
                                counter = 0  # Resetta il conteggio dei tiri
                                check_tiro = [False, False, False]  # Resetta i tiri
                                aggiorna_tiri(check_tiro)  # Aggiorna visivamente i tiri
                                for dado in dadi:  # Resetta lo stato dei dadi
                                    dado.selezionato = False
                                    dado.numero = 6
                                    tiro = False   
                                print(f"Tabellone 1 aggiornato: {giocatore1.tabellone}")
                                print("Controllo dopo la chiamata della funzione: ", controllo)
                        else:
                            messaggio_errore = "Punteggio gia' salvato!"
                            inizio_errore = pygame.time.get_ticks()
                else:  # Azioni per il turno del Giocatore 2
                    if colonna is not None and riga is not None:  # Controllo valido
                        print(f"Hai cliccato sulla cella ({riga}, {colonna})")
                        _, controllo = giocatore2.salva_punteggi(riga,punteggi)
                        if controllo:
                            giocatore2.salva_punteggi(riga, punteggi)  # Salva il punteggio per il Giocatore 2
                            suono_selezionepunteggio.play()
                            turno = not turno  # Cambia turno
                            counter = 0  # Resetta il conteggio dei tiri
                            check_tiro = [False, False, False]  # Resetta i tiri
                            aggiorna_tiri(check_tiro)  # Aggiorna visivamente i tiri
                            for dado in dadi:  # Resetta lo stato dei dadi
                                dado.selezionato = False
                                dado.numero = 6
                                tiro = False                          
                            print(f"Tabellone 2 aggiornato: {giocatore2.tabellone}")
                    else:
                        messaggio_errore = "Punteggio gia' salvato!"
                        inizio_errore = pygame.time.get_ticks()

        if messaggio_errore:
            tempo_trascorso = pygame.time.get_ticks() - inizio_errore
            if tempo_trascorso < 3000:
                alpha = max(0, 255 - int((tempo_trascorso / 3000) * 255))
                superfice_errore = font.render(messaggio_errore, True, beige)
                superfice_errore.set_alpha(alpha)
                screen.blit(superfice_errore, (10,20))
            else:
                messaggio_errore = None
        
        # Mostra il turno corrente sullo schermo
        if turno:
            testo_giocatore1 = font_grande.render(f"TURNO DI : {giocatore1.nome}", True, white)
            screen.blit(testo_giocatore1, (550, 200))  # Testo per il Giocatore 1
        else:
            testo_giocatore2 = font_grande.render(f"TURNO DI : {giocatore2.nome}", True, white)
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

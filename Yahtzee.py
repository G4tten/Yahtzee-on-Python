import random
import pygame

pygame.init()
 
screen_width = 600 
screen_height = 775 # 

screen = pygame.display.set_mode((screen_width, screen_height)) #creazione della finestra di gioco
pygame.display.set_caption("Yahtzee Game")
font = pygame.font.Font('font/casino.ttf', 28) #GRANDEZZA E STILE FONT DA SISTEMARE!!

#Palette di colori che pensavo di usare:
teal = (37, 113, 128)
beige = (242, 229, 191)
orange = (253, 139, 81)
dark_orange = (180, 100, 50)
bordeaux = (203, 96, 64)
white = (255, 255, 255)
black = (0,0,0)


background = beige

immagini_dadi = [pygame.image.load("immagini/dadi/1.png"), pygame.image.load("immagini/dadi/2.png"), pygame.image.load("immagini/dadi/3.png"), pygame.image.load("immagini/dadi/4.png"), pygame.image.load("immagini/dadi/5.png"), pygame.image.load("immagini/dadi/6.png")]

resize_immagine = [pygame.transform.scale(img, (100,100)) for img in immagini_dadi]

size_immagine = [img.get_size() for img in resize_immagine]

tiro = False
counter = 0
max_tiri = 3

class Dado:

    def __init__(self, x_pos, y_pos, num, key):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.numero = num
        self.key = key
        # self.dado = ''

    def draw(self):
        if self.numero == 1:
            screen.blit(resize_immagine[0], (self.x_pos, self.y_pos))
        
        if self.numero == 2:
            screen.blit(resize_immagine[1], (self.x_pos, self.y_pos))
        
        if self.numero == 3:
            screen.blit(resize_immagine[2], (self.x_pos, self.y_pos))

        if self.numero == 4:
            screen.blit(resize_immagine[3], (self.x_pos, self.y_pos))

        if self.numero == 5:
            screen.blit(resize_immagine[4], (self.x_pos, self.y_pos))
        
        if self.numero == 6:
            screen.blit(resize_immagine[5], (self.x_pos, self.y_pos))


    def lancio_dadi(self):
        self.numero = random.randint(1, 6)

dado1 = Dado(10, 50, 1, 0)
dado2 = Dado(130, 50, 2, 1)
dado3 = Dado(250, 50, 3, 2)
dado4 = Dado(370, 50, 4, 3)
dado5 = Dado(490, 50, 5, 4)

dadi = [dado1, dado2, dado3, dado4, dado5]

btn_testo = font.render("Tira!", True, white)

fine_btn = pygame.draw.rect(screen, bordeaux, [300, 180, 280, 50])

tira_btn_colore = orange

# Crea il font 
font = pygame.font.Font('font/casino.ttf', 36)

# Lista delle combinazioni da visualizzare nella colonna di sinistra
combinazioni = [
    "Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", 
    "Tris", "Quadris", "Full", "Scala", "Yahtzee", "Totale"
]

def disegna_griglia (schermo, righe, colonne, larghezza_cella, altezza_cella, x_inizio, y_inizio):
    colore_griglia= (0,0,0)

    sfondo_griglia = pygame.Rect(x_inizio, y_inizio, colonne * larghezza_cella, righe * altezza_cella)
    pygame.draw.rect(schermo, white, sfondo_griglia)


    for riga in range(righe):
        for colonna in range(colonne):
            rettangolo= pygame.Rect(x_inizio+ colonna *larghezza_cella, y_inizio + riga *altezza_cella, larghezza_cella, altezza_cella)
            pygame.draw.rect (schermo, colore_griglia, rettangolo, 3)
    
     # Aggiungi il testo delle combinazioni nella prima colonna
    for indice, combinazione in enumerate(combinazioni):
        if indice < righe:  # Assicurati di non eccedere il numero di righe
            testo = font.render(combinazione, True, black)  # Renderizza il testo
            schermo.blit(testo, (x_inizio + 10, y_inizio + indice * altezza_cella + 10))  # Posiziona il testo con un piccolo margine

larghezza_cella = 150
altezza_cella= 50
righe = 12
colonne=3
offset_x= 65 #indica da dove parte il tabellone da sinistra
offset_y=280 #indica da dove parte il tabellone dall'alto

#click sulla casella
def rileva_clic(x,y):
    if offset_x <= x <= offset_x + colonne * larghezza_cella and \
       offset_y <= y <= offset_y + righe * altezza_cella:
        
        x_relativo = x - offset_x
        y_relativo = y - offset_y
        
        # Calcola la colonna e la riga cliccate
        colonna = x_relativo // larghezza_cella
        riga = y_relativo // altezza_cella
        
        #Aggiorniamo poi per il salvataggio dei punteggi
        print(f'Cella cliccata: Colonna {colonna}, Riga {riga}')
        return colonna, riga
    
    else:
        print('Clic fuori dalla griglia')
        return None, None





#########################################################################################
run = True
while run: #game loop

    screen.fill(background)
    disegna_griglia(screen, righe, colonne, larghezza_cella, altezza_cella, 65, 280)


    for dado in dadi:
        dado.draw()

    if counter >= max_tiri:
        tira_btn_colore = dark_orange
        btn_testo = font.render("Tiri finiti", True, white)
    else :
        tira_btn_colore = orange
        btn_testo = font.render("Tira!", True, white)

    if counter == max_tiri:
        fine_btn = pygame.draw.rect(screen, bordeaux, [330, 180, 160, 50])

    tira_btn = pygame.draw.rect(screen, tira_btn_colore, [150, 180, 160, 50]) #MISURE DA SISTEMARE!!

    screen.blit(btn_testo, [155, 190]) #MISURE DA SISTEMARE!!

    for event in pygame.event.get(): #gestore di eventi
        if event.type == pygame.QUIT: #Quando viene cliccata la x della finestra il gioco si chiude (fondamentale per uscire dal ciclo infinito)
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if tira_btn.collidepoint(event.pos) and counter < max_tiri:
                tiro = True
                counter = counter + 1
            if fine_btn.collidepoint(event.pos) and counter == max_tiri:
                counter = 0

            colonna, riga = rileva_clic(mouse_x,mouse_y)
           
            if colonna is not None and riga is not None:
                print(f"Hai cliccato sulla cella ({riga}, {colonna})")

    if tiro:
        for dado in dadi:
            dado.lancio_dadi()
            tiro = False

    pygame.display.flip() #per aggiornare lo schermo

pygame.quit() #Termina il programma
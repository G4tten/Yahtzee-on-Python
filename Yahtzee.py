import random
import pygame

pygame.init()
 
screen_width = 600; 
screen_height = 750; 

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

background = beige

immagini_dadi = [pygame.image.load("immagini/dadi/1.png"), pygame.image.load("immagini/dadi/2.png"), pygame.image.load("immagini/dadi/3.png"), pygame.image.load("immagini/dadi/4.png"), pygame.image.load("immagini/dadi/5.png"), pygame.image.load("immagini/dadi/6.png")]

resize_immagine = [pygame.transform.scale(img, (100,100)) for img in immagini_dadi]

size_immagine = [img.get_size() for img in resize_immagine]

# print(f"Dimesioni dell'immaigine: {size_immagine}")

#Le istruzioni che seguono non verranno eseguite sulla finestra di gioco ma sul terminale di Visual Studio

# class giocatore:

#     def __init__(self, username=None):
#             if username is None :
#                 self.username= input("Inserisci il tuo username: ")
#             else:
#                 self.username = username

#             self.punteggio = 0
#             self.scheda= {
#                "Uno" : 0,
#                "Due" : 0, 
#                "Tre" : 0, 
#                "Quattro" : 0,
#                "Cinque" : 0,
#                "Sei" : 0, 
#                "Tris" :0,
#                "Quadris" : 0,
#                "Full" : 0,
#                "Scala" : 0,
#                "Yahtzee":0
#             }

#     def mostra_punteggio(self):
#         print(f"Scheda punteggio del giocatore {self.username}:")
#         for categoria, punteggio in self.scheda.items():
#             print(f"{categoria}: {punteggio}")


################################################################################jk

# giocatore1= giocatore()
# print (f"Il nome del giocatore 1 é {giocatore1.username}")
# giocatore1.mostra_punteggio()

# giocatore2= giocatore()
# print (f"Il nome del giocatore 1 é {giocatore2.username}")
# giocatore2.mostra_punteggio()

################################################################################

#Classe dado, contiene gli attributi di valore e la funzione del lancio dadi

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

tira_btn_colore = orange

###############################################################################

# class Game:
#     def __init__(self, giocatori):
#         self.giocatori = giocatori #lista di oggetti giocatori
#         self.dadi= [Dado() in range (5)]

run = True
while run: #game loop

    screen.fill(background)

    for dado in dadi:
        dado.draw()

    if counter >= max_tiri:
        tira_btn_colore = dark_orange
        btn_testo = font.render("Tiri finiti", True, white)
    else :
        tira_btn_colore = orange
        btn_testo = font.render("Tira!", True, white)

    tira_btn = pygame.draw.rect(screen, tira_btn_colore, [150, 180, 280, 50]) #MISURE DA SISTEMARE!!

    screen.blit(btn_testo, [155, 190]) #MISURE DA SISTEMARE!!

    for event in pygame.event.get(): #gestore di eventi
        if event.type == pygame.QUIT: #Quando viene cliccata la x della finestra il gioco si chiude (fondamentale per uscire dal ciclo infinito)
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if tira_btn.collidepoint(event.pos) and counter < max_tiri:
                tiro = True
                counter = counter + 1

    if tiro:
        for dado in dadi:
            dado.lancio_dadi()
            tiro = False

    pygame.display.flip() #per aggiornare lo schermo

pygame.quit() #Termina il programma
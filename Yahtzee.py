import random
import pygame

pygame.init()
 
screen_width = 600; 
screen_height = 800; 

screen = pygame.display.set_mode((screen_width, screen_height)) #creazione della finestra di gioco
pygame.display.set_caption("Yahtzee Game")

#Palette di colori che pensavo di usare:
#Teal -> rgb(37, 113, 128)
#Beige -> rgb(242, 229, 191)
#Orange -> rgb(253, 139, 81)
#Bordeaux -> rgb(203, 96, 64)

background = (242, 229, 191)

immagini_dadi = [pygame.image.load("immagini/dadi/1.png"), pygame.image.load("immagini/dadi/2.png"), pygame.image.load("immagini/dadi/3.png"), pygame.image.load("immagini/dadi/4.png"), pygame.image.load("immagini/dadi/5.png"), pygame.image.load("immagini/dadi/6.png")]

resize_immagine = [pygame.transform.scale(img, (80,80)) for img in immagini_dadi]

size_immagine = [img.get_size() for img in resize_immagine]

print(f"Dimesioni dell'immaigine: {size_immagine}")

run = True
while run: #game loop

    for event in pygame.event.get(): #gestore di eventi
        if event.type == pygame.QUIT: #Quando viene cliccata la x della finestra il gioco si chiude (fondamentale per uscire dal ciclo infinito)
            run = False
    
    screen.fill(background)

    pygame.display.flip() #per aggiornare lo schermo

pygame.quit() #Termina il programma

#Le istruzioni che seguono non verranno eseguite sulla finestra di gioco ma sul terminale di Visual Studio

class giocatore:

    def __init__(self, username=None):
            if username is None :
                self.username= input("Inserisci il tuo username: ")
            else:
                self.username = username

            self.punteggio = 0
            self.scheda= {
               "Uno" : 0,
               "Due" : 0, 
               "Tre" : 0, 
               "Quattro" : 0,
               "Cinque" : 0,
               "Sei" : 0, 
               "Tris" :0,
               "Quadris" : 0,
               "Full" : 0,
               "Scala" : 0,
               "Yahtzee":0
            }

    def mostra_punteggio(self):
        print(f"Scheda punteggio del giocatore {self.username}:")
        for categoria, punteggio in self.scheda.items():
            print(f"{categoria}: {punteggio}")


################################################################################jk

giocatore1= giocatore()
print (f"Il nome del giocatore 1 é {giocatore1.username}")
giocatore1.mostra_punteggio()

giocatore2= giocatore()
print (f"Il nome del giocatore 1 é {giocatore2.username}")
giocatore2.mostra_punteggio()

################################################################################

#Classe dado, contiene gli attributi di valore e la funzione del lancio dadi

class Dado:

    def __init__(self):
        self.valore= 0

    def lancio_dadi(self):
        self.valore= random.randint(1,6)
        return self.valore

###############################################################################

class Game:
    def __init__(self, giocatori):
        self.giocatori = giocatori #lista di oggetti giocatori
        self.dadi= [Dado() in range (5)]



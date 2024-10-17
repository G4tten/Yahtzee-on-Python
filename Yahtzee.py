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

immagini_dadi = [pygame.image.load("immagini/dadi/1.png"), pygame.image.load("immagini/dadi/2.png")]

resize_immagine = pygame.transform.scale(immagine, (100,100))

size_immagine = immagine.get_size()

print(f"Dimesioni dell'immaigine: {size_immagine}")

run = True
while run: #game loop

    for event in pygame.event.get(): #gestore di eventi
        if event.type == pygame.QUIT: #Quando viene cliccata la x della finestra il gioco si chiude (fondamentale per uscire dal ciclo infinito)
            run = False
    
    screen.fill(background)

    screen.blit(resize_immagine, (100,100))

    pygame.display.flip() #per aggiornare lo schermo

pygame.quit() #Termina il programma

#Le istruzioni che seguono non verranno eseguite sulla finestra di gioco ma sul terminale di Visual Studio

class giocatore:

    def __init__(self, username, punteggio, scheda):
            self.username = username

            # tabellone con categorie
            # punteggio totale del giocatore


giocatore1 = input("Inserire il nome del giocatore1: ")

print(f"Giocatore1: {giocatore1}")

################################################################################

#Classe dado, contiene gli attributi di valore e la funzione del lancio dadi

class Dado:

    def __init__(self):
        self.valore= 0

    def lancio_dadi(self):
        self.valore= random.randint(1,6)
        return self.valore
    
#Lancio dei dadi simulato, dopo lo rivediamo !

dado1= Dado()
dado2= Dado()
dado3= Dado()
dado4= Dado()
dado5= Dado()
print (dado1.lancio_dadi())
print (dado2.lancio_dadi())
print (dado3.lancio_dadi())
print (dado4.lancio_dadi())
print (dado5.lancio_dadi())

###############################################################################


import random
import pygame

pygame.init()
 
screen_width = 800; 
screen_height = 600; 

screen = pygame.display.set_mode((screen_width, screen_height)) #creazione della finestra di gioco

#Le istruzioni che seguono non verranno eseguite sulla finestra di gioco ma sul terminale di Visual Studio
class giocatore:

    def __init__(self, username, punteggio, scheda):
        self.username = username

        #tabellone con categorie
        #punteggio totale del giocatore


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

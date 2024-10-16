import random
import pygame

pygame.init()
 
screen_width = 800; 
screen_height = 600; 

screen = pygame.display.set_mode((screen_width, screen_height)) #creazione della finestra di gioco

#Le istruzioni che seguono non verranno eseguite sulla finestra di gioco ma sul terminale di Visual Studio
class giocatore:

    def __init__(self, username):
        self.username = username
        #tabellone con categorie
        #punteggio totale del giocatore


giocatore1 = input("Inserire il nome del giocatore1: ")

print(f"Giocatore1: {giocatore1}")
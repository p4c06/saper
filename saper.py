from random import randint
from itertools import product, chain
from time import time, sleep
import pygame

def gen_sasiedzi(i, j):
    d = [-1, 0, 1]
    sasiedzi = []
    for a, b in product(d, d):
        if i+a in range(0, poziom) and j+b in range(0, poziom):
            sasiedzi += [(i+a, j+b)]

    return sasiedzi

def print_game():
    print("\033[H\033[Jczas", int(time()-start), "miny:", miny)
    print(" ", *[f"{chr(65+i)}" for i in range(poziom)])
    for i in range(poziom):
        print(f"{chr(65+i)}", end = " ")
        for j in range(poziom):
            if (maska[i][j] == 1):
                print(".", end = " ")
            elif (maska[i][j] == -1):
                print("x", end = " ")
            elif (plansza[i][j] == 0):
                print(" ", end = " ")
            else:
                print(plansza[i][j], end = " ")
        print()

def show_game():
    global screen, start, miny
    for i in range(poziom):
        for j in range(poziom):
            maskaij = pygame.image.load(f"maski/{maska[i][j]}.png")
            planszaij = pygame.image.load(f"pola/{plansza[i][j]}.png")
            screen.blit(planszaij, (i*50, j*50))
            screen.blit(maskaij, (i*50, j*50))

    font = pygame.font.Font(pygame.font.get_default_font(), 14)
    text_surface = font.render(f"czas: {int(time()-start)}, pozostałe miny: {miny}",
                               True,
                                (0, 0, 0))
    screen.blit(text_surface, dest=(0,50*poziom))


def flaguj(i, j):
    global miny
    maska[i][j] = -maska[i][j]
    miny += maska[i][j]

def DFS(i, j):
    global odw
    odw[i][j] = True
    if (plansza[i][j] == -1 or maska[i][j] == -1):
        return
    maska[i][j] = 0
    if (plansza[i][j] == 0):
        for (a, b) in gen_sasiedzi(i, j):
            if (not odw[a][b]):
                DFS(a, b)

def zgadnij(i, j):
    global odw, przegrana, wygrana
    odw = [[0 for i in range(poziom)] for i in range(poziom)]

    if (plansza[i][j] == -1):
        przegrana = True        
    elif (plansza[i][j] == 0):
        DFS(i, j)
    
    maska[i][j] = 0
    
    maska2 = [*chain(*maska)]
    if maska2.count(-1) + maska2.count(1) == mina[n]:
        wygrana= True
        for i in range(poziom):
            for j in range(poziom):
                if (maska[i][j] in [-1, 1]):
                    maska[i][j] = -2

def gen_plansza(i, j):
    global plansza, miny, poziom

    t = 0
    while t < miny:
        a, b = randint(0, poziom-1), randint(0, poziom-1)
        if (plansza[a][b] == -1 or (a, b) in gen_sasiedzi(i, j)):
            continue
        plansza[a][b] = -1
        t += 1

    for a in range(poziom):
        for b in range(poziom):
            if (plansza[a][b] == -1):
                continue

            for c, d in gen_sasiedzi(a, b):
                plansza[a][b] += plansza[c][d] == -1

def znl(znak):
    return ord(znak) - ord('A')

poziomy = {"1": 10, "2": 16, "3": 22}
mina = {"1": 10, "2": 40, "3": 99}

n = input("Wybierz poziom od 1 do 3: ")
poziom = poziomy[n]
miny = mina[n]

plansza = [[0 for i in range(poziom)] for i in range(poziom)]
maska = [[1 for i in range(poziom)] for i in range(poziom)]
odw = [[0 for i in range(poziom)] for i in range(poziom)]

przegrana, wygrana, zaczete = False, False, False
start = time()


pygame.init()

screen = pygame.display.set_mode((poziom * 50 , poziom * 50+20))
pygame.font.init()

clock = pygame.time.Clock()
pauza = 0
while True:
    if (wygrana or przegrana):
        
        if (pauza > 5):
            pygame.quit()
            break
        else:
            pauza+=1
    else:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                wiersz, kol = (pos[0]-10)//50, (pos[1]-10)//50
                if (event.button == 1):
                
                    
                    if (not zaczete):
                        gen_plansza(wiersz, kol)
                        zaczete = True
                    zgadnij(wiersz, kol)
                else :
                    flaguj(wiersz, kol)


        screen.fill("green")
        
        show_game()
        pygame.display.flip()
        pygame.display.update()
   
    clock.tick(5)       

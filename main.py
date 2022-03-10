import pygame
import pygame.midi

from algorithm import algorithm
from utils import make_grid, draw, get_clicked_pos

WIDTH = 800
# wymiary ekranu
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Alogrytm przeszukiwania grafu A*")


def main(win, width):
    ROWS = 40       # liczba wierzcholkow na wiersz
    grid = make_grid(ROWS, width)    #tworzymy plansze

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:    #wylaczenie programu
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT        kliknecie mysza
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:    #pierwsze klikniecie to start
                    start = spot
                    start.make_start()

                elif not end and spot != start: # drugie kliknecie to koniec
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:     # nastepne tworza barierem
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # prawy myszki
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()                               #resetuje kolory
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)      #uzupelnia liste sasiadow dla kazdego elementu

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)    #wywoluje algorytm A*

                if event.key == pygame.K_r:  # resteujmy program klawiszem r
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)

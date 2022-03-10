from queue import PriorityQueue

import pygame


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0  # licznik przejsc
    open_set = PriorityQueue()  # lista wierzcholkow
    open_set.put((0, count, start))  # pierwszy to nasz f_score, drugi to liczba przjesc algorytmu, lokalizacja
    came_from = {}  # zawiera informacje z ktorego wierzcholka przyszlismy
    g_score = {spot: float("inf") for row in grid for spot in row}  # ustawiamy g score dla kazdego wierzcholka
    g_score[start] = 0  # na inf
    f_score = {spot: float("inf") for row in grid for spot in row}  # podobnie jak u gory
    f_score[start] = h(start.get_pos(), end.get_pos())  # wyliczamy heurystyke dla punktu startowego

    open_set_hash = {start}  # PriorityQueue nie posiada funkcji mowiacej nam czy wierzcholek znajduje sie
    # w kolejce.
    while not open_set.empty():  # jesli zbior stanie sie pusty oznacza to ze sciezka nie istnieje
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # wyjscie z algorytmu

        current = open_set.get()[2]  # 2 poniewaz pobieram lokalizacje wczesniejszczego wierzcholka
        open_set_hash.remove(current)

        if current == end:  # Jesli zanleziony wierzcholek jest szukanym koncem
            print("troololo")
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:  # rozwazamy wszystkich sasiadow aktualnego wierzcholka
            temp_g_score = g_score[current] + 1  # zwiekszamy wartosc funkcji o wagę trasy ( 1 ).

            if temp_g_score < g_score[neighbor]:  # jesli wartosc funkcji g jest mniejsza niz sasiada
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score  #
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:  # jesli nie odwiedzilismy wierzcholka
                    count += 1  # zwiekszamy przejscie
                    open_set.put((f_score[neighbor], count, neighbor))  # dodajemy wierzcholek wraz z danymi
                    open_set_hash.add(neighbor)  # dodajemy ten sam wierzcholek do naszego sasiada
                    neighbor.make_open()  # zmieniamy kolor na zieloy (aktywny )

        draw()  # koloruje kwadarty po przejsciu

        if current != start:  # po odwiedzeniu wszsytkich sasiadow zmieniamy
            current.make_closed()  # aktualny wierzcholek na zamkniety.

    return False

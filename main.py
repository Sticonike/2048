import pygame
import math
import random

pygame.init()

screen_size = 600  # double coordonnée mais la fenêtre doit toujours être carrée donc pas besoin de duppliquer
game_difficulty = 4  # nombre de carrés par côté (4, 5, 6)

screen = pygame.display.set_mode((screen_size, screen_size))  # affichage

grid = [[0] * game_difficulty for _ in range(game_difficulty)]  # création de la grille
screen_border = 50
squares_size = (screen_size - screen_border * 2) / game_difficulty

squares_colors = {
    2: (227, 217, 202),
    4: (255, 179, 64),
    8: (242, 125, 46),
    16: (201, 69, 32),
    32: (145, 27, 19),
    64: (184, 26, 73),
    128: (217, 28, 116),
    256: (204, 80, 179),
    512: (64, 18, 163),
    1024: (44, 45, 145),
    2048: (69, 161, 237)
}


def check_square(x, y, direction):  # pour vérifier si le carré à dépacer est en dehors de la grille
    if direction == "S" and y + 1 >= game_difficulty:
        return False
    if direction == "N" and y - 1 < 0:
        return False
    if direction == "E" and x + 1 >= game_difficulty:
        return False
    if direction == "O" and x - 1 < 0:
        return False
    else:
        return True


def move(direction):  # direction : N, S, E, O
    for i in range(game_difficulty):
        for j in range(game_difficulty):
            if grid[i][j] > 0:
                x = i
                y = j
                value = grid[i][j]
                while check_square(x, y, direction):
                    if direction == "N":  # demande s'il y a un carré devant avant de le déplacer
                        if grid[x][y - 1] == 0:  # mouvement
                            grid[x][y] = 0
                            y -= 1
                        elif grid[x][y - 1] == grid[x][y]:  # fusion
                            value = grid[x][y] * 2
                            grid[x][y] = 0
                            y -= 1
                        else:  # pour quand deux carrés fusionnent pas et que que ça fait une boucle infinie
                            break
                    elif direction == "S":
                        if grid[x][y + 1] == 0:  # mouvement
                            grid[x][y] = 0
                            y += 1
                        elif grid[x][y + 1] == grid[x][y]:  # fusion
                            value = grid[x][y] * 2
                            grid[x][y] = 0
                            y += 1
                        else:  # pour quand deux carrés fusionnent pas et que que ça fait une boucle infinie
                            break
                    elif direction == "E":
                        if grid[x + 1][y] == 0:  # mouvement
                            grid[x][y] = 0
                            x += 1
                        elif grid[x + 1][y] == grid[x][y]:  # fusion
                            value = grid[x][y] * 2
                            grid[x][y] = 0
                            x += 1
                        else:  # pour quand deux carrés fusionnent pas et que que ça fait une boucle infinie
                            break
                    elif direction == "O":  # mouvement
                        if grid[x - 1][y] == 0:
                            grid[x][y] = 0
                            x -= 1
                        elif grid[x - 1][y] == grid[x][y]:  # fusion
                            value = grid[x][y] * 2
                            grid[x][y] = 0
                            x -= 1
                        else:  # pour quand deux carrés fusionnent pas et que que ça fait une boucle infinie
                            break
                    grid[x][y] = value

    sideways_classification = []
    if direction == "N":
        for i in range(4)[::-1]:  # compte à l'envers
            is_full = True  # part du principe que la ligne est pleine, puis modifie en fonction
            square_line = []
            for j in range(4):
                if grid[i][j] == 0:
                    square_line.append([j, i])
                    is_full = False
            if not is_full:
                sideways_classification.append(square_line)
    elif direction == "S":
        for i in range(4):  # compte à l'endroit
            is_full = True  # part du principe que la ligne est pleine, puis modifie en fonction
            square_line = []
            for j in range(4):
                if grid[i][j] == 0:
                    square_line.append([j, i])
                    is_full = False
            if not is_full:
                sideways_classification.append(square_line)
    elif direction == "E":
        for i in range(4):  # compte à l'endroit
            is_full = True  # part du principe que la ligne est pleine, puis modifie en fonction
            square_line = []
            for j in range(4):
                if grid[j][i] == 0:  # i et j sont échangés parce que on bouge horizontalement contrairement à avant
                    square_line.append([i, j])
                    is_full = False
            if not is_full:
                sideways_classification.append(square_line)
    elif direction == "O":
        for i in range(4)[::-1]:  # compte à l'envers
            is_full = True  # part du principe que la ligne est pleine, puis modifie en fonction
            square_line = []
            for j in range(4):
                if grid[i][j] == 0:  # i et j sont échangés parce que on bouge horizontalement contrairement à avant
                    square_line.append([i, j])
                    is_full = False
            if not is_full:
                sideways_classification.append(square_line)

    random_created_square = random.choice(sideways_classification[0])
    grid[random_created_square[0]][random_created_square[1]] = 2


running = True  # boucle de jeu
playing = False  # pour recommencer une partie
while running:

    screen.fill("lightgray")
    pygame.draw.rect(screen, (227, 179, 111),
                     (screen_border - 2, screen_border - 2, screen_size - screen_border * 2 + 4,
                      screen_size - screen_border * 2 + 4))  # carré de jeu
    pygame.draw.rect(screen, (128, 123, 116),
                     (screen_border - 2, screen_border - 2, screen_size - screen_border * 2 + 4,
                      screen_size - screen_border * 2 + 4), 3)  # bordure

    for event in pygame.event.get():  # events
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                if not playing:
                    playing = True
                    rand_co = (random.randint(0, 3), random.randint(0, 3))  # création du premier carré de début
                    grid[rand_co[0]][rand_co[1]] = 2
            elif pygame.key.get_pressed()[pygame.K_UP]:
                if playing:
                    move("N")

            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                if playing:
                    move("S")

            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                if playing:
                    move("E")

            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                if playing:
                    move("O")

            # print(grid)

    if playing:  # placage des carrés
        for i in range(game_difficulty):
            for j in range(game_difficulty):
                if grid[i][j] > 0:
                    square_value = grid[i][j]

                    pygame.draw.rect(screen, squares_colors.get(square_value), (i * squares_size + screen_border,
                                                                                j * squares_size + screen_border,
                                                                                squares_size, squares_size),
                                     border_radius=4)

                    font = pygame.font.SysFont('Calibri bold', 50)  # texte du carré
                    number = font.render(str(grid[i][j]), True, (56, 55, 52))
                    textRect = number.get_rect()  # rectangle autour du numéro
                    textRect.center = (i * squares_size + screen_border + squares_size / 2,
                                       j * squares_size + screen_border + squares_size / 2)  # coordonnées du rectangle
                    screen.blit(number, textRect)  # affichage du texte + ses coordonnées

    pygame.display.update()

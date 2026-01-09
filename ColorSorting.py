import copy
import random
import pygame

pygame.init()

WIDTH = 550
HEIGHT = 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Water Sort PyGame')
font = pygame.font.Font('freesansbold.ttf', 24)
fps = 60
timer = pygame.time.Clock()

color_choices = [
    'crimson', 'orange', 'light blue', 'magenta',
    'spring green', 'hotpink', 'purple', 'dark blue',
    'brown', 'dark green', 'yellow', 'white'
]

initial_colors = []
new_game = True
selected = False
tube_rects = []
select_rect = 100
win = False
previous_state = []

def generate_start():
    tubes_number = random.randint(8, 10)
    tubes_colors = []
    available_colors = []

    for i in range(tubes_number):
        tubes_colors.append([])
        if i < tubes_number - 2:
            for _ in range(4):
                available_colors.append(i)

    for i in range(tubes_number - 2):
        for _ in range(4):
            color = random.choice(available_colors)
            tubes_colors[i].append(color)
            available_colors.remove(color)

    return tubes_number, tubes_colors

def draw_tubes(tubes_num, tube_cols):
    tube_boxes = []

    if tubes_num % 2 == 0:
        tubes_per_row = tubes_num // 2
        odd = False
    else:
        tubes_per_row = tubes_num // 2 + 1
        odd = True

    spacing = WIDTH / tubes_per_row

    for i in range(tubes_per_row):
        for j in range(len(tube_cols[i])):
            pygame.draw.rect(
                screen,
                color_choices[tube_cols[i][j]],
                [5 + spacing * i, 200 - (50 * j), 65, 50],
                0,
                7
            )
        box = pygame.draw.rect(screen, 'white', [5 + spacing * i, 50, 65, 200], 5, 5)
        if select_rect == i:
            pygame.draw.rect(screen, 'blue', [5 + spacing * i, 50, 65, 200], 2, 5)
        tube_boxes.append(box)

    if odd:
        for i in range(tubes_per_row - 1):
            for j in range(len(tube_cols[i + tubes_per_row])):
                pygame.draw.rect(
                    screen,
                    color_choices[tube_cols[i + tubes_per_row][j]],
                    [(spacing * 0.5) + 5 + spacing * i, 450 - (50 * j), 65, 50],
                    0,
                    7
                )
            box = pygame.draw.rect(
                screen,
                'white',
                [(spacing * 0.5) + 5 + spacing * i, 300, 65, 200],
                5,
                5
            )
            if select_rect == i + tubes_per_row:
                pygame.draw.rect(
                    screen,
                    'blue',
                    [(spacing * 0.5) + 5 + spacing * i, 300, 65, 200],
                    2,
                    5
                )
            tube_boxes.append(box)
    else:
        for i in range(tubes_per_row):
            for j in range(len(tube_cols[i + tubes_per_row])):
                pygame.draw.rect(
                    screen,
                    color_choices[tube_cols[i + tubes_per_row][j]],
                    [5 + spacing * i, 450 - (50 * j), 65, 50],
                    0,
                    7
                )
            box = pygame.draw.rect(screen, 'white', [5 + spacing * i, 300, 65, 200], 5, 5)
            if select_rect == i + tubes_per_row:
                pygame.draw.rect(screen, 'blue', [5 + spacing * i, 300, 65, 200], 2, 5)
            tube_boxes.append(box)

    return tube_boxes

def calc_move(colors, selected_rect, destination):
    same_color = True
    length = 1
    color_to_move = None

    if len(colors[selected_rect]) > 0:
        color_to_move = colors[selected_rect][-1]
        for i in range(1, len(colors[selected_rect])):
            if same_color and colors[selected_rect][-1 - i] == color_to_move:
                length += 1
            else:
                break

    if len(colors[destination]) < 4:
        if len(colors[destination]) == 0:
            color_on_top = color_to_move
        else:
            color_on_top = colors[destination][-1]

        if color_on_top == color_to_move:
            for _ in range(length):
                if len(colors[destination]) < 4 and len(colors[selected_rect]) > 0:
                    colors[destination].append(color_on_top)
                    colors[selected_rect].pop()

    return colors

def check_victory(colors):
    for tube in colors:
        if len(tube) != 0:
            if len(tube) != 4 or any(color != tube[-1] for color in tube):
                return False
    return True

run = True
while run:
    screen.fill('teal')
    timer.tick(fps)

    if new_game:
        tubes, tube_colors = generate_start()
        initial_colors = copy.deepcopy(tube_colors)
        new_game = False
    else:
        tube_rects = draw_tubes(tubes, tube_colors)

    win = check_victory(tube_colors)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                tube_colors = copy.deepcopy(initial_colors)
            elif event.key == pygame.K_RETURN:
                new_game = True
            elif event.key == pygame.K_LEFT and previous_state:
                tube_colors = previous_state.pop()
                selected = False
                select_rect = 100

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not selected:
                for i, rect in enumerate(tube_rects):
                    if rect.collidepoint(event.pos):
                        selected = True
                        select_rect = i
            else:
                for i, rect in enumerate(tube_rects):
                    if rect.collidepoint(event.pos):
                        previous_state.append(copy.deepcopy(tube_colors))
                        tube_colors = calc_move(tube_colors, select_rect, i)
                        selected = False
                        select_rect = 100

    if win:
        text = font.render('You Won! Press Enter for a new board!', True, 'white')
        screen.blit(text, (30, 265))

    info = font.render('Left-arrow-Undo | Space-Restart | Enter-New', True, 'white')
    screen.blit(info, (10, 10))

    pygame.display.flip()

pygame.quit()

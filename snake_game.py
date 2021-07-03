import pygame
import pygame_menu
from random import randint

pygame.init()

# field
BLOCK_SIZE = 25
COUNT_BLOCK = 25

MARGIN = 1
MARGIN_TOP = 70

screen_resolution = [BLOCK_SIZE * COUNT_BLOCK + 2 * BLOCK_SIZE + MARGIN * COUNT_BLOCK,
                     BLOCK_SIZE * COUNT_BLOCK + 2 * BLOCK_SIZE + MARGIN * COUNT_BLOCK + MARGIN_TOP]

# colors
PURPLE_LIGHT = (170, 142, 248)
PURPLE_BLUE = (208, 196, 241)
HEADER_COLOR = (39, 37, 37)
SNAKE_COLOR = (0, 255, 255)
APPLE_COLOR = (255, 20, 147)
FRAME_COLOR = (5, 5, 5)

# main set
screen = pygame.display.set_mode(screen_resolution)
pygame.display.set_caption('Acid Snake')
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 36)


class SnakeBlock:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return all([isinstance(other, SnakeBlock), self.x == other.x, self.y == other.y])

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCK and 0 <= self.y < COUNT_BLOCK


def draw_block(block_color, block_row, block_column):
    pygame.draw.rect(screen, block_color, [BLOCK_SIZE + block_column * BLOCK_SIZE + MARGIN * (block_column + 1),
                                           MARGIN_TOP + BLOCK_SIZE + block_row * BLOCK_SIZE + MARGIN * (block_row + 1),
                                           BLOCK_SIZE, BLOCK_SIZE])


def start_the_game():

    def get_empty_block():
        x = randint(0, COUNT_BLOCK - 1)
        y = randint(0, COUNT_BLOCK - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x, empty_block.y = randint(0, COUNT_BLOCK - 1), randint(0, COUNT_BLOCK - 1)
        return empty_block

    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    apple = get_empty_block()
    d_row = buf_row = 0
    d_col = buf_col = 1
    total = 0
    speed = 1

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1

        screen.fill(FRAME_COLOR)
        pygame.display.flip()
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, screen_resolution[0], MARGIN_TOP])

        text_total = courier.render(f'Total: {total}', True, PURPLE_LIGHT)
        text_speed = courier.render(f'Speed: {speed}', True, PURPLE_LIGHT)
        screen.blit(text_total, (BLOCK_SIZE, BLOCK_SIZE))
        screen.blit(text_speed, (BLOCK_SIZE + 450, BLOCK_SIZE))

        for row in range(COUNT_BLOCK):
            for column in range(COUNT_BLOCK):
                if (row + column) % 2 == 0:
                    color = PURPLE_BLUE
                else:
                    color = PURPLE_LIGHT
                draw_block(block_color=color, block_row=row, block_column=column)

        head = snake_blocks[-1]
        if not head.is_inside():
            print('GAME OVER')
            break

        draw_block(block_color=APPLE_COLOR, block_row=apple.x, block_column=apple.y)

        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        pygame.display.flip()

        if apple == head:
            total += 1
            speed = total // 5 + 1
            snake_blocks.append(apple)
            apple = get_empty_block()

        d_row = buf_row
        d_col = buf_col

        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            print('GAME OVER')
            break

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        timer.tick(4 + speed)


# menu
my_theme = pygame_menu.themes.THEME_DARK.copy()
my_theme.title_background_color = (0, 0, 0)
my_theme.set_background_color_opacity(0.0)

menu = pygame_menu.Menu('', 400, 300, theme=my_theme, mouse_motion_selection=True)
menu.add.button('PLAY', start_the_game)
menu.add.button('EXIT', pygame_menu.events.EXIT)
menu.mainloop(screen)

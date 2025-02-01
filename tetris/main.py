import pygame
import random

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),
    (255, 255, 0),
    (255, 165, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 0, 0),
    (128, 0, 128)
]

# Rozmiary okna
GRID_WIDTH = 10  # Szerokość planszy w klockach
GRID_HEIGHT = 20  # Wysokość planszy w klockach
BLOCK_SIZE = 30
SIDEBAR_WIDTH = 150  # Szerokość panelu bocznego
WIDTH = GRID_WIDTH * BLOCK_SIZE
HEIGHT = GRID_HEIGHT * BLOCK_SIZE
SCREEN_WIDTH = WIDTH + SIDEBAR_WIDTH  # Całkowita szerokość okna

# Kształty klocków
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()  # Dodajemy następny klocek
        self.game_over = False
        self.score = 0

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        piece = {
            'shape': shape,
            'color': color,
            'x': self.width // 2 - len(shape[0]) // 2,
            'y': 0
        }
        return piece

    def valid_move(self, piece, x, y):
        for i, row in enumerate(piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    new_x = x + j
                    new_y = y + i
                    if new_x < 0 or new_x >= self.width or new_y >= self.height:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True

    def place_piece(self):
        for i, row in enumerate(self.current_piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + i][self.current_piece['x'] + j] = self.current_piece['color']
        self.clear_lines()
        self.current_piece = self.next_piece  # Ustawiamy następny klocek jako aktualny
        self.next_piece = self.new_piece()  # Generujemy nowy następny klocek
        if not self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y']):
            self.game_over = True

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [0 for _ in range(self.width)])
        self.score += len(lines_to_clear) ** 2

    def move(self, dx):
        new_x = self.current_piece['x'] + dx
        if self.valid_move(self.current_piece, new_x, self.current_piece['y']):
            self.current_piece['x'] = new_x

    def rotate(self):
        piece = self.current_piece
        shape = piece['shape']
        new_shape = [list(row) for row in zip(*shape[::-1])]
        if self.valid_move({'shape': new_shape, 'x': piece['x'], 'y': piece['y']}, piece['x'], piece['y']):
            piece['shape'] = new_shape

    def drop(self):
        while self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
            self.current_piece['y'] += 1
        self.place_piece()

    def update(self):
        if not self.game_over:
            if self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
                self.current_piece['y'] += 1
            else:
                self.place_piece()

    def draw(self, screen):
        # Rysowanie siatki
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        # Rysowanie aktualnego klocka
        if self.current_piece:
            for i, row in enumerate(self.current_piece['shape']):
                for j, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, self.current_piece['color'], ((self.current_piece['x'] + j) * BLOCK_SIZE, (self.current_piece['y'] + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(screen, GRAY, ((self.current_piece['x'] + j) * BLOCK_SIZE, (self.current_piece['y'] + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        # Rysowanie panelu bocznego
        pygame.draw.rect(screen, GRAY, (WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))  # Tło panelu bocznego
        font = pygame.font.SysFont(None, 35)

        # Rysowanie napisu "Next:"
        text = font.render("Next:", True, WHITE)
        screen.blit(text, (WIDTH + 10, 10))

        # Rysowanie następnego klocka
        next_piece_x = WIDTH + (SIDEBAR_WIDTH // 2) - (len(self.next_piece['shape'][0]) * BLOCK_SIZE // 2)
        next_piece_y = 50
        for i, row in enumerate(self.next_piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.next_piece['color'], (next_piece_x + j * BLOCK_SIZE, next_piece_y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, GRAY, (next_piece_x + j * BLOCK_SIZE, next_piece_y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        # Rysowanie wyniku
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (WIDTH + 10, 200))

def draw_menu(screen):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 55)
    title_text = font.render("Tetris", True, WHITE)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

def draw_game_over(screen, score):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 55)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press SPACE to Restart", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # Menu główne
    in_menu = True
    while in_menu:
        draw_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    in_menu = False

    game = Tetris(GRID_WIDTH, GRID_HEIGHT)
    fall_time = 0
    fall_speed = 500

    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1)
                if event.key == pygame.K_RIGHT:
                    game.move(1)
                if event.key == pygame.K_DOWN:
                    game.drop()
                if event.key == pygame.K_UP:
                    game.rotate()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            fall_speed = 50
        else:
            fall_speed = 500

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time >= fall_speed:
            game.update()
            fall_time = 0

        game.draw(screen)
        pygame.display.flip()

        if game.game_over:
            draw_game_over(screen, game.score)
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game = Tetris(GRID_WIDTH, GRID_HEIGHT)
                            waiting_for_input = False
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return

if __name__ == "__main__":
    main()
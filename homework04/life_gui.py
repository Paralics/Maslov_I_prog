import pygame
from blib2to3.pgen2.tokenize import colon, tok_name
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        # Устанавливаем размер окна
        self.width = len(life.curr_generation[0]) * cell_size
        self.height = len(life.curr_generation) * cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self, pause: bool = False) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        if pause:
            colours = ("white", "teal")
        else:
            colours = ("white", "green")
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(colours[self.life.curr_generation[y][x]]),
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                )

    def run(self) -> None:
        """Запустить игру"""

        # pre-game prep
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        paused = False

        self.draw_grid()
        self.draw_lines()
        pygame.display.flip()

        # main game loop
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused

                        # changing cell colour when paused
                        if paused:
                            self.draw_grid(pause=True)
                            self.draw_lines()
                            pygame.display.flip()

                    elif event.key == pygame.K_w and paused:
                        self.life.step()
                        self.draw_grid(pause=True)
                        self.draw_lines()
                        pygame.display.flip()

                if event.type == pygame.MOUSEBUTTONDOWN and paused:
                    self.life.curr_generation[event.pos[1] // self.cell_size][event.pos[0] // self.cell_size] = int(
                        (self.life.curr_generation[event.pos[1] // self.cell_size][event.pos[0] // self.cell_size] - 1)
                        ** 2
                    )
                    self.draw_grid(pause=True)
                    self.draw_lines()
                    pygame.display.flip()

            if not paused:
                self.life.step()
                self.draw_grid()
                if self.life.is_max_generations_exceeded or not self.life.is_changing:
                    running = False
                self.draw_lines()
                pygame.display.flip()
                clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    tournament = GameOfLife((50, 100))
    game = GUI(tournament, cell_size=10, speed=30)
    game.run()

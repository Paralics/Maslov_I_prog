import random
import typing as tp

import pygame
from pygame.locals import *

from homework02.sudoku import create_grid

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.grid = self.get_next_generation()
            self.draw_lines()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0..
        """
        if randomize:
            grid = [[random.randint(0, 1) for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        else:
            grid = [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        colours = ("white", "green")
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(colours[self.grid[y][x]]),
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.
        """
        neighbors = []
        for dx in {-1, 0, 1}:
            for dy in {-1, 0, 1}:
                if (
                    dy + cell[0] not in {-1, self.cell_height}
                    and dx + cell[1] not in {-1, self.cell_width}
                    and not dx == dy == 0
                ):
                    neighbors.append(self.grid[dy + cell[0]][dx + cell[1]])
        return neighbors

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        """
        new_grid = self.create_grid()
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                live_neighbours = sum(self.get_neighbours((y, x)))
                if self.grid[y][x]:
                    if live_neighbours in {2, 3}:
                        new_grid[y][x] = 1
                else:
                    if live_neighbours == 3:
                        new_grid[y][x] = 1
        return new_grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()

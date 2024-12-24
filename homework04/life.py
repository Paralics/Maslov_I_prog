import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: float = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            grid = [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        for dx in {-1, 0, 1}:
            for dy in {-1, 0, 1}:
                if dy + cell[0] not in {-1, self.rows} and dx + cell[1] not in {-1, self.cols} and not dx == dy == 0:
                    neighbours.append(self.curr_generation[dy + cell[0]][dx + cell[1]])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = self.create_grid()
        for y in range(self.rows):
            for x in range(self.cols):
                live_neigbours = sum(self.get_neighbours((y, x)))
                if self.curr_generation[y][x]:
                    if live_neigbours in {2, 3}:
                        new_grid[y][x] = 1
                else:
                    if live_neigbours == 3:
                        new_grid[y][x] = 1
        return new_grid

    def step(self) -> None:
        self.prev_generation = self.curr_generation
        self.generations += 1
        self.curr_generation = self.get_next_generation()
        return None

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename) as f:
            grid = [[int(num) for num in line.strip()] for line in f.readlines() if len(line.strip()) != 0]
        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            for line in self.curr_generation:
                for number in line:
                    f.write(str(number))
                f.write("\n")


if __name__ == "__main__":
    tournament = GameOfLife.from_file(pathlib.Path("glider.txt"))
    print(tournament.curr_generation)
    for _ in range(5):
        tournament.step()
    tournament.save(pathlib.Path("PROVERKA.txt"))

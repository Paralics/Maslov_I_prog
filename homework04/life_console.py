import curses
from time import sleep

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        height, length = screen.getmaxyx()
        # horizontal lines
        for y in (0, min(len(self.life.curr_generation) + 1, height)):
            for x in range(min(len(self.life.curr_generation[0]) + 1, length)):
                screen.addch(y, x, "-")
        # vertical lines
        for x in (0, min(len(self.life.curr_generation[0]) + 1, length)):
            for y in range(min(len(self.life.curr_generation) + 1, height)):
                screen.addch(y, x, "|")
        # corners
        for x in (0, min(len(self.life.curr_generation[0]) + 1, length)):
            for y in (0, min(len(self.life.curr_generation) + 1, height)):
                screen.addch(y, x, "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        height, length = screen.getmaxyx()
        for y, row in enumerate(self.life.curr_generation):
            for x, cell in enumerate(row):
                if y < height - 2 and x < length - 2:
                    screen.addch(y + 1, x + 1, "#" if cell else ".")

    def run(self) -> None:
        screen = curses.initscr()
        screen.nodelay(True)

        while self.life.is_changing and not self.life.is_max_generations_exceeded:

            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()

            self.life.step()

            key = screen.getch()
            if key == ord("q"):
                break

            sleep(0.2)

        curses.endwin()


if __name__ == "__main__":
    life = GameOfLife((30, 30))
    game = Console(life)
    game.run()

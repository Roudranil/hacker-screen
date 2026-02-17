"""Matrix green rain effect using curses.

The iconic falling green character rain from The Matrix.
Uses curses for direct per-cell terminal control — Rich can't do
individual character placement at this speed.

Each column has an independent "drop" with random speed, length,
and characters. The head is bright white/green, the trail fades
to dark green.
"""

import contextlib
import curses
import random
import time
from dataclasses import dataclass, field

# characters used in the rain — mix of katakana and latin
RAIN_CHARS: str = (
    "アイウエオカキクケコサシスセソタチツテトナニヌネノ"
    "ハヒフヘホマミムメモヤユヨラリルレロワヲン"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
    "@#$%&*+=<>?/"
)


@dataclass
class Column:
    """Tracks the state of a single rain column.

    Attributes:
        x: Horizontal position in the terminal.
        y: Current head position of the drop.
        speed: How many rows to advance per tick.
        length: Length of the trailing tail.
        chars: Characters currently displayed in this column.
        active: Whether this column is currently raining.
    """

    x: int
    y: float = 0.0
    speed: float = 0.5
    length: int = 10
    chars: list[str] = field(default_factory=list)
    active: bool = True

    def reset(self, max_y: int) -> None:
        """Reset the column to start a new drop from the top.

        Args:
            max_y: Maximum terminal height.
        """
        self.y = random.uniform(-max_y, 0)
        self.speed = random.uniform(0.3, 1.2)
        self.length = random.randint(5, max_y // 2)
        self.chars = [random.choice(RAIN_CHARS) for _ in range(self.length)]


def _get_rain_char() -> str:
    """Pick a random character for the rain.

    Returns:
        A single random character from the rain character set.
    """
    return random.choice(RAIN_CHARS)


def _init_colors() -> None:
    """Initialize curses color pairs for the rain gradient."""
    curses.start_color()
    curses.use_default_colors()

    # color pair 1: bright green (head)
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    # color pair 2: green (body)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    # color pair 3: dark green (tail)
    curses.init_pair(3, curses.COLOR_GREEN, -1)


def _draw_rain(stdscr: "curses.window") -> None:
    """Main rain rendering loop.

    Args:
        stdscr: The curses standard screen window.
    """
    curses.curs_set(0)  # hide cursor
    stdscr.nodelay(True)  # non-blocking input
    stdscr.timeout(50)  # 50ms refresh
    _init_colors()

    max_y, max_x = stdscr.getmaxyx()

    # create a column for every other x position (spacing)
    columns: list[Column] = []
    for x in range(0, max_x, 2):
        col = Column(x=x)
        col.reset(max_y)
        columns.append(col)

    while True:
        # check for quit
        key = stdscr.getch()
        if key != -1:
            break

        stdscr.erase()

        for col in columns:
            # advance the drop
            col.y += col.speed

            # draw each character in the trail
            head_y = int(col.y)
            for i in range(col.length):
                char_y = head_y - i
                if 0 <= char_y < max_y and 0 <= col.x < max_x:
                    # pick color based on position in trail
                    if i == 0:
                        # head — bright white
                        color = curses.color_pair(1) | curses.A_BOLD
                    elif i < col.length // 3:
                        # upper trail — bright green
                        color = curses.color_pair(2) | curses.A_BOLD
                    else:
                        # lower trail — dim green
                        color = curses.color_pair(3) | curses.A_DIM

                    # randomly mutate characters
                    if random.random() < 0.05:
                        col.chars[i % len(col.chars)] = _get_rain_char()

                    char = col.chars[i % len(col.chars)]
                    # bottom-right corner write throws, suppress it
                    with contextlib.suppress(curses.error):
                        stdscr.addstr(char_y, col.x, char, color)

            # reset when drop falls off screen
            if head_y - col.length > max_y:
                col.reset(max_y)

        stdscr.refresh()
        time.sleep(0.04)


def run_matrix_rain() -> None:
    """Launch the matrix rain effect in the terminal.

    Takes over the full terminal using curses. Press any key to exit.
    Handles terminal resize and cleanup gracefully.
    """
    with contextlib.suppress(KeyboardInterrupt):
        curses.wrapper(_draw_rain)

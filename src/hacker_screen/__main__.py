"""Entry point for the hacker screen simulation.

Run with: python -m hacker_screen
Or via the installed script: hacker-screen
"""

import sys
import time

from rich.console import Console

from hacker_screen.sequences import run_all


def main() -> None:
    """Entry point for the hacker screen simulation.

    Creates a Rich console and runs the full hacking sequence.
    Clears the terminal on start for a clean takeover effect.
    Catches KeyboardInterrupt for a clean exit message.
    """
    # Windows CI/console fix: force UTF-8 output if possible
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    console = Console()

    # check terminal size
    if console.width < 60:
        console.print(
            f"[bold red]Terminal too narrow ({console.width} cols). "
            f"Need at least 60.[/bold red]"
        )
        sys.exit(1)

    try:
        # clean takeover — clear screen like curses does
        console.clear()
        time.sleep(0.3)
        run_all(console)
    except KeyboardInterrupt:
        console.print("\n\n  [bold red]★ CONNECTION TERMINATED ★[/bold red]")
        console.print("  [dim]Trace erased. You were never here.[/dim]\n")
        sys.exit(0)


if __name__ == "__main__":
    main()

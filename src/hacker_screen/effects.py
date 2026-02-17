"""Terminal effect functions for the hacking simulation.

Each function renders a distinct visual effect using Rich.
Effects are designed to be composable — sequences.py chains them
together into full hacking phases.
"""

import math
import random
import time

from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from hacker_screen.data import (
    ASCII_SKULLS,
    ENCRYPTION_ALGOS,
    ERROR_MESSAGES,
    FAKE_FILES,
    FAKE_IPS,
    FAKE_PASSWORDS,
    NETWORK_PROTOCOLS,
    PORT_NUMBERS,
    SUCCESS_MESSAGES,
    SYSTEM_PROCESSES,
    TARGET_SERVERS,
    WELCOME_BANNER,
    get_random_hex,
    get_random_ip,
    get_random_mac,
)


def typing_effect(
    console: Console,
    text: str,
    style: str = "green",
    delay: float = 0.03,
) -> None:
    """Type text character by character with a blinking cursor effect.

    Args:
        console: Rich console instance.
        text: The text to type out.
        style: Rich style string for the text color.
        delay: Seconds between each character.
    """
    for char in text:
        console.print(char, end="", style=style)
        time.sleep(delay)
    console.print()


def show_welcome_banner(console: Console) -> None:
    """Display the big ASCII welcome banner in a styled panel.

    Args:
        console: Rich console instance.
    """
    banner_text = Text(WELCOME_BANNER, style="bold green")
    panel = Panel(
        banner_text,
        border_style="bright_green",
        title="[bold red]★ CLASSIFIED ★[/bold red]",
        subtitle="[dim]v1.0.0 — unauthorized access[/dim]",
    )
    console.print(panel)
    time.sleep(0.5)

    # tagline
    typing_effect(
        console,
        ">> Initializing hacking sequence...",
        style="bold bright_green",
        delay=0.04,
    )
    time.sleep(0.3)


def show_hacking_step(console: Console, message: str, duration: float = 1.5) -> None:
    """Display a single hacking step with a spinner animation.

    Args:
        console: Rich console instance.
        message: The step message to display.
        duration: How long the spinner runs.
    """
    with Progress(
        SpinnerColumn("dots"),
        TextColumn("[bold yellow]{task.description}"),
        transient=True,
        console=console,
    ) as progress:
        progress.add_task(description=message, total=None)
        time.sleep(duration)

    # randomly pick success or error
    if random.random() < 0.85:
        msg = random.choice(SUCCESS_MESSAGES)
        console.print(f"  [bold green]✓ {msg}[/bold green]")
    else:
        msg = random.choice(ERROR_MESSAGES)
        console.print(f"  [bold red]✗ {msg}[/bold red]")
        time.sleep(0.3)
        console.print(
            "  [bold yellow]↻ Retrying with alternate vector...[/bold yellow]"
        )
        time.sleep(0.5)
        console.print(f"  [bold green]✓ {random.choice(SUCCESS_MESSAGES)}[/bold green]")


def show_password_crack(console: Console, target: str) -> None:
    """Animate a password being cracked character by character.

    Shows asterisks filling in, then reveals the plaintext password.

    Args:
        console: Rich console instance.
        target: The target file or system being cracked.
    """
    password = random.choice(FAKE_PASSWORDS)
    console.print(f"\n  [cyan]Target:[/cyan] {target}")
    console.print(f"  [cyan]Algo:[/cyan]   {random.choice(ENCRYPTION_ALGOS)}")

    # fill in asterisks
    with Live(console=console, refresh_per_second=10) as live:
        for i in range(len(password)):
            masked = "*" * (i + 1) + "_" * (len(password) - i - 1)
            live.update(Text(f"  Cracking: [{masked}]", style="bold yellow"))
            time.sleep(random.uniform(0.05, 0.2))

        # reveal
        time.sleep(0.3)
        live.update(Text(f"  Cracked:  [{password}]", style="bold green"))
    time.sleep(0.3)


def show_progress_bar(console: Console, label: str, total: int = 100) -> None:
    """Display a tqdm-style progress bar with random speed.

    Args:
        console: Rich console instance.
        label: Description label for the progress bar.
        total: Total steps for the progress bar.
    """
    from tqdm import tqdm

    # tqdm writes directly to stderr, looks authentic
    for _ in tqdm(range(total), desc=f"  {label}", ncols=70, ascii="░▒█"):
        time.sleep(random.uniform(0.005, 0.03))


def show_rich_progress(console: Console, tasks: list[str]) -> None:
    """Display multiple concurrent Rich progress bars.

    Args:
        console: Rich console instance.
        tasks: List of task description strings.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=30),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task_ids = []
        for desc in tasks:
            task_ids.append(progress.add_task(desc, total=100))

        # advance each task at random speeds
        while not all(progress.tasks[tid].completed >= 100 for tid in task_ids):
            for tid in task_ids:
                if progress.tasks[tid].completed < 100:
                    progress.advance(tid, random.uniform(1, 5))
            time.sleep(0.05)


def _build_sine_wave(
    width: int,
    height: int,
    frame: int,
    frequency: float = 0.2,
    phase_speed: float = 2.0,
) -> str:
    """Build a multi-row ASCII sinusoidal wave.

    Args:
        width: Character width of the wave.
        height: Character height of the wave area.
        frame: Current animation frame (shifts the phase).
        frequency: How many oscillations per character.
        phase_speed: How fast the wave scrolls.

    Returns:
        Multi-line string of the rendered wave.
    """
    # half-block characters for smoother curves
    chars = " ░▒▓█"
    grid = [[" "] * width for _ in range(height)]

    for x in range(width):
        # compute sine value (-1 to 1) and map to row
        y = math.sin((x * frequency) + (frame * phase_speed * 0.1))
        row = int((y + 1) / 2 * (height - 1))
        row = max(0, min(height - 1, row))

        # draw the point and fade above/below
        grid[height - 1 - row][x] = chars[4]  # █ at wave center
        for offset in range(1, 3):
            fade_char = chars[max(0, 4 - offset * 2)]
            if row + offset < height:
                grid[height - 1 - (row + offset)][x] = fade_char
            if row - offset >= 0:
                grid[height - 1 - (row - offset)][x] = fade_char

    return "\n".join("".join(row) for row in grid)


def show_signal_graph(console: Console, label: str = "SIGNAL") -> None:
    """Render a live sinusoidal wave like intercepted comms.

    Args:
        console: Rich console instance.
        label: Label for the signal graph.
    """
    width = min(console.width - 10, 50)
    height = 8
    frames = 30

    with Live(console=console, refresh_per_second=15) as live:
        for frame in range(frames):
            wave = _build_sine_wave(width, height, frame, frequency=0.25)
            text = Text(wave, style="green")
            panel = Panel(
                text,
                title=f"[bold cyan]◉ {label}[/bold cyan]",
                border_style="cyan",
                width=width + 4,
            )
            live.update(panel)
            time.sleep(0.07)


def show_dual_signal_graph(
    console: Console,
    left_label: str = "SIGINT",
    right_label: str = "AUDIO INTERCEPT",
) -> None:
    """Render two sinusoidal waves side by side.

    Both waves animate independently with different frequencies,
    displayed in adjacent panels using Rich Columns.

    Args:
        console: Rich console instance.
        left_label: Label for the left signal graph.
        right_label: Label for the right signal graph.
    """
    # each panel gets roughly half the terminal width
    panel_width = min((console.width - 6) // 2, 45)
    height = 8
    frames = 40

    with Live(console=console, refresh_per_second=15) as live:
        for frame in range(frames):
            # left wave — slower, wider frequency
            left_wave = _build_sine_wave(
                panel_width - 4,
                height,
                frame,
                frequency=0.2,
                phase_speed=1.5,
            )
            left_panel = Panel(
                Text(left_wave, style="green"),
                title=f"[bold cyan]◉ {left_label}[/bold cyan]",
                border_style="cyan",
                width=panel_width,
            )

            # right wave — faster, tighter frequency
            right_wave = _build_sine_wave(
                panel_width - 4,
                height,
                frame,
                frequency=0.35,
                phase_speed=2.5,
            )
            right_panel = Panel(
                Text(right_wave, style="bright_green"),
                title=f"[bold cyan]◉ {right_label}[/bold cyan]",
                border_style="cyan",
                width=panel_width,
            )

            live.update(Columns([left_panel, right_panel], padding=(0, 1)))
            time.sleep(0.07)


def show_hex_dump(console: Console, lines: int = 12) -> None:
    """Display a scrolling hex dump like memory inspection.

    Args:
        console: Rich console instance.
        lines: Number of hex lines to display.
    """
    console.print("\n  [bold magenta]◆ MEMORY DUMP[/bold magenta]")
    for _ in range(lines):
        addr = f"0x{random.randint(0x1000, 0xFFFF):04X}"
        hex_part = " ".join(f"{random.randint(0, 255):02X}" for _ in range(16))
        ascii_part = "".join(
            chr(random.randint(33, 126)) if random.random() > 0.3 else "."
            for _ in range(16)
        )
        console.print(
            f"  [dim]{addr}[/dim]  [green]{hex_part}[/green]  "
            f"[yellow]|{ascii_part}|[/yellow]"
        )
        time.sleep(0.08)


def show_network_traffic(console: Console, packets: int = 10) -> None:
    """Display fake packet capture log entries.

    Args:
        console: Rich console instance.
        packets: Number of packets to show.
    """
    console.print("\n  [bold cyan]◉ PACKET CAPTURE[/bold cyan]")
    table = Table(show_header=True, header_style="bold cyan", padding=(0, 1))
    table.add_column("#", width=4)
    table.add_column("Source", width=16)
    table.add_column("Destination", width=16)
    table.add_column("Proto", width=8)
    table.add_column("Size", width=8)
    table.add_column("Info", width=20)

    with Live(table, console=console, refresh_per_second=8) as live:
        for i in range(packets):
            src = get_random_ip()
            dst = random.choice(FAKE_IPS)
            proto = random.choice(NETWORK_PROTOCOLS)
            size = f"{random.randint(64, 1500)}B"
            info = random.choice(
                ["SYN", "ACK", "PSH", "FIN", "RST", "DATA", "HANDSHAKE"]
            )
            table.add_row(str(i + 1), src, dst, proto, size, info)
            live.update(table)
            time.sleep(random.uniform(0.15, 0.4))


def show_file_tree(console: Console) -> None:
    """Render an animated file tree like exploring a remote filesystem.

    Args:
        console: Rich console instance.
    """
    target = random.choice(TARGET_SERVERS)
    tree = Tree(
        f"[bold green]📂 //{target}/[/bold green]",
        guide_style="dim green",
    )

    dirs = ["etc", "var", "home", "opt", "srv", "root"]
    with Live(tree, console=console, refresh_per_second=6) as live:
        for d in dirs:
            branch = tree.add(f"[cyan]📁 {d}/[/cyan]")
            live.update(tree)
            time.sleep(0.2)

            # add some files
            for _ in range(random.randint(1, 4)):
                fname = random.choice(FAKE_FILES).split("/")[-1]
                size = f"{random.randint(1, 9999)}K"
                branch.add(f"[dim]{fname}[/dim] [yellow]({size})[/yellow]")
                live.update(tree)
                time.sleep(0.15)


def show_system_info(console: Console) -> None:
    """Display a fake system information table.

    Args:
        console: Rich console instance.
    """
    target = random.choice(TARGET_SERVERS)
    table = Table(
        title=f"[bold red]◆ SYSTEM INTEL: {target}[/bold red]",
        border_style="red",
        show_header=False,
        padding=(0, 2),
    )
    table.add_column("Key", style="bold cyan")
    table.add_column("Value", style="green")

    info = [
        ("Hostname", target),
        ("OS", random.choice(["Ubuntu 22.04", "RHEL 9", "Debian 12", "Arch"])),
        ("Kernel", f"6.{random.randint(1, 8)}.{random.randint(0, 15)}-generic"),
        ("CPU", random.choice(["Intel Xeon E5-2690", "AMD EPYC 7742", "ARM Neoverse"])),
        ("RAM", f"{random.choice([16, 32, 64, 128, 256])} GB"),
        ("Uptime", f"{random.randint(1, 365)} days"),
        ("IP", get_random_ip()),
        ("MAC", get_random_mac()),
        ("Open Ports", str(random.randint(3, 12))),
        ("Active Users", str(random.randint(1, 5))),
    ]

    with Live(table, console=console, refresh_per_second=6) as live:
        for key, val in info:
            table.add_row(key, val)
            live.update(table)
            time.sleep(0.2)
    time.sleep(0.3)


def show_port_scan(console: Console, num_ports: int = 15) -> None:
    """Animate a port scan with open/closed/filtered results.

    Args:
        console: Rich console instance.
        num_ports: Number of ports to scan.
    """
    target = get_random_ip()
    console.print(f"\n  [bold cyan]◉ SCANNING {target}[/bold cyan]")

    ports = sorted(random.sample(PORT_NUMBERS, min(num_ports, len(PORT_NUMBERS))))
    for port in ports:
        time.sleep(random.uniform(0.05, 0.2))
        state = random.choices(["open", "closed", "filtered"], weights=[0.4, 0.4, 0.2])[
            0
        ]

        if state == "open":
            # pick a service name
            service = random.choice(SYSTEM_PROCESSES)
            console.print(f"  [green]  {port:>5}/tcp   open     {service}[/green]")
        elif state == "closed":
            console.print(f"  [red]  {port:>5}/tcp   closed[/red]")
        else:
            console.print(f"  [yellow]  {port:>5}/tcp   filtered[/yellow]")


def show_countdown(console: Console, seconds: int = 10) -> None:
    """Display a dramatic countdown with large numbers.

    Args:
        console: Rich console instance.
        seconds: Number of seconds to count down from.
    """
    for i in range(seconds, 0, -1):
        # color transitions from green to red
        if i > 6:
            color = "green"
        elif i > 3:
            color = "yellow"
        else:
            color = "bold red"

        text = Text(f"  >>> {i} <<<", style=color)
        console.print(text)
        time.sleep(1.0)

    console.print("\n  [bold red blink]★ LAUNCHING ★[/bold red blink]")
    time.sleep(0.5)


def show_permission_prompt(console: Console) -> None:
    """Show the "Hack it?" prompt with animated password entry.

    Args:
        console: Rich console instance.
    """
    console.print()
    skull = random.choice(ASCII_SKULLS)
    console.print(Panel(skull, style="bold red", border_style="red"))

    typing_effect(
        console,
        ">> All systems compromised. Final payload ready.",
        style="bold yellow",
        delay=0.04,
    )
    time.sleep(0.5)

    console.print()
    console.print(
        "  [bold bright_white]╔══════════════════════════╗[/bold bright_white]"
    )
    console.print(
        "  [bold bright_white]║   EXECUTE FINAL HACK?    ║[/bold bright_white]"
    )
    console.print(
        "  [bold bright_white]╚══════════════════════════╝[/bold bright_white]"
    )
    console.print()

    # fake password prompt
    password = random.choice(FAKE_PASSWORDS)
    console.print("  [cyan]Enter master password:[/cyan] ", end="")
    for _ in password:
        console.print("[bold green]*[/bold green]", end="")
        time.sleep(random.uniform(0.05, 0.15))
    console.print()
    time.sleep(0.3)

    console.print("  [bold green]✓ AUTHENTICATION VERIFIED[/bold green]")
    time.sleep(0.5)

    typing_effect(
        console,
        ">> Initiating final sequence...",
        style="bold red",
        delay=0.05,
    )
    time.sleep(0.3)


def show_glitch_text(console: Console, text: str, cycles: int = 8) -> None:
    """Display text that glitches with random character swaps.

    Args:
        console: Rich console instance.
        text: The target text to glitch towards.
        cycles: Number of glitch animation cycles.
    """
    glitch_chars = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`░▒▓█▀▄"

    with Live(console=console, refresh_per_second=10) as live:
        for cycle in range(cycles):
            # gradually reveal the real text
            ratio = cycle / cycles
            glitched = ""
            for char in text:
                if random.random() < ratio:
                    glitched += char
                else:
                    glitched += random.choice(glitch_chars)

            live.update(Text(f"  {glitched}", style="bold bright_green"))
            time.sleep(0.12)

        # final reveal
        live.update(Text(f"  {text}", style="bold bright_green"))
    time.sleep(0.3)


def show_encryption_crack(console: Console, num_attempts: int = 20) -> None:
    """Animate a hash brute-force attack with scrolling attempts.

    Args:
        console: Rich console instance.
        num_attempts: Number of hash attempts to display.
    """
    algo = random.choice(ENCRYPTION_ALGOS)
    console.print(f"\n  [bold magenta]◆ BRUTE-FORCING {algo}[/bold magenta]")
    time.sleep(0.2)

    for i in range(num_attempts):
        attempt_hash = get_random_hex(64)
        if i < num_attempts - 1:
            console.print(f"  [red]✗[/red] [dim]{attempt_hash}[/dim]")
        else:
            console.print(f"  [green]✓[/green] [bold green]{attempt_hash}[/bold green]")
            console.print(
                "  [bold green]  COLLISION FOUND — key recovered[/bold green]"
            )
        time.sleep(random.uniform(0.03, 0.12))

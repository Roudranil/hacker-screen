"""Hacking sequence orchestration.

Chains individual effects from effects.py into dramatic multi-step
hacking phases. Each phase tells a part of the story — from recon
to exploitation to the final matrix rain.
"""

import random
import time

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from hacker_screen.data import (
    FAKE_FILES,
    FAKE_IPS,
    HACKING_STEPS,
    MALWARE_NAMES,
    TARGET_SERVERS,
    get_random_items,
)
from hacker_screen.effects import (
    show_countdown,
    show_dual_signal_graph,
    show_encryption_crack,
    show_file_tree,
    show_glitch_text,
    show_hacking_step,
    show_hex_dump,
    show_network_traffic,
    show_password_crack,
    show_permission_prompt,
    show_port_scan,
    show_progress_bar,
    show_rich_progress,
    show_system_info,
    show_welcome_banner,
    typing_effect,
)
from hacker_screen.matrix_rain import run_matrix_rain


def _phase_header(console: Console, title: str, style: str = "red") -> None:
    """Print a phase header divider.

    Args:
        console: Rich console instance.
        title: Phase title text.
        style: Rich style for the header.
    """
    console.print()
    console.print(
        Panel(
            Text(f"  ◆ {title}", style=f"bold {style}"),
            border_style=style,
            width=min(console.width, 60),
        )
    )
    time.sleep(0.5)


def run_welcome(console: Console) -> None:
    """Show welcome banner and initial system scan.

    Args:
        console: Rich console instance.
    """
    show_welcome_banner(console)
    time.sleep(0.3)

    # glitch in the target name
    target = random.choice(TARGET_SERVERS)
    show_glitch_text(console, f"TARGET ACQUIRED: {target.upper()}")
    time.sleep(0.3)

    # system info
    show_system_info(console)


def run_recon_phase(console: Console) -> None:
    """Run reconnaissance — network scan, port scan, target discovery.

    Args:
        console: Rich console instance.
    """
    _phase_header(console, "PHASE 1: RECONNAISSANCE", "cyan")

    typing_effect(console, ">> Scanning network topology...", style="cyan")
    time.sleep(0.3)

    show_port_scan(console)
    time.sleep(0.3)

    show_network_traffic(console, packets=8)
    time.sleep(0.3)

    # show some ips found
    ips = get_random_items(FAKE_IPS, 4)
    console.print("\n  [bold cyan]◉ LIVE HOSTS DISCOVERED:[/bold cyan]")
    for ip in ips:
        console.print(f"  [green]  → {ip}[/green]")
        time.sleep(0.15)


def run_exploitation_phase(console: Console) -> None:
    """Run exploitation — inject payloads, escalate privileges.

    Args:
        console: Rich console instance.
    """
    _phase_header(console, "PHASE 2: EXPLOITATION", "red")

    steps = get_random_items(HACKING_STEPS, random.randint(5, 7))
    for step in steps:
        show_hacking_step(console, step, duration=random.uniform(0.8, 2.0))
        time.sleep(0.2)


def run_cracking_phase(console: Console) -> None:
    """Run password cracking and file decryption.

    Args:
        console: Rich console instance.
    """
    _phase_header(console, "PHASE 3: CRACKING", "magenta")

    # crack some passwords
    targets = get_random_items(FAKE_FILES, 3)
    for target in targets:
        show_password_crack(console, target)
        time.sleep(0.3)

    # brute force a hash
    show_encryption_crack(console)
    time.sleep(0.3)

    # progress bar for bulk decrypt
    show_progress_bar(console, "Bulk decrypt", total=80)


def run_data_exfil_phase(console: Console) -> None:
    """Run data exfiltration — file browsing, memory dump, downloads.

    Args:
        console: Rich console instance.
    """
    _phase_header(console, "PHASE 4: DATA EXFILTRATION", "yellow")

    show_file_tree(console)
    time.sleep(0.3)

    show_hex_dump(console, lines=10)
    time.sleep(0.3)

    # download progress bars
    show_rich_progress(
        console,
        [
            "Downloading database dump...",
            "Extracting credentials...",
            "Compressing archive...",
        ],
    )


def run_surveillance_phase(console: Console) -> None:
    """Run surveillance — dual signal intercept side by side.

    Args:
        console: Rich console instance.
    """
    _phase_header(console, "PHASE 5: SURVEILLANCE", "green")

    typing_effect(
        console,
        ">> Intercepting communications...",
        style="green",
    )
    time.sleep(0.3)

    show_dual_signal_graph(
        console,
        left_label="SIGINT-A",
        right_label="AUDIO INTERCEPT",
    )


def run_malware_phase(console: Console) -> None:
    """Run malware deployment — rootkit install, persistence.

    Args:
        console: Rich console instance.
    """
    _phase_header(console, "PHASE 6: PAYLOAD DEPLOYMENT", "red")

    payloads = get_random_items(MALWARE_NAMES, 4)
    for payload in payloads:
        show_hacking_step(
            console,
            f"Deploying {payload}...",
            duration=random.uniform(0.8, 1.5),
        )
        time.sleep(0.15)

    # install progress
    show_progress_bar(console, "Installing rootkit", total=60)
    time.sleep(0.2)

    typing_effect(
        console,
        ">> All payloads deployed. Cleaning traces...",
        style="bold yellow",
    )
    show_progress_bar(console, "Wiping logs", total=40)


def run_final_prompt(console: Console) -> None:
    """Show the final "Hack it?" prompt, password, and countdown.

    Args:
        console: Rich console instance.
    """
    _phase_header(console, "PHASE 7: FINAL SEQUENCE", "bright_red")
    show_permission_prompt(console)
    time.sleep(0.5)

    typing_effect(
        console,
        ">> Hacking starting in...",
        style="bold bright_green",
    )
    show_countdown(console, seconds=10)


def run_all(console: Console) -> None:
    """Run the complete hacking simulation from start to matrix rain.

    Chains all phases in order, then launches the matrix rain effect.
    Handles KeyboardInterrupt for clean exit at any point.

    Args:
        console: Rich console instance.
    """
    # run all phases
    run_welcome(console)
    run_recon_phase(console)
    run_exploitation_phase(console)
    run_cracking_phase(console)
    run_data_exfil_phase(console)
    run_surveillance_phase(console)
    run_malware_phase(console)
    run_final_prompt(console)

    # the grand finale
    console.print("\n  [bold green]★ ENTERING THE MATRIX ★[/bold green]\n")
    time.sleep(1.0)
    run_matrix_rain()

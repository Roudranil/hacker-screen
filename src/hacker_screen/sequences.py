"""Hacking sequence orchestration.

Chains individual effects from effects.py into dramatic multi-step
hacking phases. Each phase tells a part of the story — from recon
to exploitation to the final matrix rain.

Every run is unique: messages are randomized, bonus phases appear
randomly, and some steps may "fail" and retry for dramatic tension.
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
    PHASE_MESSAGES,
    PORT_NUMBERS,
    SIGNAL_PROFILES,
    TARGET_SERVERS,
    get_random_items,
)
from hacker_screen.effects import (
    show_countdown,
    show_dual_signal_graph,
    show_encryption_crack,
    show_failure_retry,
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

# ---------------------------------------------------------------------------
# Phase metadata — centralizes phase numbering, titles, and styles
# ---------------------------------------------------------------------------

# styles cycle through these for phase headers
_PHASE_STYLES = ["cyan", "red", "magenta", "yellow", "green", "red", "bright_red"]


def _phase_header(
    console: Console,
    phase_num: int,
    title: str,
    style: str | None = None,
) -> None:
    """Print a phase header divider.

    Style is either explicit or auto-picked from the phase number.

    Args:
        console: Rich console instance.
        phase_num: Phase number (1-based) for display and auto-style.
        title: Phase title text.
        style: Rich style override; if None, chosen from phase number.
    """
    if style is None:
        style = _PHASE_STYLES[(phase_num - 1) % len(_PHASE_STYLES)]

    console.print()
    console.print(
        Panel(
            Text(f"  ◆ PHASE {phase_num}: {title}", style=f"bold {style}"),
            border_style=style,
            width=min(console.width, 60),
        )
    )
    time.sleep(0.5)


# ---------------------------------------------------------------------------
# Core phases
# ---------------------------------------------------------------------------


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


def run_recon_phase(console: Console, phase_num: int = 1) -> None:
    """Run reconnaissance — network scan, port scan, target discovery.

    Content varies per run: different messages, sometimes extra scans.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
    """
    _phase_header(console, phase_num, "RECONNAISSANCE")

    msg = random.choice(PHASE_MESSAGES["recon"])
    typing_effect(console, msg, style="cyan")
    time.sleep(0.3)

    show_port_scan(console)
    time.sleep(0.3)

    # sometimes also show a system info scan
    if random.random() < 0.35:
        typing_effect(console, ">> Fingerprinting target OS...", style="cyan")
        show_system_info(console)
        time.sleep(0.2)

    show_network_traffic(console, packets=random.randint(6, 12))
    time.sleep(0.3)

    # show some ips found
    ips = get_random_items(FAKE_IPS, random.randint(3, 6))
    console.print("\n  [bold cyan]◉ LIVE HOSTS DISCOVERED:[/bold cyan]")
    for ip in ips:
        console.print(f"  [green]  → {ip}[/green]")
        time.sleep(0.15)


def run_exploitation_phase(console: Console, phase_num: int = 2) -> None:
    """Run exploitation — inject payloads, escalate privileges.

    Some steps may randomly fail and retry for dramatic tension.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
    """
    _phase_header(console, phase_num, "EXPLOITATION")

    steps = get_random_items(HACKING_STEPS, random.randint(5, 8))
    for step in steps:
        # ~20% chance of failure
        if random.random() < 0.20:
            show_failure_retry(console, step)
        else:
            show_hacking_step(console, step, duration=random.uniform(0.8, 2.0))
        time.sleep(0.2)


def run_cracking_phase(console: Console, phase_num: int = 3) -> None:
    """Run password cracking and file decryption.

    Varies the number of targets and sometimes leads with brute-force.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
    """
    _phase_header(console, phase_num, "CRACKING")

    # sometimes lead with brute force
    if random.random() < 0.4:
        show_encryption_crack(console)
        time.sleep(0.3)

    # crack some passwords (varied count)
    targets = get_random_items(FAKE_FILES, random.randint(2, 5))
    for target in targets:
        show_password_crack(console, target)
        time.sleep(0.3)

    # brute force if we didn't lead with it
    if random.random() < 0.6:
        show_encryption_crack(console)
        time.sleep(0.3)

    # progress bar for bulk decrypt
    show_progress_bar(console, "Bulk decrypt", total=random.randint(50, 120))


def run_data_exfil_phase(console: Console, phase_num: int = 4) -> None:
    """Run data exfiltration — file browsing, memory dump, downloads.

    Download task names are randomized from phase_messages.json.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
    """
    _phase_header(console, phase_num, "DATA EXFILTRATION")

    show_file_tree(console)
    time.sleep(0.3)

    show_hex_dump(console, lines=random.randint(8, 16))
    time.sleep(0.3)

    # randomized download tasks
    tasks = get_random_items(PHASE_MESSAGES["exfil_tasks"], 3)
    show_rich_progress(console, tasks)


def run_surveillance_phase(console: Console, phase_num: int = 5) -> None:
    """Run surveillance — scanning + audio intercept side by side.

    Picks a random signal profile for varied labels and frequencies.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
    """
    _phase_header(console, phase_num, "SURVEILLANCE")

    msg = random.choice(PHASE_MESSAGES["surveillance"])
    typing_effect(console, msg, style="green")
    time.sleep(0.3)

    profile = random.choice(SIGNAL_PROFILES)
    show_dual_signal_graph(
        console,
        left_label=profile["left_label"],
        right_label=profile["right_label"],
        scan_speed=profile["scan_speed"],
        wave_freq=profile["wave_freq"],
        wave_speed=profile["wave_speed"],
    )


def run_malware_phase(console: Console, phase_num: int = 6) -> None:
    """Run malware deployment — rootkit install, persistence.

    Some installs may randomly fail and retry.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
    """
    _phase_header(console, phase_num, "PAYLOAD DEPLOYMENT")

    payloads = get_random_items(MALWARE_NAMES, random.randint(3, 6))
    for payload in payloads:
        msg = f"Deploying {payload}..."
        if random.random() < 0.15:
            show_failure_retry(console, msg)
        else:
            show_hacking_step(
                console,
                msg,
                duration=random.uniform(0.8, 1.5),
            )
        time.sleep(0.15)

    # install progress
    show_progress_bar(console, "Installing rootkit", total=random.randint(40, 80))
    time.sleep(0.2)

    msg = random.choice(PHASE_MESSAGES["malware_cleanup"])
    typing_effect(console, msg, style="bold yellow")
    show_progress_bar(console, "Wiping logs", total=random.randint(30, 60))


def run_final_prompt(console: Console, phase_num: int = 7) -> None:
    """Show the final "Hack it?" prompt, password, and countdown.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
    """
    _phase_header(console, phase_num, "FINAL SEQUENCE")
    show_permission_prompt(console)
    time.sleep(0.5)

    typing_effect(
        console,
        ">> Hacking starting in...",
        style="bold bright_green",
    )
    show_countdown(console, seconds=10)


# ---------------------------------------------------------------------------
# Bonus phases — randomly injected between core phases
# ---------------------------------------------------------------------------


def run_firewall_bypass(console: Console, phase_num: int) -> None:
    """Bonus: firewall/IDS bypass with denial then success.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
    """
    _phase_header(console, phase_num, "FIREWALL BYPASS")

    msg = random.choice(PHASE_MESSAGES["firewall_bypass"])
    typing_effect(console, msg, style="red")
    time.sleep(0.3)

    steps = get_random_items(PHASE_MESSAGES["firewall_steps"], 3)
    for step in steps:
        # replace %PORT% placeholder with a random port
        step = step.replace("%PORT%", str(random.choice(PORT_NUMBERS)))
        if random.random() < 0.3:
            show_failure_retry(console, step)
        else:
            show_hacking_step(console, step, duration=random.uniform(0.8, 1.5))
        time.sleep(0.2)

    console.print("\n  [bold green]✓ FIREWALL BYPASSED[/bold green]")
    time.sleep(0.3)


def run_social_engineering(console: Console, phase_num: int) -> None:
    """Bonus: social engineering / credential phishing simulation.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
    """
    _phase_header(console, phase_num, "SOCIAL ENGINEERING")

    msg = random.choice(PHASE_MESSAGES["social_engineering"])
    typing_effect(console, msg, style="yellow")
    time.sleep(0.3)

    steps = get_random_items(PHASE_MESSAGES["social_steps"], random.randint(2, 4))
    for step in steps:
        show_hacking_step(console, step, duration=random.uniform(1.0, 2.0))
        time.sleep(0.2)

    show_progress_bar(console, "Exfiltrating credentials", total=40)
    console.print("\n  [bold green]✓ CREDENTIALS CAPTURED[/bold green]")
    time.sleep(0.3)


def run_cleanup_phase(console: Console, phase_num: int) -> None:
    """Bonus: trace wiping and log sanitization.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
    """
    _phase_header(console, phase_num, "TRACE CLEANUP")

    msg = random.choice(PHASE_MESSAGES["cleanup"])
    typing_effect(console, msg, style="dim")
    time.sleep(0.3)

    steps = get_random_items(PHASE_MESSAGES["cleanup_steps"], random.randint(3, 5))
    for step in steps:
        show_hacking_step(console, step, duration=random.uniform(0.5, 1.2))
        time.sleep(0.15)

    show_progress_bar(console, "Sanitizing forensic evidence", total=50)
    console.print("\n  [bold green]✓ ALL TRACES ELIMINATED[/bold green]")
    time.sleep(0.3)


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

# bonus phases and their insertion probability
_BONUS_PHASES = [
    (run_firewall_bypass, 0.30),
    (run_social_engineering, 0.25),
    (run_cleanup_phase, 0.40),
]


def run_all(console: Console) -> None:
    """Run the complete hacking simulation from start to matrix rain.

    Chains core phases in order with bonus phases randomly injected
    between them. Phase numbers auto-increment so headers stay correct.
    Handles KeyboardInterrupt for clean exit at any point.

    Args:
        console: Rich console instance.
    """
    # build the phase list: core phases with bonus phases inserted
    core_phases = [
        run_recon_phase,
        run_exploitation_phase,
        run_cracking_phase,
        run_data_exfil_phase,
        run_surveillance_phase,
        run_malware_phase,
    ]

    # decide which bonus phases appear and where
    bonus_insertions: list[tuple[int, callable]] = []
    for bonus_fn, probability in _BONUS_PHASES:
        if random.random() < probability:
            # insert after a random core phase (not last, that's before final)
            insert_after = random.randint(0, len(core_phases) - 1)
            bonus_insertions.append((insert_after, bonus_fn))

    # sort by insertion point (descending) so indices don't shift
    bonus_insertions.sort(key=lambda x: x[0], reverse=True)
    for insert_after, bonus_fn in bonus_insertions:
        core_phases.insert(insert_after + 1, bonus_fn)

    # run welcome (no phase number)
    run_welcome(console)

    # run all phases with auto-incrementing phase numbers
    for i, phase_fn in enumerate(core_phases):
        phase_fn(console, phase_num=i + 1)

    # final prompt gets the next phase number
    run_final_prompt(console, phase_num=len(core_phases) + 1)

    # the grand finale
    console.print("\n  [bold green]★ ENTERING THE MATRIX ★[/bold green]\n")
    time.sleep(1.0)
    run_matrix_rain()

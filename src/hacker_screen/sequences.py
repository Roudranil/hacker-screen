"""Hacking sequence orchestration.

Chains individual effects from effects.py into dramatic multi-step
hacking phases. Each phase tells a part of the story — from recon
to exploitation to the final matrix rain.

Every run is unique: messages are randomized, bonus phases appear
randomly, and some steps may "fail" and retry for dramatic tension.

Retry caps ensure failures don't overwhelm:
- Max 2 retries per phase
- Max 3 retries globally across the entire run
"""

import random
import time
from typing import Any

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

# maximum number of phases between welcome and final (inclusive)
_MAX_PHASES = 8

# retry limits
_MAX_RETRIES_PER_PHASE = 2
_MAX_RETRIES_GLOBAL = 3


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
# Retry tracking
# ---------------------------------------------------------------------------


class RetryTracker:
    """Tracks retry counts per-phase and globally.

    Attributes:
        phase_retries: Retries used in the current phase.
        global_retries: Total retries used across all phases.
    """

    def __init__(self) -> None:
        self.phase_retries = 0
        self.global_retries = 0

    def reset_phase(self) -> None:
        """Reset the per-phase retry counter for a new phase."""
        self.phase_retries = 0

    def can_retry(self) -> bool:
        """Check if a retry is allowed under both caps.

        Returns:
            True if both per-phase and global limits allow another retry.
        """
        return (
            self.phase_retries < _MAX_RETRIES_PER_PHASE
            and self.global_retries < _MAX_RETRIES_GLOBAL
        )

    def record_retry(self) -> None:
        """Record that a retry was used."""
        self.phase_retries += 1
        self.global_retries += 1


def _maybe_fail(
    console: Console,
    message: str,
    fail_chance: float,
    tracker: RetryTracker,
    duration: float = 1.0,
) -> None:
    """Run a hacking step that may randomly fail and retry.

    Respects both per-phase and global retry caps.

    Args:
        console: Rich console instance.
        message: The step description.
        fail_chance: Probability (0-1) of failure occurring.
        tracker: RetryTracker instance for cap enforcement.
        duration: Duration for the hacking step spinner.
    """
    if random.random() < fail_chance and tracker.can_retry():
        tracker.record_retry()
        show_failure_retry(console, message)
    else:
        show_hacking_step(console, message, duration=duration)


# ---------------------------------------------------------------------------
# Core phases (always present)
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


def run_exploitation_phase(
    console: Console,
    phase_num: int = 1,
    tracker: RetryTracker | None = None,
) -> None:
    """Run exploitation — inject payloads, escalate privileges.

    Some steps may randomly fail and retry (capped by tracker).

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
        tracker: RetryTracker for cap enforcement.
    """
    if tracker is None:
        tracker = RetryTracker()
    tracker.reset_phase()
    _phase_header(console, phase_num, "EXPLOITATION")

    steps = get_random_items(HACKING_STEPS, random.randint(5, 8))
    for step in steps:
        _maybe_fail(
            console,
            step,
            0.20,
            tracker,
            duration=random.uniform(0.8, 2.0),
        )
        time.sleep(0.2)


def run_cracking_phase(
    console: Console,
    phase_num: int = 2,
    tracker: RetryTracker | None = None,
) -> None:
    """Run password cracking and file decryption.

    Varies the number of targets and sometimes leads with brute-force.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
        tracker: RetryTracker (unused, kept for consistent interface).
    """
    _phase_header(console, phase_num, "CRACKING")

    # sometimes lead with brute force
    led_with_brute = random.random() < 0.4
    if led_with_brute:
        show_encryption_crack(console)
        time.sleep(0.3)

    # crack some passwords (varied count)
    targets = get_random_items(FAKE_FILES, random.randint(2, 5))
    for target in targets:
        show_password_crack(console, target)
        time.sleep(0.3)

    # always brute force if we didn't lead with it
    if not led_with_brute:
        show_encryption_crack(console)
        time.sleep(0.3)

    # progress bar for bulk decrypt
    show_progress_bar(console, "Bulk decrypt", total=random.randint(50, 120))


def run_malware_phase(
    console: Console,
    phase_num: int = 3,
    tracker: RetryTracker | None = None,
) -> None:
    """Run malware deployment — rootkit install, persistence.

    Some installs may randomly fail and retry (capped by tracker).

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
        tracker: RetryTracker for cap enforcement.
    """
    if tracker is None:
        tracker = RetryTracker()
    tracker.reset_phase()
    _phase_header(console, phase_num, "PAYLOAD DEPLOYMENT")

    payloads = get_random_items(MALWARE_NAMES, random.randint(3, 6))
    for payload in payloads:
        msg = f"Deploying {payload}..."
        _maybe_fail(
            console,
            msg,
            0.15,
            tracker,
            duration=random.uniform(0.8, 1.5),
        )
        time.sleep(0.15)

    # install progress
    show_progress_bar(console, "Installing rootkit", total=random.randint(40, 80))
    time.sleep(0.2)

    msg = random.choice(PHASE_MESSAGES["malware_cleanup"])
    typing_effect(console, msg, style="bold yellow")
    show_progress_bar(console, "Wiping logs", total=random.randint(30, 60))


def run_final_prompt(
    console: Console,
    phase_num: int = 4,
    tracker: RetryTracker | None = None,
) -> None:
    """Show the final \"Hack it?\" prompt, password, and countdown.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
        tracker: RetryTracker (unused, kept for consistent interface).
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
# Bonus phases — randomly selected to fill remaining slots
# ---------------------------------------------------------------------------


def run_recon_phase(
    console: Console,
    phase_num: int = 1,
    tracker: RetryTracker | None = None,
) -> None:
    """Run reconnaissance — network scan, port scan, target discovery.

    Content varies per run: different messages, sometimes extra scans.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
        tracker: RetryTracker (unused, kept for consistent interface).
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


def run_data_exfil_phase(
    console: Console,
    phase_num: int = 1,
    tracker: RetryTracker | None = None,
) -> None:
    """Run data exfiltration — file browsing, memory dump, downloads.

    Download task names are randomized from phase_messages.json.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
        tracker: RetryTracker (unused, kept for consistent interface).
    """
    _phase_header(console, phase_num, "DATA EXFILTRATION")

    show_file_tree(console)
    time.sleep(0.3)

    show_hex_dump(console, lines=random.randint(8, 16))
    time.sleep(0.3)

    # randomized download tasks
    tasks = get_random_items(PHASE_MESSAGES["exfil_tasks"], 3)
    show_rich_progress(console, tasks)


def run_surveillance_phase(
    console: Console,
    phase_num: int = 1,
    tracker: RetryTracker | None = None,
) -> None:
    """Run surveillance — scanning + audio intercept side by side.

    Picks a random signal profile for varied labels and frequencies.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
        tracker: RetryTracker (unused, kept for consistent interface).
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


def run_firewall_bypass(
    console: Console,
    phase_num: int = 1,
    tracker: RetryTracker | None = None,
) -> None:
    """Bonus: firewall/IDS bypass with denial then success.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
        tracker: RetryTracker for cap enforcement.
    """
    if tracker is None:
        tracker = RetryTracker()
    tracker.reset_phase()
    _phase_header(console, phase_num, "FIREWALL BYPASS")

    msg = random.choice(PHASE_MESSAGES["firewall_bypass"])
    typing_effect(console, msg, style="red")
    time.sleep(0.3)

    steps = get_random_items(PHASE_MESSAGES["firewall_steps"], 3)
    for step in steps:
        # replace %PORT% placeholder with a random port
        step = step.replace("%PORT%", str(random.choice(PORT_NUMBERS)))
        _maybe_fail(
            console,
            step,
            0.3,
            tracker,
            duration=random.uniform(0.8, 1.5),
        )
        time.sleep(0.2)

    console.print("\n  [bold green]✓ FIREWALL BYPASSED[/bold green]")
    time.sleep(0.3)


def run_social_engineering(
    console: Console,
    phase_num: int = 1,
    tracker: RetryTracker | None = None,
) -> None:
    """Bonus: social engineering / credential phishing simulation.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
        tracker: RetryTracker (unused, kept for consistent interface).
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


def run_cleanup_phase(
    console: Console,
    phase_num: int = 1,
    tracker: RetryTracker | None = None,
) -> None:
    """Bonus: trace wiping and log sanitization.

    Args:
        console: Rich console instance.
        phase_num: Current phase number for the header.
        tracker: RetryTracker (unused, kept for consistent interface).
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

# bonus phase pool with selection weights (higher = more likely)
_BONUS_POOL: list[tuple[Any, float]] = [
    (run_recon_phase, 0.65),
    (run_data_exfil_phase, 0.55),
    (run_surveillance_phase, 0.50),
    (run_firewall_bypass, 0.30),
    (run_social_engineering, 0.25),
    (run_cleanup_phase, 0.40),
]


def _select_bonus_phases(max_slots: int) -> list:
    """Select bonus phases for available slots.

    Each phase is independently tested against its probability.
    Result is capped to max_slots.

    Args:
        max_slots: Maximum number of bonus phases to include.

    Returns:
        List of selected phase functions (randomly ordered).
    """
    selected = []
    for phase_fn, probability in _BONUS_POOL:
        if random.random() < probability:
            selected.append(phase_fn)

    # cap to available slots
    if len(selected) > max_slots:
        selected = random.sample(selected, max_slots)

    random.shuffle(selected)
    return selected


def run_all(console: Console) -> None:
    """Run the complete hacking simulation from start to matrix rain.

    Required phases: Welcome → Exploitation → Cracking → Payload → Final.
    Bonus phases fill remaining slots (up to _MAX_PHASES total).
    A shared RetryTracker enforces max 2 retries/phase, 3 globally.

    Args:
        console: Rich console instance.
    """
    tracker = RetryTracker()

    # required phases (always present, always in this order)
    required = [
        run_exploitation_phase,
        run_cracking_phase,
        run_malware_phase,
    ]

    # how many bonus slots are available?
    # total phases = required (3) + bonus + final (1) ≤ _MAX_PHASES
    bonus_slots = _MAX_PHASES - len(required) - 1  # -1 for final
    bonus_phases = _select_bonus_phases(bonus_slots)

    # build the full phase list: insert bonus phases between required ones
    phases: list = list(required)

    for bonus_fn in bonus_phases:
        insert_at = random.randint(0, len(phases))
        phases.insert(insert_at, bonus_fn)

    # run welcome (no phase number)
    run_welcome(console)

    # run all phases with auto-incrementing phase numbers
    for i, phase_fn in enumerate(phases):
        phase_fn(console, phase_num=i + 1, tracker=tracker)

    # final prompt gets the next phase number
    run_final_prompt(console, phase_num=len(phases) + 1)

    # the grand finale
    console.print("\n  [bold green]★ ENTERING THE MATRIX ★[/bold green]\n")
    time.sleep(1.0)
    run_matrix_rain()

"""Random text data pools for the hacking simulation.

All data is loaded at module import time from JSON and TXT files
in the ``assets/`` subpackage. This keeps data separate from logic
and makes it easy to customize the simulation by editing the files.

Data loading uses ``importlib.resources`` so it works correctly
with installed packages, editable installs, and PyInstaller bundles.
"""

import json
import random
import string
from importlib import resources

# ---------------------------------------------------------------------------
# Internal loaders
# ---------------------------------------------------------------------------


def _load_json(filename: str) -> list:
    """Load a JSON array from the assets directory.

    Args:
        filename: JSON file name inside the assets package.

    Returns:
        The parsed list from the JSON file.

    Raises:
        FileNotFoundError: If the asset file doesn't exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    source = resources.files("hacker_screen.assets").joinpath(filename)
    return json.loads(source.read_text(encoding="utf-8"))


def _load_text(filename: str) -> str:
    """Load a text file from the assets directory.

    Args:
        filename: Text file name inside the assets package.

    Returns:
        The full text content of the file.

    Raises:
        FileNotFoundError: If the asset file doesn't exist.
    """
    source = resources.files("hacker_screen.assets").joinpath(filename)
    return source.read_text(encoding="utf-8")


def _load_skulls() -> list[str]:
    """Load all skull ASCII art files from assets/skulls/.

    Reads every ``.txt`` file in the skulls subpackage, sorted by
    filename for deterministic ordering.

    Returns:
        A list of skull ASCII art strings.
    """
    skulls_pkg = resources.files("hacker_screen.assets.skulls")
    skull_files = sorted(f for f in skulls_pkg.iterdir() if f.name.endswith(".txt"))
    return [f.read_text(encoding="utf-8") for f in skull_files]


# ---------------------------------------------------------------------------
# Data pools — loaded from assets/ at import time
# ---------------------------------------------------------------------------

# fake ip addresses for network scans
FAKE_IPS: list[str] = _load_json("ips.json")

# system files and paths to "crack"
FAKE_FILES: list[str] = _load_json("files.json")

# common weak passwords for crack animations
FAKE_PASSWORDS: list[str] = _load_json("passwords.json")

# console messages for each hacking step
HACKING_STEPS: list[str] = _load_json("hacking_steps.json")

# malware payload names
MALWARE_NAMES: list[str] = _load_json("malware_names.json")

# target server names
TARGET_SERVERS: list[str] = _load_json("target_servers.json")

# encryption algorithms for cracking animations
ENCRYPTION_ALGOS: list[str] = _load_json("encryption_algos.json")

# network protocols for traffic simulation
NETWORK_PROTOCOLS: list[str] = _load_json("network_protocols.json")

# common port numbers for scanning
PORT_NUMBERS: list[int] = _load_json("ports.json")

# running system processes
SYSTEM_PROCESSES: list[str] = _load_json("system_processes.json")

# error messages for dramatic failures
ERROR_MESSAGES: list[str] = _load_json("error_messages.json")

# success messages for breakthroughs
SUCCESS_MESSAGES: list[str] = _load_json("success_messages.json")

# system info fields — varied OS, CPU, GPU, RAM, disk, etc.
SYSTEM_INFO: dict[str, list] = _load_json("system_info.json")

# varied typing messages for each phase
PHASE_MESSAGES: dict[str, list[str]] = _load_json("phase_messages.json")

# signal profiles for surveillance (label pairs + frequencies)
SIGNAL_PROFILES: list[dict] = _load_json("signal_profiles.json")

# small skull ascii art for dramatic moments
ASCII_SKULLS: list[str] = _load_skulls()

# welcome banner ascii art
WELCOME_BANNER: str = _load_text("banner.txt")


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def get_random_items(pool: list, n: int) -> list:
    """Pick n random items from a pool without replacement.

    Args:
        pool: The list to sample from.
        n: Number of items to pick. Clamped to pool size.

    Returns:
        A list of n randomly selected items.
    """
    n = min(n, len(pool))
    return random.sample(pool, n)


def get_random_ip() -> str:
    """Generate a random IP address on the fly.

    Returns:
        A string like '123.45.67.89'.
    """
    return ".".join(str(random.randint(1, 254)) for _ in range(4))


def get_random_hex(length: int = 32) -> str:
    """Generate a random hexadecimal string.

    Args:
        length: Number of hex characters to generate.

    Returns:
        A lowercase hex string of the given length.
    """
    return "".join(random.choices(string.hexdigits[:16], k=length))


def get_random_mac() -> str:
    """Generate a random MAC address.

    Returns:
        A string like 'a4:3b:c2:d1:e0:f9'.
    """
    return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))

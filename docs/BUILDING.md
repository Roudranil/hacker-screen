# Building Hacker Screen

Comprehensive guide to building, testing, and packaging the hacker-screen application on all supported platforms.

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------| 
| Python | 3.11+ | Runtime |
| [uv](https://docs.astral.sh/uv/) | latest | Package and dependency management |
| [PyInstaller](https://pyinstaller.org/) | 6.x | Binary packaging (installed as dev dep) |
| Git | any | Source checkout |

**Platform-specific:**
- **Linux** — No extra requirements. `curses` ships with the Python stdlib.
- **macOS** — No extra requirements. `curses` ships with macOS Python.
- **Windows** — `windows-curses` is automatically installed via the project dependencies when running on Windows.

---

## Running from Source

```bash
# 1. Clone the repo
git clone https://github.com/Roudranil/hacker-screen.git
cd hacker-screen

# 2. Install all dependencies (including dev tools)
uv sync

# 3. Run the application
uv run hacker-screen
```

> **Tip:** Your terminal must be at least **60 columns wide** and support **ANSI colors**. On Windows, use **Windows Terminal** for best results.

---

## Running Tests

```bash
# Run all tests (currently 134)
uv run pytest tests/ -v

# Run just the data loader tests
uv run pytest tests/test_data.py -v

# Run with short traceback for quick feedback
uv run pytest tests/ --tb=short

# Run with coverage (install pytest-cov first)
uv pip install pytest-cov
uv run pytest tests/ -v --cov=hacker_screen --cov-report=term-missing
```

### Test Breakdown

| File | Tests | Covers |
|------|-------|--------|
| `test_data.py` | 66 | JSON/TXT loaders, data pool integrity, type checks |
| `test_effects.py` | 25 | All 18 effect functions + helpers |
| `test_sequences.py` | 30 | Phase orchestration, RetryTracker, bonus selection, run_all |
| `test_matrix_rain.py` | 13 | Rain character set, column mechanics, curses wrapper |

### Linting

```bash
# Check for lint errors
uv run ruff check src/ tests/

# Auto-fix what can be fixed
uv run ruff check src/ tests/ --fix

# Format code
uv run ruff format src/ tests/
```

---

## Building a Binary

PyInstaller packages the Python application into a single standalone executable. The key requirement is including the `assets/` data files.

### Linux

```bash
uv sync

uv run pyinstaller \
  --onefile \
  --name hacker-screen \
  --add-data "src/hacker_screen/assets:hacker_screen/assets" \
  --collect-submodules rich._unicode_data \
  src/hacker_screen/__main__.py

# Test the binary
./dist/hacker-screen
```

### macOS

```bash
uv sync

uv run pyinstaller \
  --onefile \
  --name hacker-screen \
  --add-data "src/hacker_screen/assets:hacker_screen/assets" \
  --collect-submodules rich._unicode_data \
  src/hacker_screen/__main__.py

# Test the binary
./dist/hacker-screen
```

> **Note (macOS):** If you see a Gatekeeper warning, run:
> ```bash
> xattr -d com.apple.quarantine ./dist/hacker-screen
> ```

### Windows

```powershell
uv sync

uv run pyinstaller `
  --onefile `
  --name hacker-screen `
  --add-data "src\hacker_screen\assets;hacker_screen\assets" `
  --collect-submodules rich._unicode_data `
  src\hacker_screen\__main__.py

# Test the binary
.\dist\hacker-screen.exe
```

> **Important (Windows):** The `--add-data` separator is `;` (semicolon) on Windows, not `:` (colon).

---

## How Asset Bundling Works

The application stores all randomized data in external files under `src/hacker_screen/assets/`:

```
assets/
├── __init__.py              # marks this as a Python subpackage
├── banner.txt               # welcome banner ASCII art
├── encryption_algos.json    # AES, RSA, etc.
├── error_messages.json      # dramatic error strings
├── files.json               # fake file paths for cracking
├── hacking_steps.json       # exploitation step messages
├── ips.json                 # fake IP addresses
├── malware_names.json       # rootkit/trojan names
├── network_protocols.json   # TCP, UDP, ICMP, etc.
├── passwords.json           # fake passwords for cracking
├── phase_messages.json      # randomized messages per phase (12 categories)
├── ports.json               # port numbers for scanning
├── signal_profiles.json     # scanner + sine wave label/frequency configs (8 profiles)
├── success_messages.json    # dramatic success strings
├── system_info.json         # OS, CPU, GPU, disk for system intel display
├── system_processes.json    # fake running process names
├── target_servers.json      # target names for glitch text
└── skulls/
    ├── __init__.py
    ├── skull_01.txt
    ├── skull_02.txt
    └── skull_03.txt
```

These files are loaded at runtime via `importlib.resources`, which works with:
- **Editable installs** (`uv sync` / `pip install -e .`)
- **Wheel installs** (`pip install hacker-screen`)
- **PyInstaller bundles** (with `--add-data`)

### Customizing Data

Want to change what appears in the simulation? Just edit the JSON/TXT files directly:

```bash
# Add a new skull
vim src/hacker_screen/assets/skulls/skull_04.txt

# Add more fake IPs
vim src/hacker_screen/assets/ips.json

# Add new phase messages (must match existing keys)
vim src/hacker_screen/assets/phase_messages.json

# Add a new signal profile
vim src/hacker_screen/assets/signal_profiles.json
```

No code changes needed — the loader picks up new files automatically (skull files are auto-discovered; JSON files just need valid array/object structure).

### Phase Message Categories

The `phase_messages.json` file contains these categories:

| Key | Used By | Example |
|-----|---------|---------|
| `recon` | Reconnaissance | "Scanning target infrastructure..." |
| `exploitation` | Exploitation | "Injecting SQL payload..." |
| `exfil_tasks` | Data Exfiltration | "Database dump", "SSH keys" |
| `surveillance` | Surveillance | "Intercepting comms..." |
| `malware_cleanup` | Payload Deployment | "Sanitizing installation traces..." |
| `firewall_bypass` | Firewall Bypass | "ACCESS DENIED" |
| `firewall_steps` | Firewall Bypass | "Probing port %PORT%..." |
| `social_engineering` | Social Engineering | "Crafting phishing payload..." |
| `social_steps` | Social Engineering | "Deploying credential harvester..." |
| `cleanup` | Trace Cleanup | "Initiating forensic countermeasures..." |
| `cleanup_steps` | Trace Cleanup | "Wiping /var/log/auth.log..." |

---

## Phase Model

### Required Phases (always present, always in order)

| # | Phase | Effects Used |
|---|-------|-------------|
| — | Welcome | `show_welcome_banner` + `show_glitch_text` + `show_system_info` |
| 1+ | Exploitation | 5-8× `show_hacking_step` or `show_failure_retry` |
| 2+ | Cracking | 2-5× `show_password_crack` + `show_encryption_crack` + `show_progress_bar` |
| 3+ | Payload Deployment | 3-6× `show_hacking_step` or `show_failure_retry` + 2× `show_progress_bar` |
| last | Final Sequence | `show_permission_prompt` (tiled skulls) + `show_countdown` → Matrix Rain |

### Bonus Phase Pool (randomly selected to fill remaining slots)

| Phase | Probability | Max per run |
|-------|-------------|-------------|
| Reconnaissance | 65% | 1 |
| Data Exfiltration | 55% | 1 |
| Surveillance | 50% | 1 |
| Trace Cleanup | 40% | 1 |
| Firewall Bypass | 30% | 1 |
| Social Engineering | 25% | 1 |

**Total cap:** max 8 phases (required 3 + final 1 + up to 4 bonus).

### Retry System

- `RetryTracker` class shared across all phases in a run
- **Per-phase cap:** max 2 retries
- **Global cap:** max 3 retries across entire simulation

---

## GitHub Actions CI

The project includes a CI workflow at `.github/workflows/build.yml` that:

1. **Runs tests and lint** on every tagged push
2. **Builds binaries** for Linux and Windows
3. **Creates a GitHub Release** with the binaries attached

### Triggering a Release

```bash
# Tag a release
git tag v1.1.0
git push origin v1.1.0
```

This triggers the workflow, which:
- Checks out the code
- Installs uv and Python 3.11
- Runs `uv sync`, `pytest`, and `ruff check`
- Builds PyInstaller binaries for each platform
- Uploads them as GitHub Release assets

### Manual Trigger

You can also trigger the workflow manually from the GitHub Actions tab using **"Run workflow"** → `workflow_dispatch`.

### Adding macOS Builds

To add macOS, expand the matrix in `build.yml`:

```yaml
matrix:
  include:
    - os: ubuntu-latest
      artifact_name: hacker-screen-linux
      binary_name: hacker-screen
    - os: windows-latest
      artifact_name: hacker-screen-windows
      binary_name: hacker-screen.exe
    - os: macos-latest                    # ← add this
      artifact_name: hacker-screen-macos
      binary_name: hacker-screen
```

### Testing GH Actions Locally

Use [act](https://github.com/nektos/act) to run workflows locally in Docker:

```bash
# install
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# run the default push event
act push

# run a specific workflow
act -W .github/workflows/build.yml

# dry-run (just show what would execute)
act -n
```

---

## Verifying a Built Binary

After building, verify the binary works correctly:

```bash
# 1. Check it runs
./dist/hacker-screen

# 2. Verify assets are bundled (should see system info, IP addresses, etc.)
#    If assets are missing, you'll get a FileNotFoundError at startup.

# 3. Check binary size (should be ~15-25 MB depending on platform)
ls -lh dist/hacker-screen

# 4. Test on a clean machine (no Python installed)
#    Copy the binary to another machine and run it.
#    This is the best test for PyInstaller bundles.
```

---

## Troubleshooting

### `FileNotFoundError: assets/ips.json`
The `--add-data` flag was missing or incorrect when building with PyInstaller. Rebuild with:
```bash
--add-data "src/hacker_screen/assets:hacker_screen/assets"
```

### `Terminal too narrow` error
The simulation requires at least 60 columns. Maximize your terminal or reduce font size.

### Garbled output / no colors
Ensure your terminal supports ANSI escape codes. On Windows, use **Windows Terminal**, **PowerShell 7+**, or **Git Bash**. The legacy `cmd.exe` has limited color support.

### `ModuleNotFoundError: No module named '_curses'` (Windows)
The `windows-curses` package should be installed automatically. If not:
```bash
uv pip install windows-curses
```

### Matrix rain doesn't render properly
- Ensure your terminal supports Unicode (the rain uses katakana characters).
- Try a different terminal emulator if characters appear as boxes.
- Font recommendation: **JetBrains Mono**, **Fira Code**, or any Nerd Font.

### PyInstaller build is very slow
First builds take longer because PyInstaller analyzes all imports. Subsequent builds use a cache in the `build/` directory. To speed things up:
```bash
# Clean previous build artifacts
rm -rf build/ dist/ *.spec

# Rebuild
uv run pyinstaller --onefile --name hacker-screen \
  --add-data "src/hacker_screen/assets:hacker_screen/assets" \
  src/hacker_screen/__main__.py
```

### Windows SmartScreen blocks the binary
The binary is unsigned. Click **"More info" → "Run anyway"** to proceed.

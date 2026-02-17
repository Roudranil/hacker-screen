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
git clone https://github.com/your-repo/hacker-screen.git
cd hacker-screen

# 2. Install all dependencies (including dev tools)
uv sync

# 3. Run the application
uv run hacker-screen
```

> **Tip:** Your terminal must be at least **60 columns wide** and support **ANSI colors**.

---

## Running Tests

```bash
# Run all tests (currently 114)
uv run pytest tests/ -v

# Run just the data loader tests
uv run pytest tests/test_data.py -v

# Run with short traceback for quick feedback
uv run pytest tests/ --tb=short

# Run with coverage (install pytest-cov first)
uv pip install pytest-cov
uv run pytest tests/ -v --cov=hacker_screen --cov-report=term-missing
```

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
  src\hacker_screen\__main__.py

# Test the binary
.\dist\hacker-screen.exe
```

> **Important (Windows):** The `--add-data` separator is `;` (semicolon) on Windows, not `:` (colon).

---

## How Asset Bundling Works

The application stores all randomized data (IP addresses, passwords, ASCII art, etc.) in external files under `src/hacker_screen/assets/`:

```
assets/
├── __init__.py          # marks this as a Python subpackage
├── banner.txt           # welcome banner ASCII art
├── encryption_algos.json
├── error_messages.json
├── files.json
├── hacking_steps.json
├── ips.json
├── malware_names.json
├── network_protocols.json
├── passwords.json
├── ports.json
├── success_messages.json
├── system_info.json     # OS, CPU, GPU, disk, etc. for system intel display
├── system_processes.json
├── target_servers.json
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

# Add more system info variety
vim src/hacker_screen/assets/system_info.json
```

No code changes needed — the loader picks up new files automatically.

---

## GitHub Actions CI

The project includes a CI workflow at `.github/workflows/build.yml` that:

1. **Runs tests and lint** on every tagged push
2. **Builds binaries** for Linux and Windows
3. **Creates a GitHub Release** with the binaries attached

### Triggering a Release

```bash
# Tag a release
git tag v1.0.0
git push origin v1.0.0
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

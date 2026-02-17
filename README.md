# 💀 Hacker Screen

> An over-the-top terminal hacking simulation with Matrix rain effect.
> Because every developer deserves to feel like a movie hacker.

## ✨ Features

Every run is **unique** — phases, messages, failures, and effects are all randomized.

### Required Phases (always present)
- **Welcome** — dramatic ASCII art with glitch text reveal + system intel
- **Exploitation** — SQL injection, privilege escalation, backdoor installation (with random failures)
- **Password Cracking** — animated asterisk fill, plaintext reveal, brute-force hash collision
- **Payload Deployment** — rootkit installation, malware persistence, log wiping (with random failures)
- **Final Sequence** — tiled skull art, "Hack it?" prompt, countdown → Matrix rain

### Bonus Phases (randomly selected, up to 4 per run)
- **Reconnaissance** (65%) — port scanning, network traffic capture, host discovery
- **Data Exfiltration** (55%) — file tree browsing, hex dumps, download progress bars
- **Surveillance** (50%) — scanner sweep + sine wave audio intercept (side-by-side)
- **Trace Cleanup** (40%) — log wiping, forensic evidence sanitization
- **Firewall Bypass** (30%) — IDS evasion with failures and retries
- **Social Engineering** (25%) — credential phishing simulation

### Safeguards
- **Max 8 phases** per run (4 required + up to 4 bonus)
- **Max 2 retries per phase**, **3 retries globally** — failures add tension without overwhelming

## 🚀 Quick Start

### From binary (no Python needed)

Download the latest binary from [Releases](https://github.com/Roudranil/hacker-screen/releases) and run:

```bash
# linux
chmod +x hacker-screen
./hacker-screen

# windows (use Windows Terminal for best results)
.\hacker-screen.exe
```

### From source (requires Python 3.11+ and uv)

```bash
git clone https://github.com/Roudranil/hacker-screen.git
cd hacker-screen
uv sync
uv run hacker-screen
```

**Press any key** to exit the matrix rain. **Ctrl+C** to quit at any time.

## 🏗️ Building the Binary

```bash
uv sync

# linux/macOS
uv run pyinstaller --onefile --name hacker-screen \
  --add-data "src/hacker_screen/assets:hacker_screen/assets" \
  --collect-submodules rich._unicode_data \
  src/hacker_screen/__main__.py

# windows (note: semicolon separator)
uv run pyinstaller --onefile --name hacker-screen `
  --add-data "src\hacker_screen\assets;hacker_screen\assets" `
  --collect-submodules rich._unicode_data `
  src\hacker_screen\__main__.py

# binary appears in dist/
./dist/hacker-screen
```

> **Note:** PyInstaller builds platform-specific binaries. Build on Linux for
> Linux, on Windows for Windows. See **[docs/BUILDING.md](docs/BUILDING.md)**
> for full platform-specific instructions, CI setup, and troubleshooting.

## 🧪 Running Tests

```bash
# run all 134 tests
uv run pytest tests/ -v

# with coverage
uv run pytest tests/ -v --cov=hacker_screen

# lint
uv run ruff check src/ tests/
```

## 📁 Project Structure

```
hacker-screen/
├── pyproject.toml              # project config, deps, ruff, pytest
├── README.md
├── docs/
│   ├── ARCHITECTURE.md         # module design & data flow
│   ├── BUILDING.md             # build, test, and packaging guide
│   └── EFFECTS_CATALOG.md      # visual catalog of all effects
├── src/hacker_screen/
│   ├── __init__.py             # package metadata
│   ├── __main__.py             # entry point
│   ├── data.py                 # loads data pools from assets/
│   ├── effects.py              # 18 terminal effect functions
│   ├── sequences.py            # phase orchestration + RetryTracker
│   ├── matrix_rain.py          # curses-based matrix rain
│   └── assets/                 # external data files (JSON + TXT)
│       ├── ips.json, files.json, ...   # 13 JSON data pools
│       ├── phase_messages.json         # randomized phase messages
│       ├── signal_profiles.json        # signal graph configurations
│       ├── banner.txt                  # welcome banner ASCII art
│       └── skulls/                     # skull ASCII art files
└── tests/
    ├── conftest.py             # shared fixtures
    ├── test_data.py            # 66 data pool + loader tests
    ├── test_effects.py         # 25 effect tests
    ├── test_sequences.py       # 30 sequence + retry tests
    └── test_matrix_rain.py     # 13 rain tests
```

## 🎨 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11+ | Runtime |
| [Rich](https://github.com/Textualize/rich) | Terminal styling, panels, progress bars, live display |
| [tqdm](https://github.com/tqdm/tqdm) | Classic progress bars |
| curses | Matrix rain per-cell rendering |
| [uv](https://github.com/astral-sh/uv) | Package management |
| [ruff](https://github.com/astral-sh/ruff) | Linting |
| pytest | Testing |
| PyInstaller | Binary packaging |

## ⚠️ Requirements

- Terminal width ≥ 60 columns
- Terminal with color support (most modern terminals)
- Python 3.11+ (for running from source)
- **Windows:** Use **Windows Terminal** (not legacy cmd.exe) for proper colors and Unicode

## 🙏 Credits

Built with ❤️ by **Rudy**.

Powered by [**Antigravity**](https://github.com/google-deepmind) and **Claude Opus 4.6** by Anthropic.

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

*Disclaimer: This is a fun simulation. No actual hacking occurs. Don't use this
to scare your coworkers. Or do. We won't judge.*

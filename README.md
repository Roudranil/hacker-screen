# 💀 Hacker Screen

> An over-the-top terminal hacking simulation with Matrix rain effect.
> Because every developer deserves to feel like a movie hacker.

## ✨ Features

- **Welcome Banner** — dramatic ASCII art with glitch text reveal
- **Reconnaissance** — port scanning, network traffic capture, host discovery
- **Exploitation** — SQL injection, privilege escalation, backdoor installation
- **Password Cracking** — animated asterisk fill + plaintext reveal
- **Data Exfiltration** — file tree browsing, hex dumps, download progress bars
- **Surveillance** — sine wave signal graphs, audio spectrum analyzer
- **Malware Deployment** — rootkit installation, log wiping
- **Final Sequence** — "Hack it?" prompt, password entry, countdown
- **Matrix Rain** — the iconic green character rain (katakana + latin)

All effects are randomized — every run is unique.

## 🚀 Quick Start

### From source (requires Python 3.11+ and uv)

```bash
# clone and install
git clone https://github.com/your-repo/hacker-screen.git
cd hacker-screen
uv sync

# run it
uv run hacker-screen
```

### From binary (no Python needed)

Download the latest binary from [Releases](https://github.com/your-repo/hacker-screen/releases) and run:

```bash
# linux
chmod +x hacker-screen
./hacker-screen

# windows
hacker-screen.exe
```

**Press any key** to exit the matrix rain. **Ctrl+C** to quit at any time.

## 🏗️ Building the Binary

```bash
# install dev dependencies
uv sync

# build (linux/macOS)
uv run pyinstaller --onefile --name hacker-screen \
  --add-data "src/hacker_screen/assets:hacker_screen/assets" \
  src/hacker_screen/__main__.py

# binary appears in dist/
./dist/hacker-screen
```

> **Note:** PyInstaller builds platform-specific binaries. Build on Linux for
> Linux, on Windows for Windows. See **[docs/BUILDING.md](docs/BUILDING.md)**
> for full platform-specific instructions, CI setup, and troubleshooting.

## 🧪 Running Tests

```bash
# run all 114 tests
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
│   ├── effects.py              # 17 terminal effect functions
│   ├── sequences.py            # 9 hacking phases
│   ├── matrix_rain.py          # curses-based matrix rain
│   └── assets/                 # external data files (JSON + TXT)
│       ├── ips.json, files.json, ...  # 13 JSON data pools
│       ├── banner.txt          # welcome banner ASCII art
│       └── skulls/             # skull ASCII art files
└── tests/
    ├── conftest.py             # shared fixtures
    ├── test_data.py            # 62 data pool + loader tests
    ├── test_effects.py         # 21 effect tests
    ├── test_sequences.py       # 14 sequence tests
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

## 🙏 Credits

Built with ❤️ by **Rudy**.

Powered by [**Antigravity**](https://github.com/google-deepmind) and **Claude Opus 4.6** by Anthropic.

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

*Disclaimer: This is a fun simulation. No actual hacking occurs. Don't use this
to scare your coworkers. Or do. We won't judge.*

# Architecture

## Module Dependency Graph

```
__main__.py
    └── sequences.py        ← orchestration + RetryTracker
            ├── effects.py   ← 18 terminal effect functions
            │       └── data.py  ← loads pools from assets/
            └── matrix_rain.py   ← curses-based final rain
```

## Data Flow

1. **`__main__.py`** creates a `Rich Console` and calls `run_all()`
2. **`sequences.py`** creates a `RetryTracker`, selects bonus phases, and runs 5-8 phases with auto-numbered headers
3. **`effects.py`** renders individual visual effects using Rich (panels, progress, live, tables, trees)
4. **`data.py`** provides random text pools + structured data (`PHASE_MESSAGES`, `SIGNAL_PROFILES`) sampled by effects
5. **`matrix_rain.py`** takes over the terminal with `curses` for the final rain effect

## Phase Model

```
Welcome (no number)
  ↓
┌─────────────────────────────────────────────────────┐
│  REQUIRED (always present, always in order):        │
│    Exploitation → Cracking → Payload Deployment     │
│                                                     │
│  BONUS (randomly selected, inserted between above): │
│    Recon, Data Exfil, Surveillance,                 │
│    Firewall Bypass, Social Engineering, Cleanup     │
│                                                     │
│  Cap: max 8 phases total (3 required + 1 final +    │
│       up to 4 bonus)                                │
└─────────────────────────────────────────────────────┘
  ↓
Final Sequence → Matrix Rain
```

### Retry System

`RetryTracker` is shared across all phases in a single run:
- **Per-phase cap:** max 2 retries (reset each phase)
- **Global cap:** max 3 retries (never reset)
- `_maybe_fail()` helper checks both caps before triggering `show_failure_retry()`

## Design Decisions

### Rich vs curses split
- **Rich** handles the hacking simulation (all phases): panels, styled text, progress bars, tables, live updates
- **curses** handles the matrix rain: needs per-cell character placement at 25fps, which Rich's Live display can't do efficiently

### Randomization
- Every run feels different: random bonus phase selection, random message sampling, random failures with retry caps
- `data.py` pools are large enough (15-32 items each) to avoid repetition across runs
- `phase_messages.json` provides 12 message categories with 5-10 alternatives each
- `signal_profiles.json` stores 8 scanner/sine wave configurations

### Skull tiling
- `show_permission_prompt` tiles a random skull side-by-side to fill the terminal width
- Computes skull width, calculates fitting copies, pads and joins lines horizontally

### Testability
- Effects accept a `Console` parameter → inject a `StringIO`-backed console in tests
- `time.sleep` is patched in all effect/sequence tests for instant execution
- Matrix rain tested via mocked `curses.wrapper` (can't run curses in CI)
- `RetryTracker` has isolated unit tests for both caps
- `_select_bonus_phases` is tested for max-slot enforcement
- `run_all` mocks bonus selection to isolate required-phase testing

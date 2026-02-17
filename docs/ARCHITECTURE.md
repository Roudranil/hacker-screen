# Architecture

## Module Dependency Graph

```
__main__.py
    └── sequences.py
            ├── effects.py
            │       └── data.py
            └── matrix_rain.py
```

## Data Flow

1. **`__main__.py`** creates a `Rich Console` and calls `run_all()`
2. **`sequences.py`** orchestrates 7 hacking phases in order, each calling multiple effects
3. **`effects.py`** renders individual visual effects using Rich (panels, progress, live, tables, trees)
4. **`data.py`** provides random text pools sampled by effects
5. **`matrix_rain.py`** takes over the terminal with `curses` for the final rain effect

## Design Decisions

### Rich vs curses split
- **Rich** handles the hacking simulation (phases 1-7): panels, styled text, progress bars, tables, live updates
- **curses** handles the matrix rain: needs per-cell character placement at 25fps, which Rich's Live display can't do efficiently

### Randomization
- Every run feels different: random data pool sampling, random effect durations, random success/failure outcomes
- `data.py` pools are large enough (15-32 items each) to avoid repetition across runs

### Testability
- Effects accept a `Console` parameter → inject a `StringIO`-backed console in tests
- `time.sleep` is patched in all effect/sequence tests for instant execution
- Matrix rain tested via mocked `curses.wrapper` (can't run curses in CI)

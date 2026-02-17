# Effects Catalog

Every effect function lives in `effects.py` and accepts a `Rich Console` as its first argument.

## Text Effects

| Effect | Function | Description |
|--------|----------|-------------|
| Typing | `typing_effect()` | Character-by-character text reveal with configurable delay |
| Glitch Text | `show_glitch_text()` | Random character swaps gradually resolving to target text |

## Banners & Info

| Effect | Function | Description |
|--------|----------|-------------|
| Welcome Banner | `show_welcome_banner()` | Large ASCII art "HACKER NETHING" in a styled panel |
| System Info | `show_system_info()` | Fake OS/CPU/RAM/IP table for a target server |

## Hacking Steps

| Effect | Function | Description |
|--------|----------|-------------|
| Hacking Step | `show_hacking_step()` | Rich spinner + message for configurable duration |
| Password Crack | `show_password_crack()` | Asterisks fill in, then reveal plaintext password |
| Encryption Crack | `show_encryption_crack()` | Scrolling hex hash attempts, final collision found |
| Failure Retry | `show_failure_retry()` | Red FAILED → pause → yellow retry → green success |

## Progress & Downloads

| Effect | Function | Description |
|--------|----------|-------------|
| Progress Bar | `show_progress_bar()` | tqdm-style bar with `░▒█` characters |
| Rich Progress | `show_rich_progress()` | Multiple concurrent Rich progress bars |

## Network & Scanning

| Effect | Function | Description |
|--------|----------|-------------|
| Port Scan | `show_port_scan()` | Ports scanned with open/closed/filtered results |
| Network Traffic | `show_network_traffic()` | Packet capture table with src, dst, proto, size |

## Surveillance & Signals

| Effect | Function | Description |
|--------|----------|-------------|
| Dual Signal Graph | `show_dual_signal_graph()` | Side-by-side: horizontal scanner sweep (left) + sine wave (right) |
| Signal Graph | `show_signal_graph()` | Single ASCII sine wave graph (standalone) |

### Dual Signal Graph Details

The left panel uses `_build_scan_line()` — a bright bar sweeps left-to-right with a fading trail and random noise. The right panel uses `_build_sine_wave()` — a classic sinusoidal waveform.

Parameters are loaded from `signal_profiles.json` (8 profiles), each with:
- `left_label` / `right_label` — panel headers
- `scan_speed` — sweep speed for the scanner
- `wave_freq` / `wave_speed` — sine wave frequency and animation speed

## Data & Memory

| Effect | Function | Description |
|--------|----------|-------------|
| Hex Dump | `show_hex_dump()` | Memory inspection with hex + ASCII columns |
| File Tree | `show_file_tree()` | Animated Rich Tree exploring remote filesystem |

## Final Sequence

| Effect | Function | Description |
|--------|----------|-------------|
| Permission Prompt | `show_permission_prompt()` | Tiled skull art filling terminal width + password entry |
| Countdown | `show_countdown()` | 10-second countdown with green→yellow→red color shift |

## Phase → Effect Mapping

### Required Phases

| Phase | Effects |
|-------|---------|
| Welcome | `show_welcome_banner` + `show_glitch_text` + `show_system_info` |
| Exploitation | 5-8× `show_hacking_step` or `show_failure_retry` (20% fail chance, capped) |
| Cracking | 2-5× `show_password_crack` + 1× `show_encryption_crack` + `show_progress_bar` |
| Payload Deployment | 3-6× `show_hacking_step` or `show_failure_retry` (15% fail chance, capped) + 2× `show_progress_bar` |
| Final Sequence | `show_permission_prompt` (tiled skulls) + `show_countdown` → Matrix Rain |

### Bonus Phases

| Phase | Effects |
|-------|---------|
| Reconnaissance | `show_port_scan` + `show_network_traffic` + host discovery list |
| Data Exfiltration | `show_file_tree` + `show_hex_dump` + `show_rich_progress` |
| Surveillance | `show_dual_signal_graph` (scanner + sine wave) |
| Firewall Bypass | 3× `show_hacking_step` or `show_failure_retry` (30% fail chance, capped) |
| Social Engineering | 2-4× `show_hacking_step` + `show_progress_bar` |
| Trace Cleanup | 3-5× `show_hacking_step` + `show_progress_bar` |

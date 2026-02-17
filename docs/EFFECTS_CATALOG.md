# Effects Catalog

Every effect function lives in `effects.py` and accepts a `Rich Console` as its first argument.

## Text Effects

| Effect | Function | Description |
|--------|----------|-------------|
| Typing | `typing_effect()` | Character-by-character text reveal with delay |
| Glitch Text | `show_glitch_text()` | Random character swaps gradually resolving to target text |

## Banners & Info

| Effect | Function | Description |
|--------|----------|-------------|
| Welcome Banner | `show_welcome_banner()` | Large ASCII art "HACKER NETHING" in a styled panel |
| System Info | `show_system_info()` | Fake OS/CPU/RAM/IP table for a target server |

## Hacking Steps

| Effect | Function | Description |
|--------|----------|-------------|
| Hacking Step | `show_hacking_step()` | Spinner + message, randomly succeeds (85%) or fails with retry |
| Password Crack | `show_password_crack()` | Asterisks fill in, then reveal plaintext password |
| Encryption Crack | `show_encryption_crack()` | Scrolling hex hash attempts, final collision found |

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
| Signal Graph | `show_signal_graph()` | Live ASCII sine wave (SIGINT intercept) |
| Bar Graph | `show_bar_graph()` | Animated vertical bar chart (audio spectrum) |

## Data & Memory

| Effect | Function | Description |
|--------|----------|-------------|
| Hex Dump | `show_hex_dump()` | Memory inspection with hex + ASCII columns |
| File Tree | `show_file_tree()` | Animated Rich Tree exploring remote filesystem |

## Final Sequence

| Effect | Function | Description |
|--------|----------|-------------|
| Permission Prompt | `show_permission_prompt()` | Skull art + "EXECUTE FINAL HACK?" + password entry |
| Countdown | `show_countdown()` | 10-second countdown with green→yellow→red color |

## Sequence Phases

Effects are chained into 7 phases by `sequences.py`:

1. **Welcome** → `show_welcome_banner` + `show_glitch_text` + `show_system_info`
2. **Recon** → `show_port_scan` + `show_network_traffic`
3. **Exploitation** → 5-7× `show_hacking_step`
4. **Cracking** → 3× `show_password_crack` + `show_encryption_crack` + `show_progress_bar`
5. **Data Exfil** → `show_file_tree` + `show_hex_dump` + `show_rich_progress`
6. **Surveillance** → 2× `show_signal_graph` + `show_bar_graph`
7. **Malware** → 4× `show_hacking_step` + 2× `show_progress_bar`
8. **Final** → `show_permission_prompt` + `show_countdown` → Matrix Rain

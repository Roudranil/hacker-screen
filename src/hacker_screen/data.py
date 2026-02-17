"""Random text data pools for the hacking simulation.

Contains extensive collections of fake IPs, file paths, passwords,
hacking step messages, and other text used to make the simulation
feel varied and realistic. Every run pulls random items from these pools.
"""

import random
import string

# fake ip addresses for network scans
FAKE_IPS: list[str] = [
    "192.168.0.42",
    "10.0.13.37",
    "172.16.255.1",
    "203.0.113.66",
    "198.51.100.7",
    "10.10.10.1",
    "192.168.1.100",
    "172.31.0.99",
    "10.0.0.137",
    "192.168.50.25",
    "203.0.113.200",
    "198.51.100.42",
    "10.255.255.1",
    "172.16.0.13",
    "192.168.100.77",
    "10.0.42.69",
    "172.20.10.5",
    "192.168.69.1",
    "10.13.37.42",
    "172.16.100.200",
    "8.8.8.8",
    "1.1.1.1",
    "9.9.9.9",
    "208.67.222.222",
    "45.33.32.156",
]

# system files and paths to "crack"
FAKE_FILES: list[str] = [
    "/etc/shadow",
    "/etc/passwd",
    "/var/lib/mysql/users.db",
    "/root/.ssh/id_rsa",
    "/home/admin/.bash_history",
    "/var/log/auth.log",
    "/opt/secrets/vault.enc",
    "/tmp/.hidden/keylog.dat",
    "/srv/classified/top_secret.gpg",
    "/usr/local/bin/backdoor.sh",
    "C:\\Windows\\System32\\config\\SAM",
    "C:\\Users\\Admin\\Documents\\passwords.xlsx",
    "C:\\ProgramData\\ssh\\ssh_host_rsa_key",
    "/proc/self/mem",
    "/dev/sda1",
    "/sys/kernel/security/apparmor",
    "/var/spool/cron/crontabs/root",
    "/etc/ssl/private/server.key",
    "/opt/oracle/product/db/wallet.p12",
    "/backup/full_dump_2024.sql.gz",
]

# common weak passwords for crack animations
FAKE_PASSWORDS: list[str] = [
    "P@55w0rd!",
    "hunter2",
    "letmein2024",
    "admin123!@#",
    "qwerty",
    "password123",
    "iloveyou",
    "trustno1",
    "monkey",
    "dragon",
    "master",
    "abc123",
    "shadow",
    "1234567890",
    "access14",
    "flower",
    "superman1",
    "michael1",
    "!@#$%^&*",
    "correct-horse-battery-staple",
]

# console messages for each hacking step
HACKING_STEPS: list[str] = [
    "Bypassing firewall...",
    "Injecting SQL payload...",
    "Escalating privileges...",
    "Spoofing MAC address...",
    "Tunneling through VPN...",
    "Brute-forcing SSH keys...",
    "Deploying zero-day exploit...",
    "Intercepting TLS handshake...",
    "Overwriting kernel module...",
    "Planting rootkit in /boot...",
    "Exfiltrating database dump...",
    "Cracking WPA2 handshake...",
    "Sniffing network packets...",
    "Hijacking DNS resolver...",
    "Forging authentication tokens...",
    "Injecting shellcode into memory...",
    "Disabling intrusion detection...",
    "Corrupting audit logs...",
    "Pivoting to internal network...",
    "Establishing reverse shell...",
    "Extracting session cookies...",
    "Dumping LSASS process memory...",
    "Bypassing two-factor auth...",
    "Patching binary on the fly...",
    "Embedding persistence hook...",
]

# malware payload names
MALWARE_NAMES: list[str] = [
    "rootkit_v3.bin",
    "keylogger.so",
    "cryptominer.wasm",
    "backdoor.elf",
    "ransomware_payload.enc",
    "trojan_horse.dll",
    "worm_spreader.py",
    "spyware_agent.deb",
    "botnet_node.rpm",
    "exploit_kit.tar.gz",
    "stealth_miner.sh",
    "data_exfil.jar",
    "rat_controller.exe",
    "dns_tunneler.go",
    "fileless_implant.ps1",
]

# target server names
TARGET_SERVERS: list[str] = [
    "pentagon-mainframe",
    "nsa-archive-07",
    "cia-blackops-db",
    "mi6-comms-relay",
    "kremlin-sat-net",
    "interpol-central",
    "echelon-node-13",
    "area51-research",
    "nato-command",
    "gchq-sigint-hub",
    "fbi-case-files",
    "darpa-project-x",
    "norad-defense",
    "cybercom-ops",
    "mossad-intel",
]

# encryption algorithms for cracking animations
ENCRYPTION_ALGOS: list[str] = [
    "AES-256-GCM",
    "RSA-4096",
    "ChaCha20-Poly1305",
    "Blowfish-CBC",
    "Twofish-256",
    "3DES-EDE",
    "Serpent-256",
    "Camellia-256",
    "CAST-256",
    "IDEA-128",
    "RC4-256",
    "Salsa20",
    "XTEA",
    "SHA-512",
    "bcrypt(cost=14)",
]

# network protocols for traffic simulation
NETWORK_PROTOCOLS: list[str] = [
    "SSH",
    "TLS 1.3",
    "WireGuard",
    "Tor",
    "I2P",
    "TCP",
    "UDP",
    "ICMP",
    "HTTP/2",
    "DNS",
    "SMTP",
    "FTP",
    "SNMP",
    "RDP",
    "SMB",
]

# common port numbers for scanning
PORT_NUMBERS: list[int] = [
    22,
    23,
    25,
    53,
    80,
    110,
    135,
    139,
    143,
    443,
    445,
    993,
    995,
    1337,
    1433,
    1521,
    2049,
    3306,
    3389,
    5432,
    5900,
    6379,
    6667,
    8080,
    8443,
    8888,
    9090,
    9200,
    27017,
    31337,
    49152,
    51820,
]

# running system processes
SYSTEM_PROCESSES: list[str] = [
    "sshd",
    "nginx",
    "postgres",
    "kernel_worker",
    "systemd",
    "cron",
    "docker",
    "containerd",
    "kube-proxy",
    "redis-server",
    "mysqld",
    "apache2",
    "openvpn",
    "tor",
    "fail2ban",
]

# error messages for dramatic failures
ERROR_MESSAGES: list[str] = [
    "ACCESS DENIED",
    "SEGFAULT AT 0xDEADBEEF",
    "PERMISSION DENIED",
    "CONNECTION REFUSED",
    "TIMEOUT EXCEEDED",
    "AUTHENTICATION FAILED",
    "BUFFER OVERFLOW DETECTED",
    "KERNEL PANIC",
    "STACK SMASHING DETECTED",
    "INVALID CERTIFICATE",
    "CHECKSUM MISMATCH",
    "ENCRYPTION KEY EXPIRED",
]

# success messages for breakthroughs
SUCCESS_MESSAGES: list[str] = [
    "ACCESS GRANTED",
    "FIREWALL BYPASSED",
    "ROOT SHELL OBTAINED",
    "DECRYPTION COMPLETE",
    "PAYLOAD DELIVERED",
    "PERSISTENCE ESTABLISHED",
    "DATA EXFILTRATED",
    "BACKDOOR INSTALLED",
    "PRIVILEGE ESCALATION SUCCESSFUL",
    "AUTHENTICATION BYPASSED",
    "INTRUSION DETECTION DISABLED",
    "EXPLOIT SUCCEEDED",
]

# small skull ascii art for dramatic moments
ASCII_SKULLS: list[str] = [
    r"""
     ____
    /    \
   | o  o |
   |  __  |
    \____/
    """,
    r"""
      ___
     /   \
    |() ()|
     \ ^ /
      |_|
    """,
    r"""
    .----.
    |x  x|
    | /\ |
    '----'
    """,
]

# welcome banner ascii art
WELCOME_BANNER: str = r"""
 ██░ ██  ▄▄▄       ▄████▄   ██ ▄█▀▓█████  ██▀███
▓██░ ██▒▒████▄    ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
▒██▀▀██░▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
░▓█ ░██ ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄
░▓█▒░██▓ ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒
 ▒ ░░▒░▒ ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
 ▒ ░▒░ ░  ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
 ░  ░░ ░  ░   ▒   ░        ░ ░░ ░    ░     ░░   ░
 ░  ░  ░      ░  ░░ ░      ░  ░      ░  ░   ░
                   ░
 ███▄    █ ▓█████▄▄▄█████▓ ██░ ██  ██▓ ███▄    █   ▄████
 ██ ▀█   █ ▓█   ▀▓  ██▒ ▓▒▓██░ ██▒▓██▒ ██ ▀█   █  ██▒ ▀█▒
▓██  ▀█ ██▒▒███  ▒ ▓██░ ▒░▒██▀▀██░▒██▒▓██  ▀█ ██▒▒██░▄▄▄░
▓██▒  ▐▌██▒▒▓█  ▄░ ▓██▓ ░ ░▓█ ░██ ░██░▓██▒  ▐▌██▒░▓█  ██▓
▒██░   ▓██░░▒████▒ ▒██▒ ░ ░▓█▒░██▓░██░▒██░   ▓██░░▒▓███▀▒
░ ▒░   ▒ ▒ ░░ ▒░ ░ ▒ ░░    ▒ ░░▒░▒░▓  ░ ▒░   ▒ ▒  ░▒   ▒
░ ░░   ░ ▒░ ░ ░  ░   ░     ▒ ░▒░ ░ ▒ ░░ ░░   ░ ▒░  ░   ░
   ░   ░ ░    ░    ░       ░  ░░ ░ ▒ ░   ░   ░ ░ ░ ░   ░
         ░    ░  ░          ░  ░  ░ ░           ░       ░
"""


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

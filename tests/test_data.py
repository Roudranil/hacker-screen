"""Tests for the data module — pools, helpers, and random generators."""

import re

from hacker_screen.data import (
    ASCII_SKULLS,
    ENCRYPTION_ALGOS,
    ERROR_MESSAGES,
    FAKE_FILES,
    FAKE_IPS,
    FAKE_PASSWORDS,
    HACKING_STEPS,
    MALWARE_NAMES,
    NETWORK_PROTOCOLS,
    PORT_NUMBERS,
    SUCCESS_MESSAGES,
    SYSTEM_PROCESSES,
    TARGET_SERVERS,
    WELCOME_BANNER,
    get_random_hex,
    get_random_ip,
    get_random_items,
    get_random_mac,
)


class TestDataPools:
    """Verify all data pools are populated and have variety."""

    def test_fake_ips_not_empty(self) -> None:
        assert len(FAKE_IPS) >= 20

    def test_fake_files_not_empty(self) -> None:
        assert len(FAKE_FILES) >= 15

    def test_fake_passwords_not_empty(self) -> None:
        assert len(FAKE_PASSWORDS) >= 15

    def test_hacking_steps_not_empty(self) -> None:
        assert len(HACKING_STEPS) >= 20

    def test_malware_names_not_empty(self) -> None:
        assert len(MALWARE_NAMES) >= 10

    def test_target_servers_not_empty(self) -> None:
        assert len(TARGET_SERVERS) >= 10

    def test_encryption_algos_not_empty(self) -> None:
        assert len(ENCRYPTION_ALGOS) >= 10

    def test_network_protocols_not_empty(self) -> None:
        assert len(NETWORK_PROTOCOLS) >= 10

    def test_port_numbers_not_empty(self) -> None:
        assert len(PORT_NUMBERS) >= 20

    def test_system_processes_not_empty(self) -> None:
        assert len(SYSTEM_PROCESSES) >= 10

    def test_error_messages_not_empty(self) -> None:
        assert len(ERROR_MESSAGES) >= 10

    def test_success_messages_not_empty(self) -> None:
        assert len(SUCCESS_MESSAGES) >= 10

    def test_ascii_skulls_not_empty(self) -> None:
        assert len(ASCII_SKULLS) >= 2

    def test_welcome_banner_is_string(self) -> None:
        assert isinstance(WELCOME_BANNER, str)
        assert len(WELCOME_BANNER) > 100

    def test_no_duplicate_ips(self) -> None:
        assert len(set(FAKE_IPS)) == len(FAKE_IPS)

    def test_no_duplicate_servers(self) -> None:
        assert len(set(TARGET_SERVERS)) == len(TARGET_SERVERS)

    def test_port_numbers_are_valid(self) -> None:
        for port in PORT_NUMBERS:
            assert 1 <= port <= 65535


class TestGetRandomItems:
    """Tests for the get_random_items helper."""

    def test_returns_correct_count(self) -> None:
        result = get_random_items(FAKE_IPS, 5)
        assert len(result) == 5

    def test_returns_subset(self) -> None:
        result = get_random_items(FAKE_IPS, 3)
        for item in result:
            assert item in FAKE_IPS

    def test_no_duplicates(self) -> None:
        result = get_random_items(FAKE_IPS, 10)
        assert len(set(result)) == len(result)

    def test_clamps_to_pool_size(self) -> None:
        small_pool = ["a", "b", "c"]
        result = get_random_items(small_pool, 100)
        assert len(result) == 3

    def test_zero_items(self) -> None:
        result = get_random_items(FAKE_IPS, 0)
        assert result == []


class TestGetRandomIp:
    """Tests for the random IP generator."""

    def test_format(self) -> None:
        ip = get_random_ip()
        parts = ip.split(".")
        assert len(parts) == 4

    def test_octets_in_range(self) -> None:
        ip = get_random_ip()
        for octet in ip.split("."):
            assert 1 <= int(octet) <= 254

    def test_returns_string(self) -> None:
        assert isinstance(get_random_ip(), str)

    def test_randomness(self) -> None:
        # two calls should usually differ
        ips = {get_random_ip() for _ in range(10)}
        assert len(ips) > 1


class TestGetRandomHex:
    """Tests for the random hex generator."""

    def test_default_length(self) -> None:
        result = get_random_hex()
        assert len(result) == 32

    def test_custom_length(self) -> None:
        result = get_random_hex(64)
        assert len(result) == 64

    def test_valid_hex_chars(self) -> None:
        result = get_random_hex(100)
        assert re.match(r"^[0-9a-f]+$", result)

    def test_zero_length(self) -> None:
        assert get_random_hex(0) == ""


class TestGetRandomMac:
    """Tests for the random MAC generator."""

    def test_format(self) -> None:
        mac = get_random_mac()
        assert re.match(r"^([0-9a-f]{2}:){5}[0-9a-f]{2}$", mac)

    def test_returns_string(self) -> None:
        assert isinstance(get_random_mac(), str)

    def test_six_octets(self) -> None:
        mac = get_random_mac()
        assert len(mac.split(":")) == 6

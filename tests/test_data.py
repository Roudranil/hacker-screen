"""Tests for the data module — loaders, pools, helpers, and random generators.

Tests cover:
- JSON/TXT asset loading functions
- Asset file integrity (every file loads and has expected structure)
- Data pool population and uniqueness
- Random generator helpers
"""

import re

import pytest

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
    _load_json,
    _load_skulls,
    _load_text,
    get_random_hex,
    get_random_ip,
    get_random_items,
    get_random_mac,
)


class TestLoadJson:
    """Tests for the _load_json helper."""

    def test_loads_list(self) -> None:
        result = _load_json("ips.json")
        assert isinstance(result, list)

    def test_loads_correct_type_strings(self) -> None:
        result = _load_json("ips.json")
        assert all(isinstance(item, str) for item in result)

    def test_loads_correct_type_ints(self) -> None:
        result = _load_json("ports.json")
        assert all(isinstance(item, int) for item in result)

    def test_loads_nonempty(self) -> None:
        result = _load_json("ips.json")
        assert len(result) > 0

    def test_missing_file_raises(self) -> None:
        with pytest.raises(FileNotFoundError):
            _load_json("nonexistent_file.json")

    def test_all_json_files_are_valid(self) -> None:
        """Verify every JSON asset file parses without error."""
        json_files = [
            "ips.json",
            "files.json",
            "passwords.json",
            "hacking_steps.json",
            "malware_names.json",
            "target_servers.json",
            "encryption_algos.json",
            "network_protocols.json",
            "ports.json",
            "system_processes.json",
            "error_messages.json",
            "success_messages.json",
        ]
        for filename in json_files:
            data = _load_json(filename)
            assert isinstance(data, list), f"{filename} did not return a list"
            assert len(data) > 0, f"{filename} is empty"


class TestLoadText:
    """Tests for the _load_text helper."""

    def test_loads_string(self) -> None:
        result = _load_text("banner.txt")
        assert isinstance(result, str)

    def test_banner_has_content(self) -> None:
        result = _load_text("banner.txt")
        assert len(result) > 100

    def test_missing_file_raises(self) -> None:
        with pytest.raises(FileNotFoundError):
            _load_text("nonexistent_file.txt")


class TestLoadSkulls:
    """Tests for the _load_skulls helper."""

    def test_returns_list(self) -> None:
        result = _load_skulls()
        assert isinstance(result, list)

    def test_at_least_three_skulls(self) -> None:
        result = _load_skulls()
        assert len(result) >= 3

    def test_all_strings(self) -> None:
        result = _load_skulls()
        assert all(isinstance(s, str) for s in result)

    def test_skulls_have_content(self) -> None:
        result = _load_skulls()
        for skull in result:
            assert len(skull.strip()) > 10

    def test_sorted_order(self) -> None:
        """Skulls should load in deterministic filename order."""
        result1 = _load_skulls()
        result2 = _load_skulls()
        # ordering should be reproducible across calls
        assert result1 == result2


class TestAssetFileIntegrity:
    """Verify each JSON asset file has expected minimum items."""

    @pytest.mark.parametrize(
        "filename,min_count",
        [
            ("ips.json", 20),
            ("files.json", 15),
            ("passwords.json", 15),
            ("hacking_steps.json", 20),
            ("malware_names.json", 10),
            ("target_servers.json", 10),
            ("encryption_algos.json", 10),
            ("network_protocols.json", 10),
            ("ports.json", 20),
            ("system_processes.json", 10),
            ("error_messages.json", 10),
            ("success_messages.json", 10),
        ],
    )
    def test_minimum_item_count(self, filename: str, min_count: int) -> None:
        data = _load_json(filename)
        assert len(data) >= min_count, (
            f"{filename} has {len(data)} items, expected >= {min_count}"
        )

    @pytest.mark.parametrize(
        "filename,expected_keys",
        [
            ("phase_messages.json", ["recon", "exploitation", "exfil_tasks"]),
            ("signal_profiles.json", None),  # list, not dict
        ],
    )
    def test_structured_assets(
        self,
        filename: str,
        expected_keys: list | None,
    ) -> None:
        data = _load_json(filename)
        if expected_keys is not None:
            for key in expected_keys:
                assert key in data, f"Missing key '{key}' in {filename}"
                assert len(data[key]) >= 3
        else:
            # signal_profiles is a list of dicts
            assert isinstance(data, list)
            assert len(data) >= 3
            for item in data:
                assert "left_label" in item
                assert "right_label" in item


class TestDataPoolTypes:
    """Verify module-level constants have correct runtime types."""

    def test_string_pools_are_string_lists(self) -> None:
        string_pools = [
            FAKE_IPS,
            FAKE_FILES,
            FAKE_PASSWORDS,
            HACKING_STEPS,
            MALWARE_NAMES,
            TARGET_SERVERS,
            ENCRYPTION_ALGOS,
            NETWORK_PROTOCOLS,
            SYSTEM_PROCESSES,
            ERROR_MESSAGES,
            SUCCESS_MESSAGES,
        ]
        for pool in string_pools:
            assert isinstance(pool, list)
            assert all(isinstance(item, str) for item in pool)

    def test_port_numbers_are_int_list(self) -> None:
        assert isinstance(PORT_NUMBERS, list)
        assert all(isinstance(p, int) for p in PORT_NUMBERS)

    def test_skulls_are_string_list(self) -> None:
        assert isinstance(ASCII_SKULLS, list)
        assert all(isinstance(s, str) for s in ASCII_SKULLS)


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

"""Tests for the effects module — each effect runs without crashing.

Effects are heavily visual and time-dependent, so we mock time.sleep
and use a string-buffer console to verify output is produced without
errors. We don't assert exact visual output — that's fragile.
"""

import io
from unittest.mock import MagicMock, patch

import pytest
from rich.console import Console

from hacker_screen import effects


@pytest.fixture
def buffer_console() -> Console:
    """Console that writes to a string buffer for output capture."""
    return Console(file=io.StringIO(), width=80, force_terminal=True)


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestTypingEffect:
    """Tests for the typing_effect function."""

    def test_produces_output(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.typing_effect(console, "hello", delay=0)
        output = console.file.getvalue()
        assert "h" in output

    def test_empty_string(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.typing_effect(console, "", delay=0)
        # should not crash


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowWelcomeBanner:
    """Tests for the welcome banner display."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_welcome_banner(console)

    def test_prints_something(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_welcome_banner(console)
        assert len(console.file.getvalue()) > 0


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowHackingStep:
    """Tests for the hacking step spinner."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_hacking_step(console, "Testing...", duration=0)

    def test_with_different_messages(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        for msg in ["Step 1", "Step 2", "Step 3"]:
            effects.show_hacking_step(console, msg, duration=0)


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowPasswordCrack:
    """Tests for password cracking animation."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_password_crack(console, "/etc/shadow")


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowProgressBar:
    """Tests for progress bar rendering."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_progress_bar(console, "Test progress", total=10)


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowRichProgress:
    """Tests for concurrent Rich progress bars."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_rich_progress(console, ["Task A", "Task B"])


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowSignalGraph:
    """Tests for the sine wave signal graph."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_signal_graph(console, label="TEST")


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowDualSignalGraph:
    """Tests for the dual side-by-side sinusoidal graph."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=100)
        effects.show_dual_signal_graph(console, left_label="A", right_label="B")


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowHexDump:
    """Tests for hex dump display."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_hex_dump(console, lines=3)


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowNetworkTraffic:
    """Tests for network traffic log."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=100)
        effects.show_network_traffic(console, packets=3)


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowFileTree:
    """Tests for animated file tree."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_file_tree(console)


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowSystemInfo:
    """Tests for system info table."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_system_info(console)


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowPortScan:
    """Tests for port scan animation."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_port_scan(console, num_ports=5)


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowCountdown:
    """Tests for countdown timer."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_countdown(console, seconds=3)

    def test_calls_sleep(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_countdown(console, seconds=3)
        # sleep called for each second + final pause
        assert mock_sleep.call_count >= 3


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowPermissionPrompt:
    """Tests for the final permission prompt."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_permission_prompt(console)


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowGlitchText:
    """Tests for glitch text effect."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_glitch_text(console, "HELLO WORLD", cycles=3)


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowEncryptionCrack:
    """Tests for hash brute-force animation."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_encryption_crack(console, num_attempts=5)


@patch("hacker_screen.effects.time.sleep", return_value=None)
class TestShowFailureRetry:
    """Tests for the failure/retry simulation."""

    def test_runs_without_error(self, mock_sleep: MagicMock) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_failure_retry(console, "Test operation")

    def test_output_contains_failed_and_success(
        self,
        mock_sleep: MagicMock,
    ) -> None:
        console = Console(file=io.StringIO(), width=80)
        effects.show_failure_retry(console, "Test operation")
        output = console.file.getvalue()
        assert "FAILED" in output
        assert "succeeded" in output


class TestBuildScanLine:
    """Tests for the horizontal scanning helper."""

    def test_returns_multiline_string(self) -> None:
        result = effects._build_scan_line(20, 5, 0)
        lines = result.split("\n")
        assert len(lines) == 5

    def test_width_matches(self) -> None:
        result = effects._build_scan_line(30, 4, 0)
        for line in result.split("\n"):
            assert len(line) == 30

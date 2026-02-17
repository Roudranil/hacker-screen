"""Tests for the sequences module — phase orchestration.

Verifies each phase function calls expected effects and that
run_all chains everything in the right order. All effects and
matrix rain are mocked to avoid actual rendering.

Randomization makes exact call counts unpredictable, so tests
use range-based assertions (>= / <=) where appropriate.
"""

import io
from unittest.mock import MagicMock, patch

import pytest
from rich.console import Console

from hacker_screen import sequences
from hacker_screen.sequences import RetryTracker


@pytest.fixture
def mock_console() -> MagicMock:
    """Console mock with width attribute."""
    console = MagicMock()
    console.width = 80
    return console


@pytest.fixture
def buffer_console() -> Console:
    """Real console that writes to a string buffer."""
    return Console(file=io.StringIO(), width=80, force_terminal=True)


@pytest.fixture
def tracker() -> RetryTracker:
    """Fresh retry tracker for testing."""
    return RetryTracker()


# ---------------------------------------------------------------------------
# RetryTracker
# ---------------------------------------------------------------------------


class TestRetryTracker:
    """Tests for the RetryTracker class."""

    def test_initial_state(self) -> None:
        t = RetryTracker()
        assert t.phase_retries == 0
        assert t.global_retries == 0

    def test_can_retry_initially(self) -> None:
        assert RetryTracker().can_retry()

    def test_record_increments_both(self) -> None:
        t = RetryTracker()
        t.record_retry()
        assert t.phase_retries == 1
        assert t.global_retries == 1

    def test_reset_phase_clears_phase_only(self) -> None:
        t = RetryTracker()
        t.record_retry()
        t.reset_phase()
        assert t.phase_retries == 0
        assert t.global_retries == 1

    def test_per_phase_cap(self) -> None:
        t = RetryTracker()
        t.record_retry()
        t.record_retry()
        assert not t.can_retry()  # 2 retries in phase = cap

    def test_global_cap(self) -> None:
        t = RetryTracker()
        for _ in range(3):
            t.record_retry()
            t.reset_phase()
        assert not t.can_retry()  # 3 global = cap


# ---------------------------------------------------------------------------
# Phase header
# ---------------------------------------------------------------------------


@patch("hacker_screen.sequences.time.sleep", return_value=None)
class TestPhaseHeader:
    """Tests for the internal _phase_header function."""

    def test_prints_panel(self, mock_sleep: MagicMock, mock_console: MagicMock) -> None:
        sequences._phase_header(mock_console, 1, "TEST PHASE")
        mock_console.print.assert_called()

    def test_auto_style_from_phase_num(
        self,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences._phase_header(mock_console, 1, "A")
        sequences._phase_header(mock_console, 2, "B")
        assert mock_console.print.call_count >= 4

    def test_explicit_style_override(
        self,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences._phase_header(mock_console, 1, "X", style="magenta")
        mock_console.print.assert_called()


# ---------------------------------------------------------------------------
# Welcome
# ---------------------------------------------------------------------------


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.show_system_info")
@patch("hacker_screen.sequences.show_glitch_text")
@patch("hacker_screen.sequences.show_welcome_banner")
class TestRunWelcome:
    """Tests for the welcome phase."""

    def test_calls_banner(
        self,
        mock_banner: MagicMock,
        mock_glitch: MagicMock,
        mock_sysinfo: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_welcome(mock_console)
        mock_banner.assert_called_once_with(mock_console)

    def test_calls_system_info(
        self,
        mock_banner: MagicMock,
        mock_glitch: MagicMock,
        mock_sysinfo: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_welcome(mock_console)
        mock_sysinfo.assert_called_once_with(mock_console)


# ---------------------------------------------------------------------------
# Required phases
# ---------------------------------------------------------------------------


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.show_failure_retry")
@patch("hacker_screen.sequences.show_hacking_step")
class TestRunExploitationPhase:
    """Tests for the exploitation phase."""

    def test_calls_steps(
        self,
        mock_step: MagicMock,
        mock_fail: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_exploitation_phase(mock_console, tracker=RetryTracker())
        total = mock_step.call_count + mock_fail.call_count
        assert 5 <= total <= 8

    def test_retries_capped(
        self,
        mock_step: MagicMock,
        mock_fail: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        """Failure retries should never exceed per-phase cap."""
        sequences.run_exploitation_phase(mock_console, tracker=RetryTracker())
        assert mock_fail.call_count <= 2


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.show_progress_bar")
@patch("hacker_screen.sequences.show_encryption_crack")
@patch("hacker_screen.sequences.show_password_crack")
class TestRunCrackingPhase:
    """Tests for the cracking phase."""

    def test_calls_password_crack(
        self,
        mock_crack: MagicMock,
        mock_encrypt: MagicMock,
        mock_progress: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_cracking_phase(mock_console)
        assert mock_crack.call_count >= 2

    def test_calls_encryption_crack(
        self,
        mock_crack: MagicMock,
        mock_encrypt: MagicMock,
        mock_progress: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_cracking_phase(mock_console)
        assert mock_encrypt.call_count == 1


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.show_progress_bar")
@patch("hacker_screen.sequences.show_failure_retry")
@patch("hacker_screen.sequences.show_hacking_step")
@patch("hacker_screen.sequences.typing_effect")
class TestRunMalwarePhase:
    """Tests for the malware deployment phase."""

    def test_calls_steps(
        self,
        mock_typing: MagicMock,
        mock_step: MagicMock,
        mock_fail: MagicMock,
        mock_progress: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_malware_phase(mock_console, tracker=RetryTracker())
        total = mock_step.call_count + mock_fail.call_count
        assert 3 <= total <= 6

    def test_retries_capped(
        self,
        mock_typing: MagicMock,
        mock_step: MagicMock,
        mock_fail: MagicMock,
        mock_progress: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_malware_phase(mock_console, tracker=RetryTracker())
        assert mock_fail.call_count <= 2

    def test_calls_progress_bar(
        self,
        mock_typing: MagicMock,
        mock_step: MagicMock,
        mock_fail: MagicMock,
        mock_progress: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_malware_phase(mock_console, tracker=RetryTracker())
        assert mock_progress.call_count == 2


# ---------------------------------------------------------------------------
# Final prompt
# ---------------------------------------------------------------------------


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.show_countdown")
@patch("hacker_screen.sequences.show_permission_prompt")
@patch("hacker_screen.sequences.typing_effect")
class TestRunFinalPrompt:
    """Tests for the final prompt phase."""

    def test_calls_permission_prompt(
        self,
        mock_typing: MagicMock,
        mock_prompt: MagicMock,
        mock_countdown: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_final_prompt(mock_console)
        mock_prompt.assert_called_once()

    def test_calls_countdown(
        self,
        mock_typing: MagicMock,
        mock_prompt: MagicMock,
        mock_countdown: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_final_prompt(mock_console)
        mock_countdown.assert_called_once_with(mock_console, seconds=10)


# ---------------------------------------------------------------------------
# Bonus phases
# ---------------------------------------------------------------------------


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.show_system_info")
@patch("hacker_screen.sequences.show_network_traffic")
@patch("hacker_screen.sequences.show_port_scan")
@patch("hacker_screen.sequences.typing_effect")
class TestRunReconPhase:
    """Tests for the reconnaissance bonus phase."""

    def test_calls_port_scan(
        self,
        mock_typing: MagicMock,
        mock_port: MagicMock,
        mock_traffic: MagicMock,
        mock_sysinfo: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_recon_phase(mock_console, tracker=RetryTracker())
        mock_port.assert_called_once()


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.show_rich_progress")
@patch("hacker_screen.sequences.show_hex_dump")
@patch("hacker_screen.sequences.show_file_tree")
class TestRunDataExfilPhase:
    """Tests for the data exfiltration bonus phase."""

    def test_calls_file_tree(
        self,
        mock_tree: MagicMock,
        mock_hex: MagicMock,
        mock_progress: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_data_exfil_phase(mock_console, tracker=RetryTracker())
        mock_tree.assert_called_once()


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.show_dual_signal_graph")
@patch("hacker_screen.sequences.typing_effect")
class TestRunSurveillancePhase:
    """Tests for the surveillance bonus phase."""

    def test_calls_dual_signal_graph(
        self,
        mock_typing: MagicMock,
        mock_dual: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_surveillance_phase(mock_console, tracker=RetryTracker())
        mock_dual.assert_called_once()


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.show_failure_retry")
@patch("hacker_screen.sequences.show_hacking_step")
@patch("hacker_screen.sequences.typing_effect")
class TestRunFirewallBypass:
    """Tests for the firewall bypass bonus phase."""

    def test_runs_without_error(
        self,
        mock_typing: MagicMock,
        mock_step: MagicMock,
        mock_fail: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_firewall_bypass(mock_console, phase_num=3, tracker=RetryTracker())
        total = mock_step.call_count + mock_fail.call_count
        assert total == 3


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.show_progress_bar")
@patch("hacker_screen.sequences.show_hacking_step")
@patch("hacker_screen.sequences.typing_effect")
class TestRunSocialEngineering:
    """Tests for the social engineering bonus phase."""

    def test_runs_without_error(
        self,
        mock_typing: MagicMock,
        mock_step: MagicMock,
        mock_progress: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_social_engineering(
            mock_console, phase_num=4, tracker=RetryTracker()
        )
        assert mock_step.call_count >= 2
        mock_progress.assert_called_once()


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.show_progress_bar")
@patch("hacker_screen.sequences.show_hacking_step")
@patch("hacker_screen.sequences.typing_effect")
class TestRunCleanupPhase:
    """Tests for the cleanup bonus phase."""

    def test_runs_without_error(
        self,
        mock_typing: MagicMock,
        mock_step: MagicMock,
        mock_progress: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_cleanup_phase(mock_console, phase_num=8, tracker=RetryTracker())
        assert mock_step.call_count >= 3
        mock_progress.assert_called_once()


# ---------------------------------------------------------------------------
# Bonus phase selection
# ---------------------------------------------------------------------------


class TestSelectBonusPhases:
    """Tests for the _select_bonus_phases helper."""

    def test_respects_max_slots(self) -> None:
        # even if all phases roll in, cap to max_slots
        for _ in range(50):
            result = sequences._select_bonus_phases(2)
            assert len(result) <= 2

    def test_returns_list(self) -> None:
        result = sequences._select_bonus_phases(4)
        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# Full orchestration
# ---------------------------------------------------------------------------


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.run_matrix_rain")
@patch("hacker_screen.sequences.run_final_prompt")
@patch("hacker_screen.sequences.run_malware_phase")
@patch("hacker_screen.sequences.run_cracking_phase")
@patch("hacker_screen.sequences.run_exploitation_phase")
@patch("hacker_screen.sequences.run_welcome")
@patch("hacker_screen.sequences._select_bonus_phases", return_value=[])
class TestRunAll:
    """Tests for the full run_all orchestration."""

    def test_calls_required_phases(
        self,
        mock_bonus: MagicMock,
        mock_welcome: MagicMock,
        mock_exploit: MagicMock,
        mock_crack: MagicMock,
        mock_malware: MagicMock,
        mock_final: MagicMock,
        mock_rain: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_all(mock_console)

        mock_welcome.assert_called_once_with(mock_console)
        mock_exploit.assert_called_once()
        mock_crack.assert_called_once()
        mock_malware.assert_called_once()
        mock_final.assert_called_once()
        mock_rain.assert_called_once()

    def test_required_phases_get_tracker(
        self,
        mock_bonus: MagicMock,
        mock_welcome: MagicMock,
        mock_exploit: MagicMock,
        mock_crack: MagicMock,
        mock_malware: MagicMock,
        mock_final: MagicMock,
        mock_rain: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        """Required phases that use retries get a tracker kwarg."""
        sequences.run_all(mock_console)

        _, kwargs = mock_exploit.call_args
        assert "tracker" in kwargs
        assert isinstance(kwargs["tracker"], RetryTracker)

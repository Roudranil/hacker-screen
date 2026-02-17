"""Tests for the sequences module — phase orchestration.

Verifies each phase function calls expected effects and that
run_all chains everything in the right order. All effects and
matrix rain are mocked to avoid actual rendering.
"""

from unittest.mock import MagicMock, patch

import pytest

from hacker_screen import sequences


@pytest.fixture
def mock_console() -> MagicMock:
    """Console mock with width attribute."""
    console = MagicMock()
    console.width = 80
    return console


@patch("hacker_screen.sequences.time.sleep", return_value=None)
class TestPhaseHeader:
    """Tests for the internal _phase_header function."""

    def test_prints_panel(self, mock_sleep: MagicMock, mock_console: MagicMock) -> None:
        sequences._phase_header(mock_console, "TEST PHASE")
        mock_console.print.assert_called()


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


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.show_network_traffic")
@patch("hacker_screen.sequences.show_port_scan")
@patch("hacker_screen.sequences.typing_effect")
class TestRunReconPhase:
    """Tests for the reconnaissance phase."""

    def test_calls_port_scan(
        self,
        mock_typing: MagicMock,
        mock_port: MagicMock,
        mock_traffic: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_recon_phase(mock_console)
        mock_port.assert_called_once()

    def test_calls_network_traffic(
        self,
        mock_typing: MagicMock,
        mock_port: MagicMock,
        mock_traffic: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_recon_phase(mock_console)
        mock_traffic.assert_called_once()


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.show_hacking_step")
class TestRunExploitationPhase:
    """Tests for the exploitation phase."""

    def test_calls_hacking_steps(
        self,
        mock_step: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_exploitation_phase(mock_console)
        # should call 5-7 hacking steps
        assert mock_step.call_count >= 5
        assert mock_step.call_count <= 7


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
        assert mock_crack.call_count == 3

    def test_calls_encryption_crack(
        self,
        mock_crack: MagicMock,
        mock_encrypt: MagicMock,
        mock_progress: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_cracking_phase(mock_console)
        mock_encrypt.assert_called_once()


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.show_rich_progress")
@patch("hacker_screen.sequences.show_hex_dump")
@patch("hacker_screen.sequences.show_file_tree")
class TestRunDataExfilPhase:
    """Tests for the data exfiltration phase."""

    def test_calls_file_tree(
        self,
        mock_tree: MagicMock,
        mock_hex: MagicMock,
        mock_progress: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_data_exfil_phase(mock_console)
        mock_tree.assert_called_once()

    def test_calls_hex_dump(
        self,
        mock_tree: MagicMock,
        mock_hex: MagicMock,
        mock_progress: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_data_exfil_phase(mock_console)
        mock_hex.assert_called_once()


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.show_dual_signal_graph")
@patch("hacker_screen.sequences.typing_effect")
class TestRunSurveillancePhase:
    """Tests for the surveillance phase."""

    def test_calls_dual_signal_graph(
        self,
        mock_typing: MagicMock,
        mock_dual: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_surveillance_phase(mock_console)
        mock_dual.assert_called_once()


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.show_progress_bar")
@patch("hacker_screen.sequences.show_hacking_step")
@patch("hacker_screen.sequences.typing_effect")
class TestRunMalwarePhase:
    """Tests for the malware deployment phase."""

    def test_calls_hacking_step(
        self,
        mock_typing: MagicMock,
        mock_step: MagicMock,
        mock_progress: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_malware_phase(mock_console)
        assert mock_step.call_count == 4

    def test_calls_progress_bar(
        self,
        mock_typing: MagicMock,
        mock_step: MagicMock,
        mock_progress: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_malware_phase(mock_console)
        assert mock_progress.call_count == 2


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


@patch("hacker_screen.sequences.time.sleep", return_value=None)
@patch("hacker_screen.sequences.run_matrix_rain")
@patch("hacker_screen.sequences.run_final_prompt")
@patch("hacker_screen.sequences.run_malware_phase")
@patch("hacker_screen.sequences.run_surveillance_phase")
@patch("hacker_screen.sequences.run_data_exfil_phase")
@patch("hacker_screen.sequences.run_cracking_phase")
@patch("hacker_screen.sequences.run_exploitation_phase")
@patch("hacker_screen.sequences.run_recon_phase")
@patch("hacker_screen.sequences.run_welcome")
class TestRunAll:
    """Tests for the full run_all orchestration."""

    def test_calls_all_phases_in_order(
        self,
        mock_welcome: MagicMock,
        mock_recon: MagicMock,
        mock_exploit: MagicMock,
        mock_crack: MagicMock,
        mock_exfil: MagicMock,
        mock_surv: MagicMock,
        mock_malware: MagicMock,
        mock_final: MagicMock,
        mock_rain: MagicMock,
        mock_sleep: MagicMock,
        mock_console: MagicMock,
    ) -> None:
        sequences.run_all(mock_console)

        mock_welcome.assert_called_once_with(mock_console)
        mock_recon.assert_called_once_with(mock_console)
        mock_exploit.assert_called_once_with(mock_console)
        mock_crack.assert_called_once_with(mock_console)
        mock_exfil.assert_called_once_with(mock_console)
        mock_surv.assert_called_once_with(mock_console)
        mock_malware.assert_called_once_with(mock_console)
        mock_final.assert_called_once_with(mock_console)
        mock_rain.assert_called_once()

"""Tests for the matrix rain module.

The actual curses rendering can't be tested in CI, so we test
the data structures (Column) and helper functions. The curses
wrapper handles cleanup, so we verify graceful exit behavior.
"""

from unittest.mock import MagicMock, patch

from hacker_screen.matrix_rain import RAIN_CHARS, Column, _get_rain_char


class TestRainChars:
    """Tests for the rain character set."""

    def test_not_empty(self) -> None:
        assert len(RAIN_CHARS) > 50

    def test_contains_katakana(self) -> None:
        # check for some katakana chars
        assert "ア" in RAIN_CHARS
        assert "カ" in RAIN_CHARS

    def test_contains_latin(self) -> None:
        assert "A" in RAIN_CHARS
        assert "Z" in RAIN_CHARS

    def test_contains_digits(self) -> None:
        assert "0" in RAIN_CHARS
        assert "9" in RAIN_CHARS


class TestGetRainChar:
    """Tests for the random rain character picker."""

    def test_returns_single_char(self) -> None:
        char = _get_rain_char()
        assert len(char) == 1

    def test_returns_char_from_set(self) -> None:
        char = _get_rain_char()
        assert char in RAIN_CHARS

    def test_randomness(self) -> None:
        chars = {_get_rain_char() for _ in range(50)}
        assert len(chars) > 5


class TestColumn:
    """Tests for the Column dataclass."""

    def test_default_init(self) -> None:
        col = Column(x=5)
        assert col.x == 5
        assert col.y == 0.0
        assert col.active is True

    def test_reset_changes_position(self) -> None:
        col = Column(x=0)
        col.y = 100.0
        col.reset(max_y=40)
        assert col.y <= 0

    def test_reset_sets_speed(self) -> None:
        col = Column(x=0)
        col.reset(max_y=40)
        assert 0.3 <= col.speed <= 1.2

    def test_reset_sets_length(self) -> None:
        col = Column(x=0)
        col.reset(max_y=40)
        assert 5 <= col.length <= 20

    def test_reset_populates_chars(self) -> None:
        col = Column(x=0)
        col.reset(max_y=40)
        assert len(col.chars) == col.length

    def test_chars_from_rain_set(self) -> None:
        col = Column(x=0)
        col.reset(max_y=40)
        for char in col.chars:
            assert char in RAIN_CHARS


class TestRunMatrixRain:
    """Tests for the matrix rain launcher."""

    @patch("hacker_screen.matrix_rain.curses.wrapper")
    def test_calls_curses_wrapper(self, mock_wrapper: MagicMock) -> None:
        from hacker_screen.matrix_rain import run_matrix_rain

        run_matrix_rain()
        mock_wrapper.assert_called_once()

    @patch(
        "hacker_screen.matrix_rain.curses.wrapper",
        side_effect=KeyboardInterrupt,
    )
    def test_handles_keyboard_interrupt(self, mock_wrapper: MagicMock) -> None:
        from hacker_screen.matrix_rain import run_matrix_rain

        # should not raise
        run_matrix_rain()

"""Unit tests for entry point."""

from unittest.mock import MagicMock, patch

from pydantic import ValidationError

from icsaet_mcp.__main__ import main, setup_logging


class TestSetupLogging:
    """Tests for logging configuration."""

    def test_setup_logging_does_not_raise(self):
        """Test setup_logging runs without error."""
        # Act & Assert - should not raise
        setup_logging()


class TestMain:
    """Tests for main entry point."""

    @patch("icsaet_mcp.__main__.get_settings")
    def test_main_config_error_returns_1(self, mock_get_settings):
        """Test configuration error returns exit code 1."""
        # Arrange
        mock_get_settings.side_effect = ValidationError.from_exception_data(
            "Settings", []
        )

        # Act
        result = main()

        # Assert
        assert result == 1

    @patch("icsaet_mcp.__main__.get_settings")
    @patch("icsaet_mcp.server.mcp")
    def test_main_keyboard_interrupt_returns_0(self, mock_mcp, mock_get_settings):
        """Test KeyboardInterrupt returns exit code 0."""
        # Arrange
        mock_settings = MagicMock()
        mock_get_settings.return_value = mock_settings
        mock_mcp.run.side_effect = KeyboardInterrupt()

        # Act
        result = main()

        # Assert
        assert result == 0

    @patch("icsaet_mcp.__main__.get_settings")
    @patch("icsaet_mcp.server.mcp")
    def test_main_validates_config_first(self, mock_mcp, mock_get_settings):
        """Test configuration is validated before server runs."""
        # Arrange
        mock_settings = MagicMock()
        mock_get_settings.return_value = mock_settings
        call_order = []

        def track_get_settings():
            call_order.append("get_settings")
            return mock_settings

        def track_run():
            call_order.append("run")

        mock_get_settings.side_effect = track_get_settings
        mock_mcp.run.side_effect = track_run

        # Act
        main()

        # Assert
        assert call_order == ["get_settings", "run"]

    @patch("icsaet_mcp.__main__.get_settings")
    @patch("icsaet_mcp.server.mcp")
    def test_main_success_returns_0(self, mock_mcp, mock_get_settings):
        """Test successful run returns exit code 0."""
        # Arrange
        mock_settings = MagicMock()
        mock_get_settings.return_value = mock_settings

        # Act
        result = main()

        # Assert
        assert result == 0

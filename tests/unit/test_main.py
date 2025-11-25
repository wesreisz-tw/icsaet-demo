"""Unit tests for entry point."""

import logging
import sys
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from icsaet_mcp.__main__ import configure_logging, main


def test_configure_logging():
    """Arrange: Clean logging state
    Act: Call configure_logging
    Assert: Logging configured successfully"""
    configure_logging()

    root_logger = logging.getLogger()
    handlers = root_logger.handlers
    assert len(handlers) > 0


def test_main_with_valid_configuration():
    """Arrange: Valid configuration and mocked server
    Act: Call main
    Assert: Server starts successfully"""
    with (
        patch("icsaet_mcp.__main__.get_settings") as mock_settings,
        patch("icsaet_mcp.__main__.mcp") as mock_mcp,
    ):
        mock_settings.return_value = MagicMock(
            icaet_api_key="test-key", user_email="test@example.com"
        )
        mock_mcp.run.return_value = None

        main()

        mock_settings.assert_called_once()
        mock_mcp.run.assert_called_once()


def test_main_with_missing_configuration(capsys):
    """Arrange: Missing environment variables
    Act: Call main
    Assert: Exits with code 1 and prints helpful error message"""
    with patch("icsaet_mcp.__main__.get_settings") as mock_settings:
        mock_settings.side_effect = ValidationError.from_exception_data(
            "Settings",
            [
                {
                    "type": "missing",
                    "loc": ("ICAET_API_KEY",),
                    "input": {},
                    "msg": "Field required",
                }
            ],
        )

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Missing required configuration" in captured.err
        assert "ICAET_API_KEY" in captured.err
        assert "Cursor" in captured.err


def test_main_with_keyboard_interrupt():
    """Arrange: Server running, user presses Ctrl+C
    Act: Raise KeyboardInterrupt during server run
    Assert: Exits gracefully with code 0"""
    with (
        patch("icsaet_mcp.__main__.get_settings") as mock_settings,
        patch("icsaet_mcp.__main__.mcp") as mock_mcp,
    ):
        mock_settings.return_value = MagicMock(
            icaet_api_key="test-key", user_email="test@example.com"
        )
        mock_mcp.run.side_effect = KeyboardInterrupt()

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0


def test_main_with_server_error(capsys):
    """Arrange: Server raises unexpected exception
    Act: Call main
    Assert: Exits with code 1 and prints error message"""
    with (
        patch("icsaet_mcp.__main__.get_settings") as mock_settings,
        patch("icsaet_mcp.__main__.mcp") as mock_mcp,
    ):
        mock_settings.return_value = MagicMock(
            icaet_api_key="test-key", user_email="test@example.com"
        )
        mock_mcp.run.side_effect = RuntimeError("Test error")

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Server failed to start" in captured.err
        assert "Test error" in captured.err


def test_main_logs_version():
    """Arrange: Valid configuration
    Act: Call main with mocked logger
    Assert: Version is logged at startup"""
    with (
        patch("icsaet_mcp.__main__.get_settings") as mock_settings,
        patch("icsaet_mcp.__main__.mcp") as mock_mcp,
        patch("icsaet_mcp.__main__.logger") as mock_logger,
    ):
        mock_settings.return_value = MagicMock(
            icaet_api_key="test-key", user_email="test@example.com"
        )
        mock_mcp.run.return_value = None

        main()

        version_logged = any(
            "Starting ICAET MCP Server" in str(call)
            for call in mock_logger.info.call_args_list
        )
        assert version_logged

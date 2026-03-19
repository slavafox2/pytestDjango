import json
import os
import urllib.request
from unittest.mock import MagicMock, Mock, patch

import pytest


def fetch_rate() -> int:
    """
    Example function that would normally hit a remote API.
    We'll mock `urllib.request.urlopen` in the test so no network is used.
    """
    req = urllib.request.Request(
        "https://example.com/rate",
        headers={"User-Agent": "pytest"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read()
        status = getattr(resp, "status", None)
        if status != 200:
            raise ValueError("Bad response")
        return json.loads(body)["rate"]


def get_user_from_db(user_id: int) -> dict:
    """
    Pretend this is a real DB call. In unit tests we will patch it.
    """
    raise RuntimeError("DB is not available in unit test")


def get_user_name(user_id: int) -> str:
    return get_user_from_db(user_id)["name"]


def build_url() -> str:
    base = os.environ.get("API_BASE_URL", "http://localhost")
    return f"{base}/ping"


def test_mock_urlopen() -> None:
    """
    Mock example #1: patching a library call (urllib.request.urlopen).
    """
    fake_resp = Mock()
    fake_resp.status = 200
    fake_resp.read.return_value = json.dumps({"rate": 42}).encode("utf-8")

    fake_ctx = MagicMock()
    fake_ctx.__enter__.return_value = fake_resp
    fake_ctx.__exit__.return_value = False

    with patch("urllib.request.urlopen", return_value=fake_ctx) as mock_urlopen:
        assert fetch_rate() == 42
        mock_urlopen.assert_called_once()


def test_mock_internal_function() -> None:
    """
    Mock example #2: patching your own function (DB accessor).
    """
    with patch(f"{__name__}.get_user_from_db", return_value={"name": "Alice"}):
        assert get_user_name(1) == "Alice"


def test_monkeypatch_env(monkeypatch) -> None:
    """
    Mock example #3: monkeypatching environment variables.
    """
    monkeypatch.setenv("API_BASE_URL", "https://staging.example.com")
    assert build_url() == "https://staging.example.com/ping"


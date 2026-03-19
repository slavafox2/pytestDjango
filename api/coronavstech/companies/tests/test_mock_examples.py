import json
import os
from unittest.mock import Mock, patch

import pytest
import requests


def fetch_rate() -> int:
    """
    Example function that would normally hit a remote API.
    We'll mock `requests.get` in the test so no network is used.
    """
    resp = requests.get("https://example.com/rate", headers={"User-Agent": "pytest"}, timeout=10)
    if resp.status_code != 200:
        raise ValueError("Bad response")
    return json.loads(resp.content)["rate"]


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


def test_mock_requests_get() -> None:
    """
    Mock example #1: patching a library call (requests.get).
    """
    fake_resp = Mock()
    fake_resp.status_code = 200
    fake_resp.content = json.dumps({"rate": 42}).encode("utf-8")

    with patch("requests.get", return_value=fake_resp) as mock_get:
        assert fetch_rate() == 42
        mock_get.assert_called_once()


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


import json
from typing import Any

import pytest
import responses
from unittest import TestCase, mock

from iress.xplan.api import ResourcefulAPICall, ResourcefulAPIBasicAuth
from iress.xplan.session import Session

_CLIENT_ID = "dummy-client_id"
_BASE_URL = "https://dev.xplan.iress.com.au"
_CLIENT_V4_PATH = "entity/client-v4"
_CLIENT_V4_URL = f"{_BASE_URL}/resourceful/{_CLIENT_V4_PATH}"


class _AuthMocker:
    _time_code = 52548824
    otp_secret = "MR2W23LZFVXXI4C7ONSWG4TFOQ"
    user_id = "dummy-user"
    pwd = "dummy-pwd"
    # auth_string generated from user_id:pwd\n\r\t\u0007<otp>
    expected_auth_string = "Basic ZHVtbXktdXNlcjpkdW1teS1wd2QKDQkHMTA5ODg1"

    @classmethod
    def patch_totp_timecode(cls):
        return mock.patch("iress.xplan.api.TOTP.timecode", return_value=cls._time_code)


class TestResourcefulAPICall(TestCase):
    @responses.activate
    def test_url(self) -> None:
        """Should call the correct resourceful URL"""
        # setup
        responses.add(
            responses.GET,
            _CLIENT_V4_URL,
            json="dummy-response",
            status=200,
        )

        # execute
        result = self._execute_ResourcefulAPICall_with(
            base_url=_BASE_URL, path=_CLIENT_V4_PATH
        )

        # verify
        self._verify_responses_mock_was_called(result)

    @responses.activate
    def test_http_error(self) -> None:
        """Should throw an exception if http error occurs"""
        # setup
        responses.add(
            responses.GET,
            _CLIENT_V4_URL,
            json="",
            status=401,
        )

        # execute
        with pytest.raises(Exception) as err:
            self._execute_ResourcefulAPICall_with(
                base_url=_BASE_URL, path=_CLIENT_V4_PATH
            )

        # Verify
        assert err.value.args[0] == ('401 Client Error: Unauthorized for url: '
                                     'https://dev.xplan.iress.com.au/resourceful/entity/client-v4')

    @staticmethod
    def _execute_ResourcefulAPICall_with(base_url, path) -> Any:
        global _CLIENT_ID
        session = Session(base_url, _CLIENT_ID)
        client = ResourcefulAPICall(session, path)
        return json.loads(client.call_content())

    @staticmethod
    def _verify_responses_mock_was_called(result) -> None:
        expected_result = responses.calls[0].response.json()
        assert result == expected_result
        assert len(responses.calls) == 1

    @responses.activate
    @_AuthMocker.patch_totp_timecode()
    def test_get_request_headers(self, totp_tc) -> None:
        """Should send Xplan App Id and Accept headers"""
        global _CLIENT_ID

        # setup
        responses.add(
            responses.GET,
            _CLIENT_V4_URL,
            json="dummy-response",
            status=200,
        )

        # execute
        self._execute_ResourcefulAPICall_with(
            base_url=_BASE_URL, path=_CLIENT_V4_PATH
        )

        # verify
        headers = responses.calls[0].request.headers
        assert headers["X-Xplan-App-Id"] == _CLIENT_ID
        assert headers["Accept"] == "application/json"

    @responses.activate
    @_AuthMocker.patch_totp_timecode()
    def test_gen_authorization(self, totp_tc) -> None:
        """Should send correct OTP with request"""
        # setup
        responses.add(
            responses.GET,
            _CLIENT_V4_URL,
            json="dummy-response",
            status=200,
        )

        # execute
        self._execute_ResourcefulAPICall_with(
            base_url=_BASE_URL, path=_CLIENT_V4_PATH
        )

        # verify
        assert responses.calls[0].request.headers.get("Authorization") is None


class TestResourcefulAPIAuth(TestCase):
    @staticmethod
    def _execute_ResourcefulAPICall_with(base_url, path) -> Any:
        global _CLIENT_ID
        session = Session(base_url, _CLIENT_ID)
        client = ResourcefulAPIBasicAuth(
            session, path, "dummy-user", "dummy-pwd", _AuthMocker.otp_secret
        )
        return json.loads(client.call_content())

    @responses.activate
    @_AuthMocker.patch_totp_timecode()
    def test_gen_otp(self, totp_tc) -> None:
        """Should send correct OTP with request"""
        # setup
        responses.add(
            responses.GET,
            _CLIENT_V4_URL,
            json="dummy-response",
            status=200,
        )

        # execute
        self._execute_ResourcefulAPICall_with(
            base_url=_BASE_URL, path=_CLIENT_V4_PATH
        )

        # verify
        assert (
            responses.calls[0].request.headers["Authorization"]
            == _AuthMocker.expected_auth_string
        )

    @responses.activate
    def test_no_otp(self) -> None:
        """Should send basic auth string without OTP with request"""
        global _CLIENT_ID

        # setup
        session = Session("https://dev.xplan.iress.com.au/", _CLIENT_ID)
        responses.add(
            responses.GET,
            _CLIENT_V4_URL,
            json="dummy-response",
            status=200,
        )

        # execute
        client = ResourcefulAPIBasicAuth(
            session, _CLIENT_V4_PATH, "dummy-user", "dummy-pwd"
        )
        json.loads(client.call_content())

        # verify
        assert (
            responses.calls[0].request.headers["Authorization"]
            == "Basic ZHVtbXktdXNlcjpkdW1teS1wd2Q="
        )

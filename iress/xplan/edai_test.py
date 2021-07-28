import json
from unittest import TestCase, mock

import pytest
import responses

from iress.xplan.edai import EDAICall
from iress.xplan.session import Session

_RPC_URL = "https://dev.xplan.iress.com.au/RPC2"
_DUMMY_PATH = "my/dummy/path"


class _MockSession(Session):
    @property
    def cookies(self):
        return {"XPLANID": "xplan-session-cookie"}


class TestEDAICall(TestCase):
    def setUp(self) -> None:
        self.session = _MockSession("https://dev.xplan.iress.com.au", "sss")
        self.edai_call = EDAICall(self.session)

        responses.add(
            responses.POST, _RPC_URL, json="", status=200
        )

    @mock.patch("iress.xplan.edai.time.time")
    @responses.activate
    def test_call_test_parameters(self, time_mk) -> None:
        # Set up
        time_mk.return_value = 1577068503.711234
        params = ["xplan-session-cookie", "param-1", "param-2"]
        expected = bytearray(
            json.dumps(
                {"method": "edai.test_m", "params": params, "id": "1577068503711"}
            ),
            "utf-8",
        )

        # Execute
        self.edai_call.call(method="test_m", params=params[1:])

        # Verify
        assert responses.calls[0].request.body == expected

    @responses.activate
    def test_call_test_url(self) -> None:
        # Set up
        expected = _RPC_URL

        # Execute
        self.edai_call.call(method="test_m", params=[])

        # Verify
        assert responses.calls[0].request.url == expected

    @responses.activate
    def test_call_test_headers(self) -> None:
        # Execute
        self.edai_call.call(method="test_m", params=[])

        # Verify
        resp_headers = responses.calls[0].request.headers
        assert resp_headers["Authorization"] == f"Bearer {self.session.session_id}"
        assert resp_headers["Content-Type"] == "application/json"
        assert resp_headers["Origin"] == self.session.base_url

    @responses.activate
    def test_call_test_cookies(self) -> None:
        # Execute
        self.edai_call.call(method="test_m", params=[])

        # Verify
        assert (
            responses.calls[0].request.headers["Cookie"]
            == f"XPLANID={self.session.session_id}"
        )

    @mock.patch("iress.xplan.edai.EDAICall.call")
    @responses.activate
    def test_get_value(self, call_mk) -> None:
        # Execute
        self.edai_call.get_value(path=_DUMMY_PATH)

        # Verify
        assert call_mk.call_args[1]["method"] == "GetVal"
        assert call_mk.call_args[1]["params"][0] == _DUMMY_PATH


class TestEDAICallError(TestCase):
    def setUp(self) -> None:
        self.session = _MockSession("https://dev.xplan.iress.com.au", "sss")
        self.edai_call = EDAICall(self.session)

    @responses.activate
    def test_http_error(self) -> None:
        """Should throw an exception if http error occurs"""
        # setup
        responses.add(
            responses.POST, _RPC_URL, json="", status=401
        )

        # execute
        with pytest.raises(Exception) as err:
            self.edai_call.get_value(path=_DUMMY_PATH)

        # Verify
        assert err.value.args[0] == '401 Client Error: Unauthorized for url: https://dev.xplan.iress.com.au/RPC2'

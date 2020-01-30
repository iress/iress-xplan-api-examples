import json
from unittest import TestCase, mock

import pytest
import responses

from iress.xplan.edai import EDAICall
from iress.xplan.session import Session


class _MockSession(Session):
    @property
    def cookies(self):
        return {"XPLANID": "xplan-session-cookie"}


class TestEDAICall(TestCase):
    def setUp(self) -> None:
        self.session = _MockSession("https://dev.xplan.iress.com.au", "sss")
        self.edai_call = EDAICall(self.session)

        responses.add(
            responses.POST, "https://dev.xplan.iress.com.au/RPC2", json="", status=200
        )

    @mock.patch("iress.xplan.edai.time.time")
    @responses.activate
    def test_call_test_parameters(self, time_mk):
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
    def test_call_test_url(self):
        # Set up
        expected = "https://dev.xplan.iress.com.au/RPC2"

        # Execute
        self.edai_call.call(method="test_m", params=[])

        # Verify
        assert responses.calls[0].request.url == expected

    @responses.activate
    def test_call_test_headers(self):
        # Execute
        self.edai_call.call(method="test_m", params=[])

        # Verify
        resp_headers = responses.calls[0].request.headers
        assert resp_headers["Authorization"] == f"Bearer {self.session.session_id}"
        assert resp_headers["Content-Type"] == "application/json"
        assert resp_headers["Origin"] == self.session.base_url

    @responses.activate
    def test_call_test_cookies(self):
        # Execute
        self.edai_call.call(method="test_m", params=[])

        # Verify
        assert (
            responses.calls[0].request.headers["Cookie"]
            == f"XPLANID={self.session.session_id}"
        )

    @mock.patch("iress.xplan.edai.EDAICall.call")
    @responses.activate
    def test_get_value(self, call_mk):
        # Execute
        self.edai_call.get_value(path="my/dummy/path")

        # Verify
        assert call_mk.call_args[1]["method"] == "GetVal"
        assert call_mk.call_args[1]["params"][0] == "my/dummy/path"


class TestEDAICallError(TestCase):
    def setUp(self) -> None:
        self.session = _MockSession("https://dev.xplan.iress.com.au", "sss")
        self.edai_call = EDAICall(self.session)

    @responses.activate
    def test_http_error(self):
        """Should throw an exception if http error occurs"""
        # setup
        responses.add(
            responses.POST, "https://dev.xplan.iress.com.au/RPC2", json="", status=401
        )

        # execute
        with pytest.raises(Exception) as err:
            self.edai_call.get_value(path="my/dummy/path")

        # Verify
        assert err.value.args[0] == 'HTTP status code 401, error "Unauthorized".'

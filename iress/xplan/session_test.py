from unittest import TestCase

import responses

from iress.xplan.session import Session

_TEST_URL = "https://dev.xplan.iress.com.au"
_OTP_SECRET = "MR2W23LZFVXXI4C7ONSWG4TFOQ"
_CLIENT_ID = "dummy-client_id"


class TestSession(TestCase):
    def setUp(self) -> None:
        self.session = Session(_TEST_URL, _CLIENT_ID)
        responses.add(
            responses.GET,
            f"{_TEST_URL}/resourceful/session/user",
            json={"entity_id": 1234},
            headers={"set-cookie": "XPLANID=dummyid"},
            status=200,
        )

    @responses.activate
    def test_session_id_and_entity_id(self) -> None:
        # Execute
        self.session.authenticate(
            user="dummy-user", pwd="dummy-pwd", otp_secret=_OTP_SECRET
        )

        # Verify
        assert self.session.session_id == "dummyid"
        assert self.session.entity_id == 1234

    @responses.activate
    def test_cookies(self) -> None:
        # Execute
        self.session.authenticate(
            user="dummy-user", pwd="dummy-pwd", otp_secret=_OTP_SECRET
        )

        # Verify
        assert self.session.cookies == {"XPLANID": "dummyid"}

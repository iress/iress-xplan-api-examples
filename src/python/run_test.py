from argparse import Namespace
from unittest import TestCase, mock

from run import get_arguments, call
from iress.xplan.session import Session

_RAW_ARGS = [
    "-b",
    "https://dev.xplan.iress.com.au",
    "-u",
    "testuser",
    "-p",
    "dummy",
    "-o",
    "dummyotp",
    "-i",
    "dummyclientid",
]


class TestGetArguments(TestCase):
    def test_get_arguments(self):
        # Execute
        options = get_arguments(_RAW_ARGS)

        # Validate
        assert options.client_id == _RAW_ARGS[9]
        assert options.otp_secret == _RAW_ARGS[7]
        assert options.password == _RAW_ARGS[5]
        assert options.user_name == _RAW_ARGS[3]
        assert options.base_url == _RAW_ARGS[1]

    @mock.patch("run.getpass")
    def test_get_arguments_no_password(self, getpass):
        # Set up
        arg_copy = _RAW_ARGS.copy()
        del arg_copy[4:6]
        getpass.return_value = "s"

        # Execute
        options = get_arguments(arg_copy)

        # Validate
        assert options.password == "s"
        assert getpass.call_count == 1

    @mock.patch("run.getpass")
    def test_get_arguments_no_otp_secret_2fa(self, getpass):
        # Set up
        arg_copy = _RAW_ARGS.copy()
        del arg_copy[6:8]
        arg_copy.append("--use-tfa")
        getpass.return_value = "s"

        # Execute
        options = get_arguments(arg_copy)

        # Validate
        assert options.otp_secret == "s"
        assert getpass.call_count == 1

    @mock.patch("run.getpass")
    def test_get_arguments_no_otp_secret_non_2fa(self, getpass):
        # Set up
        arg_copy = _RAW_ARGS.copy()
        del arg_copy[6:8]

        # Execute
        options = get_arguments(arg_copy)

        # Validate
        assert options.otp_secret is None
        assert getpass.call_count == 0


class TestCall(TestCase):
    def setUp(self) -> None:
        self.session = Session("dummy", "cid")

    @mock.patch("run.EDAICall.get_value")
    def test_call_edai(self, edai_call):
        # Set up
        options = Namespace(edai_example=True)

        # Execute
        call(self.session, options)

        # Verify
        assert edai_call.call_count == 2

    @mock.patch("run.ResourcefulAPICall.call_content")
    def test_call_api(self, api_call):
        # Set up
        options = Namespace(edai_example=False)

        # Execute
        call(self.session, options)

        # Verify
        assert api_call.call_count == 1

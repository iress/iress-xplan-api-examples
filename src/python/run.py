#!/usr/bin/env python3

# vi:syntax=python

import sys
from argparse import ArgumentParser, Namespace
from getpass import getpass
from typing import List, Optional

from iress.xplan.api import ResourcefulAPICall
from iress.xplan.edai import EDAICall
from iress.xplan.session import Session


def _get_secrets(options: Optional[Namespace]):
    if not options.password:
        options.password = getpass(
            prompt="Password for {user}: ".format(user=options.user_name)
        )
    if not options.otp_secret and options.use_tfa:
        options.otp_secret = getpass(prompt="OTP Secret: ")


def get_arguments(argv: List) -> Optional[Namespace]:
    parser = ArgumentParser()
    parser.add_argument(
        "--base-url",
        "-b",
        help="The Base Xplan URL (e.g. https://edai.xplan.iress.com).",
        required=True,
    )
    parser.add_argument(
        "--client-id", "-i", help="The Xplan API key/Client ID.", required=True
    )
    parser.add_argument(
        "--otp-secret",
        "-o",
        help="The One Time Password (OTP) secret, if not provided the script will prompt the user.",
    )
    parser.add_argument("--user-name", "-u", help="The Xplan user name.", required=True)
    parser.add_argument(
        "--password",
        "-p",
        help="The Xplan user password, if not provided the script will prompt the user.",
    )
    parser.add_argument(
        "--use-tfa", "-tfa", help="Use 2FA for authentication.", action="store_true"
    )

    parser.add_argument(
        "--api-example",
        "-api",
        help="Run the API example with basic authentication.",
        action="store_true",
    )
    parser.add_argument(
        "--edai-example", "-edai", help="Run the EDAI example.", action="store_true"
    )

    known_args, unknown_args = parser.parse_known_args(args=argv)
    _get_secrets(known_args)

    return known_args


def api_example(session: Session):
    client = ResourcefulAPICall(session=session, api_path="entity/client-v4")

    print(client.call_content())


def edai_example(session: Session):
    client = EDAICall(session=session)

    print(client.get_value(path=f"entitymgr/user/{session.entity_id}/field/last_name"))
    print(client.get_value(path=f"entitymgr/user/{session.entity_id}/field/first_name"))


def call(session: Session, options: Optional[Namespace]):
    if options.edai_example:
        edai_example(session)
    else:
        api_example(session)


if __name__ == "__main__":
    opts = get_arguments(sys.argv[1:])

    xp_session = Session(opts.base_url, client_id=opts.client_id)
    xp_session.authenticate(
        user=opts.user_name, pwd=opts.password, otp_secret=opts.otp_secret
    )
    call(xp_session, opts)

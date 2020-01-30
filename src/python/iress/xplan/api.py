import base64
from urllib import response
from urllib.parse import urljoin

import requests
from pyotp import TOTP

# Xplan uses the below unique string to unpack the password and OTP when authenticating
from iress.xplan.session import Session

_OTP_SEPARATOR = "\n\r\t\u0007"


class ResourcefulAPICall:
    def __init__(self, session: Session, api_path: str):
        """
        Resourceful API class for using Xplan API

        Args:
            session (Session): The current Session object.
            api_path (str): The API endpoint path.
        """
        self.session = session
        self.api_path = api_path

    def call_content(self):
        resp = self.call()
        if resp.status_code != 200:
            raise Exception(
                f'HTTP status code {resp.status_code}, error "{resp.reason}".'
            )
        return resp.content

    def call(self) -> response:
        return requests.request(
            "get",
            self._url,
            headers=self._get_request_headers(),
            cookies=self.session.cookies,
        )

    @property
    def _url(self) -> str:
        return urljoin(
            urljoin(f"{self.session.base_url}/", "resourceful/"), self.api_path
        )

    def _get_request_headers(self) -> {str: str}:
        return {"X-Xplan-App-Id": self.session.client_id, "Accept": "application/json"}


class ResourcefulAPIBasicAuth(ResourcefulAPICall):
    def __init__(
        self,
        session: Session,
        api_path: str,
        user: str,
        pwd: str,
        otp_secret: str = None,
    ):
        """
        Resourceful API class for authenticating and using Xplan API

        Args:
            session (Session): The current Session object.
            api_path (str): The API endpoint path.
            user (str): The user to authenticate as.
            pwd (str): The user's password.
            otp_secret (:obj:`str`, optional): If 2FA needs to be used for authentication pass the Secret
                used to generate the OTP.
        """
        super().__init__(session, api_path)

        self.user = user
        self.pwd = pwd
        self.otp_secret = otp_secret

    def _get_request_headers(self) -> {str: str}:
        headers = super()._get_request_headers()
        headers["Authorization"] = self._get_authorization()
        return headers

    def _get_authorization(self) -> str:
        return f'Basic {self._gen_authorisation().decode("utf-8")}'

    def _gen_authorisation(self) -> bytes:
        auth_str = f"{self.user}:{self.pwd}"
        if self.otp_secret:
            auth_str = f"{auth_str}{_OTP_SEPARATOR}{self._gen_otp()}"

        return base64.b64encode(bytearray(auth_str, "utf-8"))

    def _gen_otp(self) -> str:
        return TOTP(self.otp_secret).now()

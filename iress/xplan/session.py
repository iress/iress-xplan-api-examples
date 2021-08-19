import json
from typing import Dict


class Session:
    def __init__(self, base_url: str, client_id: str) -> None:
        """
        Session class to hold Xplan session details.

        Args:
            base_url (str): The Xplan base URL (everything before `/resourceful/`.
            client_id (str): The Xplan API client ID.
        """
        self.base_url = base_url
        self.client_id = client_id

        self._cookies: Dict[str, str] = {}
        self._entity_id: int = 0

    def authenticate(self, user: str, pwd: str, otp_secret: str = None) -> None:
        from iress.xplan.api import ResourcefulAPIBasicAuth

        r_call = ResourcefulAPIBasicAuth(
            self, api_path="session/user", user=user, pwd=pwd, otp_secret=otp_secret
        )
        response = r_call.call()
        self._cookies = response.cookies

        raw_content = response.text
        print(response.status_code)
        print(raw_content)
        content = json.loads(raw_content)
        self._entity_id = content["entity_id"]

    @property
    def session_id(self) -> str:
        return self.cookies.get("XPLANID")

    @property
    def cookies(self) -> Dict[str, str]:
        return self._cookies

    @property
    def entity_id(self) -> int:
        return self._entity_id

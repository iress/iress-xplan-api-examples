import json


class Session:
    def __init__(self, base_url: str, client_id: str):
        """
        Session class to hold Xplan session details.

        Args:
            base_url (str): The Xplan base URL (everything before `/resourceful/`.
            client_id (str): The Xplan API client ID.
        """
        self.base_url = base_url
        self.client_id = client_id

        self._cookies: {str, str} = {}
        self._entity_id: int = 0

    def authenticate(self, user: str, pwd: str, otp_secret: str = None):
        from iress.xplan.api import ResourcefulAPIBasicAuth

        r_call = ResourcefulAPIBasicAuth(
            self, api_path="session/user", user=user, pwd=pwd, otp_secret=otp_secret
        )
        response = r_call.call()
        self._cookies = response.cookies

        content = json.loads(response.content)
        self._entity_id = content["entity_id"]

    @property
    def session_id(self):
        return self.cookies.get("XPLANID")

    @property
    def cookies(self):
        return self._cookies

    @property
    def entity_id(self):
        return self._entity_id

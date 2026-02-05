import json
import time
from http import HTTPStatus
from typing import Any, cast

import requests

from iress.xplan.session import Session


class EDAICall:
    def __init__(self, session: Session) -> None:
        """EDAI client class for using Xplan EDAI

        Args:
            session (Session): The current Session object.
        """
        self.session: Session = session

    def call(self, method: str, params: list[str]) -> dict[str, Any]:
        json_str = self._get_json(method, params)

        resp = requests.post(
            url=self._url(),
            json=json_str,
            headers=self._get_headers(),
            cookies=self.session.cookies,
            timeout=20,
        )
        if resp.status_code != HTTPStatus.OK:
            resp.raise_for_status()

        return cast("dict[str, Any]", json.loads(resp.content))

    def _get_json(self, method: str, params: list[str]) -> dict[str, str | list[str]]:
        return {
            "method": f"edai.{method}",
            "params": [self._session_id, *params],
            "id": str(round(time.time() * 1000)),
        }

    @property
    def _session_id(self) -> str:
        return self.session.session_id.split(".")[0]

    def _url(self) -> str:
        return f"{self.session.base_url}/RPC2"

    def _get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.session.session_id}",
            "Content-Type": "application/json",
            "Origin": self.session.base_url,
        }

    def get_value(self, path: str) -> dict[str, Any]:
        return self.call(method="GetVal", params=[path])

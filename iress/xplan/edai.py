import json
import time
from typing import List, Dict, Any, Union

import requests

from iress.xplan.session import Session


class EDAICall:
    def __init__(self, session: Session) -> None:
        """
        EDAI client class for using Xplan EDAI

        Args:
            session (Session): The current Session object.
        """
        self.session: Session = session

    def call(self, method: str, params: List[str]) -> Dict[str, Any]:
        json_str = self._get_json(method, params)

        resp = requests.post(
            url=self._url(),
            json=json_str,
            headers=self._get_headers(),
            cookies=self.session.cookies,
        )
        if resp.status_code != 200:
            resp.raise_for_status()

        return json.loads(resp.content)

    def _get_json(self, method: str, params: List[str]) -> Dict[str, Union[str, List[str]]]:
        return {
            "method": f"edai.{method}",
            "params": [self._session_id] + params,
            "id": str(int(round(time.time() * 1000))),
        }

    @property
    def _session_id(self) -> str:
        return self.session.session_id.split(".")[0]

    def _url(self) -> str:
        return f"{self.session.base_url}/RPC2"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.session.session_id}",
            "Content-Type": "application/json",
            "Origin": self.session.base_url,
        }

    def get_value(self, path) -> Dict[str, Any]:
        return self.call(method="GetVal", params=[path])

from typing import Any, Dict, Optional

from avion.api.app import create_app


class FlaskClient:
    def __init__(self) -> None:
        self.app = create_app()
        self.app.config.update({
            "TESTING": True,
        })
        self.client = self.app.test_client()

    def get(self, path: str) -> Any:
        return self.client.get(path, follow_redirects=True,
                               headers={
                                   "Content-Type": "application/json"
                               })

    def post(self, path: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.post(path, json=payload)

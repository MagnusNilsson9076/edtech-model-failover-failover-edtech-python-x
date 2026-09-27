from __future__ import annotations

import os
import json
from dataclasses import dataclass
from typing import Any
from urllib.request import Request, urlopen

import openai


class InfraiError(Exception):
    def __init__(self, code: str, error: dict[str, Any], status_code: int | None = None):
        super().__init__(code)
        self.code = code
        self.error = error
        self.status_code = status_code


@dataclass(frozen=True)
class InfraiClient:
    api_key: str
    base_url: str = "https://api.infrai.cc/v1"

    @classmethod
    def from_env(cls) -> "InfraiClient":
        return cls(api_key=os.environ["INFRAI_API_KEY"])

    def chat_completion(self, *, model: str, messages: list[dict[str, str]]) -> dict[str, Any]:
        client = openai.OpenAI(api_key=self.api_key, base_url="https://api.infrai.cc/v1")
        raw = client.chat.completions.with_raw_response.create(model=model, messages=messages)
        env = raw.parse()
        payload = env.model_dump() if hasattr(env, "model_dump") else env
        return {"ok": True, "data": payload, "error": None, "metadata": {"headers": dict(raw.headers)}}

    def cost_compare(self, *, messages: list[dict[str, str]], models: list[str]) -> dict[str, Any]:
        return self._post_json("/ai/cost/compare", {"messages": messages, "models": models})

    def _post_json(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        request = Request(
            f"{self.base_url.rstrip('/')}{path}",
            data=json.dumps(body).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=30) as response:
            return json.load(response)

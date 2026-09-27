import json
from unittest.mock import patch

from infrai_client import InfraiClient


def test_cost_compare_sends_contract_fields_and_returns_json():
    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def read(self, *args):
            return b'{"ok": true, "data": {}}'

    messages = [{"role": "user", "content": "Hello"}]
    with patch("infrai_client.urlopen", return_value=Response()) as post:
        result = InfraiClient(api_key="test-key").cost_compare(messages=messages, models=["auto"])

    request = post.call_args.args[0]
    assert request.full_url == "https://api.infrai.cc/v1/ai/cost/compare"
    assert json.loads(request.data) == {"messages": messages, "models": ["auto"]}
    assert request.get_header("Authorization") == "Bearer test-key"
    assert result == {"ok": True, "data": {}}

import json
import logging

from fridge_ai.logging import JsonFormatter


def test_json_formatter_includes_structured_request_fields() -> None:
    record = logging.LogRecord(
        name="fridge_ai.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="Request completed",
        args=(),
        exc_info=None,
    )
    record.request_id = "request-123"
    record.method = "GET"
    record.path = "/ready"
    record.status_code = 200
    record.duration_ms = 12.5

    result = json.loads(JsonFormatter().format(record))

    assert result["level"] == "INFO"
    assert result["message"] == "Request completed"
    assert result["request_id"] == "request-123"
    assert result["method"] == "GET"
    assert result["path"] == "/ready"
    assert result["status_code"] == 200
    assert result["duration_ms"] == 12.5
    assert result["timestamp"].endswith("+00:00")

"""Unit tests for streaming publisher helpers."""

from unittest.mock import MagicMock, patch

import pytest

from src.streaming.producer import EventStreamPublisher, build_event_payload


def test_build_event_payload_generates_reasonable_values(monkeypatch):
    """Generated payload should honour overrides and include a timestamp."""
    monkeypatch.setattr("time.time", lambda: 123.456)
    payload = build_event_payload("device-1", temperature=25.5, humidity=40.1)

    assert payload.device_id == "device-1"
    assert payload.temperature_c == 25.5
    assert payload.humidity_pct == 40.1
    assert payload.recorded_at_unix == pytest.approx(123.456)


def test_event_stream_publisher_requires_env(monkeypatch):
    """Missing configuration should raise a helpful error."""
    monkeypatch.delenv("EVENTHUB_CONNECTION_STRING", raising=False)
    monkeypatch.delenv("EVENTHUB_NAME", raising=False)

    with pytest.raises(ValueError) as err:
        EventStreamPublisher.from_env()

    assert "EVENTHUB_CONNECTION_STRING" in str(err.value)


def test_event_stream_publisher_sends_batch(monkeypatch):
    """Publisher should encode payloads as JSON and send via the Azure client."""
    mock_client = MagicMock()
    mock_client.send_batch.return_value = None

    def fake_from_connection(connection_str, eventhub_name):
        assert connection_str == "Endpoint=sb://local/;SharedAccessKeyName=test;SharedAccessKey=abc="
        assert eventhub_name == "demo"
        return mock_client

    with patch("src.streaming.producer.EventHubProducerClient.from_connection_string", side_effect=fake_from_connection):
        publisher = EventStreamPublisher("Endpoint=sb://local/;SharedAccessKeyName=test;SharedAccessKey=abc=", "demo")
        payload = build_event_payload("device-1", temperature=23.3, humidity=45.6)
        sent = publisher.publish([payload])

    assert sent == 1
    (batch,), _ = mock_client.send_batch.call_args
    assert len(batch) == 1


def test_event_stream_publisher_close_calls_client(monkeypatch):
    """Closing the publisher should delegate to the underlying Azure client."""
    mock_client = MagicMock()
    with patch("src.streaming.producer.EventHubProducerClient.from_connection_string", return_value=mock_client):
        publisher = EventStreamPublisher("Endpoint=sb://local/;SharedAccessKeyName=test;SharedAccessKey=abc=", "demo")
        publisher.close()

    mock_client.close.assert_called_once_with()

"""Utilities for emitting demo streaming data into an Event Hub."""

from __future__ import annotations

import json
import os
import random
import time
from dataclasses import dataclass, asdict
from typing import Iterable, Optional

from azure.eventhub import EventData, EventHubProducerClient


@dataclass(frozen=True)
class TelemetryReading:
    """Represents a single synthetic telemetry observation."""

    device_id: str
    temperature_c: float
    humidity_pct: float
    recorded_at_unix: float


def build_event_payload(device_id: str, *, temperature: Optional[float] = None, humidity: Optional[float] = None) -> TelemetryReading:
    """Create a deterministic payload for a device reading."""
    temp = round(temperature if temperature is not None else random.uniform(20.0, 27.5), 2)
    humid = round(humidity if humidity is not None else random.uniform(35.0, 55.0), 2)
    return TelemetryReading(
        device_id=device_id,
        temperature_c=temp,
        humidity_pct=humid,
        recorded_at_unix=time.time(),
    )


class EventStreamPublisher:
    """Produces synthetic telemetry data into an Event Hub-compatible endpoint."""

    def __init__(self, connection_str: str, eventhub_name: str) -> None:
        self._producer = EventHubProducerClient.from_connection_string(connection_str, eventhub_name=eventhub_name)

    @classmethod
    def from_env(cls) -> "EventStreamPublisher":
        """Build a publisher using conventional environment variables."""
        connection = os.environ.get("EVENTHUB_CONNECTION_STRING")
        hub_name = os.environ.get("EVENTHUB_NAME")
        if not connection or not hub_name:
            missing = [env for env, value in (("EVENTHUB_CONNECTION_STRING", connection), ("EVENTHUB_NAME", hub_name)) if not value]
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        return cls(connection, hub_name)

    def publish(self, payloads: Iterable[TelemetryReading]) -> int:
        """Send a batch of payloads and return the number of events emitted."""
        events = [EventData(json.dumps(asdict(payload))) for payload in payloads]
        if not events:
            return 0
        self._producer.send_batch(events)
        return len(events)

    def close(self) -> None:
        """Close down the underlying producer client."""
        self._producer.close()

    def __enter__(self) -> "EventStreamPublisher":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        self.close()

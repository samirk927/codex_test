# Streaming POC Guide

This proof-of-concept demonstrates how to run a Python streaming producer inside Docker and forward events to the Azure Event Hubs Emulator.

## Prerequisites
- Docker Desktop or a compatible container runtime.
- Python 3.11 (only required if you prefer running the producer locally without Docker).
- Copy `.env.example` to `.env` and adjust values if desired.

The Event Hubs emulator exposes a default connection string that is already captured in `.env.example`. Override it if you connect to a real Azure namespace later.

## Running the Stack
```bash
docker compose up --build
```

Compose starts two services:
- `eventhubs`: runs the official Event Hubs Emulator container. Set `EVENTHUBS_EMULATOR_IMAGE` in `.env` to the image reference or a locally built emulator image.
- `producer`: builds the repository image and executes `python -m src.streaming.main`.

The producer emits five batches of demo telemetry by default. Tail the logs with `docker compose logs -f producer` to observe the stream. Adjust iterations, batch size, or other flags via `docker compose run producer --iterations 20`.

## Using the Producer Locally
Activate the virtual environment and run:
```bash
source .venv/bin/activate
python -m src.streaming.main --iterations 3 --batch-size 5
```

Ensure the emulator is running in another terminal (`docker compose up eventhubs`) before invoking the script.

## Switching to Azure Event Hubs
1. Provision an Event Hubs namespace and hub.
2. Update `EVENTHUB_CONNECTION_STRING` and `EVENTHUB_NAME` in `.env`.
3. Restart the producer container (`docker compose up --build producer`) or rerun the local script.

Validate ingress using `EventHubConsumerClient` in a separate process or Azure tools such as the Service Bus Explorer.

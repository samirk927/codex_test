"""Command-line entry point for the demo streaming producer."""

from __future__ import annotations

import argparse
import itertools
import sys
import time

from .producer import EventStreamPublisher, build_event_payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emit demo telemetry into an Event Hub-compatible endpoint.")
    parser.add_argument("--device-prefix", default="device", help="Prefix used when generating device identifiers.")
    parser.add_argument("--device-count", type=int, default=5, help="Number of synthetic devices to simulate.")
    parser.add_argument("--batch-size", type=int, default=10, help="Number of readings to emit per batch.")
    parser.add_argument("--interval", type=float, default=2.0, help="Seconds to wait between batches.")
    parser.add_argument("--iterations", type=int, default=5, help="Number of batches to send before exiting.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    identifiers = [f"{args.device_prefix}-{index:03d}" for index in range(1, args.device_count + 1)]

    try:
        publisher = EventStreamPublisher.from_env()
    except ValueError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    with publisher:
        for iteration in range(args.iterations):
            payloads = [build_event_payload(device_id) for device_id in itertools.islice(itertools.cycle(identifiers), args.batch_size)]
            count = publisher.publish(payloads)
            print(f"[info] iteration={iteration + 1} published={count}")
            time.sleep(args.interval)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

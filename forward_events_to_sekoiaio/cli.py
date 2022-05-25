import argparse
import logging

from .chunker import Chunker
from .constants import SEKOIAIO_INTAKE_HOST
from .forwarder import Forwarder
from .helpers import normalize_events, reader


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Send events to SEKOIA.IO")
    parser.add_argument("intake_key", type=str, help="Intake Key to use")
    parser.add_argument(
        "events_file", type=str, help="The file containing the events to send"
    )
    parser.add_argument(
        "--chunk-size", type=int, help="The size of chunks", default=10000
    )
    parser.add_argument(
        "--select-types",
        type=str,
        help="The event types to send (accept a list with comma as separator)",
        default="Event::Endpoint::*",
    )

    return parser


def main():
    logger = logging.getLogger("events_forwarder")
    parser: argparse.ArgumentParser = get_parser()
    args = parser.parse_args()

    forwarder = Forwarder(SEKOIAIO_INTAKE_HOST, args.intake_key, logger)
    chunker = Chunker(args.chunk_size)

    with reader(args.events_file) as f:
        events = normalize_events(f.readlines())
        chunks = chunker.chunk(events)
        for chunk in chunks:
            forwarder.send(chunk)

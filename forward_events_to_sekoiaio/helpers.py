import sys
from contextlib import contextmanager
from typing import Generator, Sequence


@contextmanager
def reader(filepath: str):
    if filepath.strip() == "-":
        yield sys.stdin
    else:
        with open(filepath, "r") as f:
            yield f


def normalize_events(events: Sequence) -> Generator[str, None, None]:
    """
    Normalize the events

    Steps:
     - Remove new-line character from lines
    """
    for event in events:
        if event[-1] == "\n":
            yield event[:-1]
        else:
            yield event

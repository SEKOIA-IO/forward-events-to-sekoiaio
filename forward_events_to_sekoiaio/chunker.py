from typing import Generator, Sequence


class Chunker:
    """
    Split a sequence of events into fixed-size of chunks
    """

    def __init__(self, chunk_size: int):
        """
        :param int chunk_size: The size of chunks
        """
        self.chunk_size = chunk_size

    def chunk(self, events: Sequence) -> Generator[list, None, None]:
        """
        Chunk events into smaller groups

        :param Sequence events: The list of events to split
        """
        chunk: list = []

        # iter over the events
        for event in events:

            # if the chnuk is full
            if len(chunk) >= self.chunk_size:
                # yield the current chunk and create a new one
                yield chunk
                chunk = []

            # add the event to the current chunk
            chunk.append(event)

        # if the last chunk is not empty
        if len(chunk) > 0:
            # yield the last chunk
            yield chunk

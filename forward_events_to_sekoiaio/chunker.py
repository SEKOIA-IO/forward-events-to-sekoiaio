from forward_events_to_sekoiaio.constants import CHUNK_BYTES_MAX_SIZE


class Chunker:
    """
    Split a sequence of events into fixed-size of chunks
    """

    def __init__(self, chunk_size, bytes_max_size=CHUNK_BYTES_MAX_SIZE):
        """
        :param int chunk_size: The size of chunks
        """
        self.__chunk_size = chunk_size
        self.__bytes_max_size = bytes_max_size

    def chunk(self, events):
        """
        Chunk events into smaller groups

        :param Sequence events: The list of events to split
        """
        chunk: list = []
        chunk_bytes = 0

        # iter over the events
        for event in events:

            # if the chunk is full or exceed maximal chunk size
            if (
                len(chunk) >= self.__chunk_size
                or chunk_bytes + len(event) > self.__bytes_max_size
            ):
                # yield the current chunk and create a new one
                yield chunk
                chunk = []
                chunk_bytes = 0

            # add the event to the current chunk
            chunk.append(event)
            chunk_bytes += len(event)

        # if the last chunk is not empty
        if len(chunk) > 0:
            # yield the last chunk
            yield chunk

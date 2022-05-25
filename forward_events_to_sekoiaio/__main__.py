import logging
import sys

from .cli import get_parser, main

if __name__ == "__main__":

    logging.basicConfig(
        format='app=%(name)s\tlevel=%(levelname)s\tdate=%(asctime)s\tmsg="%(message)s"\turl=%(url)s\tstatus_code=%(status_code)d\tresponse=%(response)s',
        level=logging.INFO,
        stream=sys.stderr,
    )

    main()

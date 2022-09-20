import logging
from functools import cached_property
from typing import Sequence
from urllib.parse import urljoin

import requests
import tenacity


class Forwarder:
    """
    Forward events to SEKOIA.IO
    """

    def __init__(self, intake_host, intake_key, logger):
        self.intake_host = intake_host
        self.intake_key = intake_key
        self.logger = logger
        self.session = requests.Session()

    @cached_property
    def url(self):
        return urljoin(self.intake_host, "/batch")

    def send(self, events):
        """
        Forward events

        :param Sequence events: The list of events to send
        """
        list_of_events = list(events)

        try:
            for attempt in tenacity.Retrying(
                stop=tenacity.stop_after_attempt(5),
                wait=tenacity.wait_exponential(multiplier=2, min=1, max=10),
                retry=tenacity.retry_if_exception_type(requests.Timeout),
            ):
                with attempt:
                    response: requests.Response = self.session.post(
                        self.url,
                        json={"intake_key": self.intake_key, "jsons": list_of_events},
                    )

                    if not response.ok:
                        self.logger.error(
                            f"Failed to send {len(list_of_events)} events to {self.intake_host}",
                            extra=dict(
                                url=self.url,
                                status_code=response.status_code,
                                response=response.content,
                            ),
                        )
                    else:
                        self.logger.info(
                            f"sent {len(list_of_events)} events to {self.intake_host}",
                            extra=dict(
                                url=self.url,
                                status_code=response.status_code,
                                response=",".join(response.json().get("event_ids")),
                            ),
                        )
        except tenacity.RetryError as error:
            self.logger.exception(
                f"Failed to send {len(list_of_events)} events to {self.intake_host}",
                exc_info=error,
            )

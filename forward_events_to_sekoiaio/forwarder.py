import json
from functools import cached_property
from typing import Sequence
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter, Retry

from forward_events_to_sekoiaio.constants import INTAKE_PAYLOAD_BYTES_MAX_SIZE

retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])


class Forwarder:
    """
    Forward events to SEKOIA.IO
    """

    def __init__(self, intake_host, intake_key, logger):
        self.intake_host = intake_host
        self.intake_key = intake_key
        self.logger = logger
        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

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
            payload = {"intake_key": self.intake_key, "jsons": list_of_events}
            request_body = json.dumps(payload)

            body_len = len(request_body)
            if body_len > INTAKE_PAYLOAD_BYTES_MAX_SIZE:
                self.logger.warning(
                    (
                        "The events exceeds the maximun length allowed. Expected less than "
                        f"{INTAKE_PAYLOAD_BYTES_MAX_SIZE/1024}kio. Got {body_len} bytes"
                    ),
                    extra=dict(
                        url=self.url,
                        status_code=None,
                        response=None,
                    ),
                )

            response: requests.Response = self.session.post(
                self.url,
                data=request_body,
                headers={"Content-Type": "application/json"},
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
        except Exception as error:
            self.logger.exception(
                f"Failed to send {len(list_of_events)} events to {self.intake_host}",
                exc_info=error,
            )

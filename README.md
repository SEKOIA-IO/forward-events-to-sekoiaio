# Forward events to SEKOIA.IO

This script helps to send events from a file to SEKOIA.IO.


## Requirements

This script requires at Python3 

## Installation

Create a Python virtual environment:

```bash
$ python3 -m venv <path to the venv>
```

Install the dependencies:

```bash
$ <path to the venv>/bin/pip3 install -Ur requirements.txt
```

## Create the intake

Go to the [intake page](https://app.sekoia.io/operations/intakes) and create a new intake from the format Sophos EDR.
Copy the resulting intake key.

## Send events

```bash
$ <path to the venv>/bin/python3 -m forward_events_to_sekoiaio <intake_key> <file containing the events to send>
```

The script have the following options:

- `--chunk-size`: Events are splitted in chunks. This option allows to define the maximal size of a chunk.

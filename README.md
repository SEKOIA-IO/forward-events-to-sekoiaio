# Forward events to SEKOIA.IO

This script helps to send events from a file (line-oriented) to SEKOIA.IO.


## Requirements

This script requires at Python3 

## Installation

Get the module from the releases or clone the repository:

```bash
$ git clone https://github.com/SEKOIA-IO/forward-events-to-sekoiaio .
$ cd forward-events-to-sekoiaio
```

Create a Python virtual environment:

```bash
$ python3 -m venv <path to the venv>
```

Install the dependencies:

```bash
$ <path to the venv>/bin/pip3 install -Ur requirements.txt
```

## Create the intake

Go to the [intake page](https://app.sekoia.io/operations/intakes) and create a new intake from the expected format.
Copy the resulting intake key.

## Send events

The script is line-oriented, reading one event per line from the input.

```bash
$ <path to the venv>/bin/python3 -m forward_events_to_sekoiaio <intake_key> <file containing the events to send>
```

The script have the following options:

- `--chunk-size`: Events are splitted in chunks. This option allows to define the maximal size of a chunk.

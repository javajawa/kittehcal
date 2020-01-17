#!/usr/bin/env python3
# vim: ts=4 expandtab

from __future__ import annotations

from typing import Dict, List
from datetime import date, timedelta

import json
import itertools

from event import Event, EventGenerator, EventJSONEncoder, TagDict

import listed_events
import regular_events


def read_tags() -> TagDict:
    tags: TagDict = dict()

    with open('tags', 'r') as tag_file:
        while True:
            line = tag_file.readline()

            if not line:
                break

            line = line.strip()

            if not line or line.startswith('#'):
                continue

            name, uuid = line.strip().split('\t')
            tags[name.lower()] = uuid.lower()

    return tags


def get_events(tags: TagDict) -> itertools.chain[Event]:
    start: date = date.today()
    end: date = start + timedelta(days=-start.weekday(), weeks=16)
    start = start + timedelta(days=-start.weekday(), weeks=-2)

    functions: List[EventGenerator] = [listed_events.generator, regular_events.generator]

    return itertools.chain(*[lamb(start, end, tags) for lamb in functions])


def main():
    tags = read_tags()

    acc: List[Event] = []
    tag_map: Dict[str, List[str]] = {}

    for event in get_events(tags):
        for tag in event.tags:
            if tag not in tag_map:
                tag_map[tag] = []

            tag_map[tag].append(event.event)

        acc.append(event)

    with open('data.json', 'w') as output:
        json.dump(acc, output, indent=2, cls=EventJSONEncoder)

    for tag in tag_map:
        with open(tag + '.json', 'w') as output:
            json.dump(tag_map[tag], output, indent=2)


if __name__ == '__main__':
    main()

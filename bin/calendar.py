#!/usr/bin/python3
# vim: ts=4 expandtab

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from datetime import date, timedelta
from typing import Dict, List, Generator, Optional

import json
import itertools

from third_days import earliest, latest, from_date, ThirdDay


class EventType(Enum):
    BUSY = 'busy'
    MOVEABLE = 'moveable'


@dataclass
class Event:
    event: str
    title: Optional[str]
    start: ThirdDay
    end: ThirdDay
    type: EventType
    tags: List[str] = field(default_factory=list)


class EventJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Event):
            return json.JSONEncoder.default(self, obj)

        return {
            'id': obj.event,
            'title': obj.title,
            'class': obj.type.value,
            'start': str(obj.start),
            'end': str(obj.end)
        }


def read_tags() -> Dict[str, str]:
    tags: Dict[str, str] = dict()

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


def events(tags: Dict[str, str]) -> Generator[Event]:
    i: int = 0

    with open('calendar', 'r') as in_file:
        while True:
            line: str = in_file.readline()

            if not line:
                break

            line = line.strip()

            if not line or line.startswith('#'):
                continue

            date_str, title = line.strip().split(' ', 1)

            mode: EventType = EventType.BUSY

            if date_str.endswith('?'):
                mode = EventType.MOVEABLE
                date_str = date_str[:-1]

            start_date = earliest(date_str)
            end_date = latest(date_str)

            if title.strip() == '--':
                line = in_file.readline()
                date_str, title = line.strip().split(' ', 1)
                end_date = latest(date_str)

            title = title.strip()
            i += 1
            event = str(start_date) + '-' + str(i)
            event_tags = [tags[k] for k in tags if k in title.lower()]

            yield Event(event, None, start_date, end_date, mode, event_tags)

def normal() -> Generator[Event]:
    a_day: timedelta = timedelta(days=1)

    ptr: date = date.today()
    end: date = ptr + timedelta(days=-ptr.weekday(), weeks=16)
    ptr: date = ptr + timedelta(days=-ptr.weekday(), weeks=-2)

    holidays: List[date] = []

    with open('holidays', 'r') as holidays_in:
        for holiday in holidays_in.readlines():
            bits = holiday.strip().split('-', 2)

            if len(bits) != 3:
                continue

            year, month, day = bits

            holidays.append(date(int(year), int(month), int(day)))

    while ptr < end:
        if ptr not in holidays and ptr.weekday() < 4:
            e_start = from_date(ptr, 'M')
            e_end = from_date(ptr, 'A')
            yield Event("work-" + str(ptr), "Work", e_start, e_end, EventType.MOVEABLE)

        if ptr not in holidays and ptr.weekday() == 6:
            day = from_date(ptr, 'M')
            yield Event("market-" + str(ptr), "Market", day, day, EventType.MOVEABLE)

        ptr += a_day


def main():
    tags = read_tags()

    acc: List[Event] = []
    tag_map: Dict[str, List[str]] = {}

    for event in itertools.chain(events(tags), normal()):
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

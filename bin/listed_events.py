#!/usr/bin/env python3
# vim: ts=4 expandtab

from __future__ import annotations

from datetime import date

from event import Event, EventType, TagDict, EventList
from third_days import earliest, latest
from utils import read_skip_comments

def generator(start: date, end: date, tags: TagDict) -> EventList:
    i: int = 0

    with open('data/calendar', 'r') as in_file:
        for line in read_skip_comments(in_file):
            date_str, title = line.strip().split(' ', 1)

            mode: EventType = EventType.BUSY

            if date_str.endswith('?'):
                mode = EventType.MOVEABLE
                date_str = date_str[:-1]

            start_date = earliest(date_str)
            end_date = latest(date_str)

            if start_date.day > end or end_date.day < start:
                continue

            if title.strip() == '--':
                line = in_file.readline()
                date_str, title = line.strip().split(' ', 1)

                if date_str.endswith('?'):
                    mode = EventType.MOVEABLE
                    date_str = date_str[:-1]

                end_date = latest(date_str)

            title = title.strip()
            i += 1
            event = str(start_date) + '-' + str(i)
            event_tags = [tags[k] for k in tags if k in title.lower()]

            yield Event(event, None, start_date, end_date, mode, event_tags)

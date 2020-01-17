#!/usr/bin/env python3
# vim: ts=4 expandtab

from __future__ import annotations

from datetime import date, timedelta
from typing import List, Generator

from event import Event, EventList, EventType, TagDict
from third_days import from_date, ThirdDay


def get_holidays(start: date, end: date) -> Generator[date, None, None]:
    with open('holidays', 'r') as holidays_in:
        for holiday in holidays_in.readlines():
            bits = holiday.strip().split('-', 2)

            if len(bits) != 3:
                continue

            year, month, day = bits

            holidate = date(int(year), int(month), int(day))

            if start <= holidate <= end:
                yield holidate


def simple_event(name: str, start: ThirdDay, end: ThirdDay, tags=None) -> Event:
    return Event(
        name.lower() + '-' + str(start),
        name, start, end,
        EventType.MOVEABLE,
        tags if tags else []
    )


def generator(start: date, end: date, tags: TagDict) -> EventList:
    a_day: timedelta = timedelta(days=1)
    holidays: List[date] = list(get_holidays(start, end))

    ptr: date = start

    while ptr < end:
        if ptr not in holidays and ptr.weekday() < 4:
            e_start = from_date(ptr, 'M')
            e_end = from_date(ptr, 'A')
            yield simple_event("Work", e_start, e_end)

        if ptr not in holidays and ptr.weekday() == 6:
            day = from_date(ptr, 'M')
            yield simple_event("Market", day, day)

        ptr += a_day

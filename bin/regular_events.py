#!/usr/bin/env python3
# vim: ts=4 expandtab

from __future__ import annotations

from datetime import date, timedelta
from typing import List, Generator, Optional, Tuple

from event import Event, EventList, EventType, TagDict
from third_days import from_date, ThirdDay
from utils import read_skip_comments


# pylint: disable=too-many-instance-attributes
class DateMatcher:
    title: str
    slot_start: str
    slot_end: str

    year: Optional[int] = None
    month: Optional[int] = None
    iso_week: Optional[int] = None
    month_week: Optional[int] = None
    dow: Optional[int] = None
    day: Optional[int] = None

    def __init__(self: DateMatcher, specifier: str, start: str, end: str, event: str):
        self.title = event
        self.slot_start = start
        self.slot_end = end

        spec = specifier.replace('*', '-')

        # The first element is the year
        token, spec = self.next_token(spec)
        self.year = int(token) if token else None

        # After the year is either the ISO week,
        # or the month number
        if spec[0] == 'W':
            token, spec = self.next_token(spec[1:])
            self.iso_week = int(token) if token else None

            token, spec = self.last_token(spec)
            self.dow = int(token) if token else None

        else:
            token, spec = self.next_token(spec)

            if token and token.contains('w'):
                month, week = token.split('w')

                self.month = int(month) if month != '-' else None
                self.month_week = int(week) if week != 'l' else -1

                token, spec = self.last_token(spec)
                self.dow = int(token) if token else None

            else:
                self.month = int(token) if token else None

                token, spec = self.last_token(spec)
                self.day = int(token) if token else None

        if spec:
            raise ValueError("Error in specifier: " + specifier)

    # pylint: disable=no-self-use
    def next_token(self: DateMatcher, spec: str) -> Tuple[Optional[str], str]:
        if spec[0] == '-':
            if spec[1] != '-':
                raise ValueError('Invalid Specifier')

            return None, spec[2:]

        return spec.split('-', 1)

    # pylint: disable=no-self-use
    def last_token(self: DateMatcher, spec: str) -> Tuple[Optional[str], str]:
        if '-' in spec:
            raise ValueError("Expected last token, but found a -")

        return spec, ''

    def matches(self: DateMatcher, day: date) -> bool:
        _, iso_week, dow = day.isocalendar()

        if self.year and self.year != day.year:
            return False

        if self.month and self.month != day.month:
            return False

        if self.iso_week and self.iso_week != iso_week:
            return False

        if self.month_week:
            raise Exception("I have not implemented month weeks")

        if self.dow and self.dow != dow:
            return False

        if self.day and self.day != date.day:
            return False

        return True


def get_formats() -> Generator[DateMatcher, None, None]:
    with open('data/regular-events', 'r') as patterns_in:
        for line in read_skip_comments(patterns_in):
            yield DateMatcher(*line.split(' ', 3))


def get_holidays(start: date, end: date) -> Generator[date, None, None]:
    with open('data/holidays', 'r') as holidays_in:
        for line in read_skip_comments(holidays_in):
            bits = line.strip().split('-', 2)

            if len(bits) != 3:
                continue

            year, month, day = bits

            holidate = date(int(year), int(month), int(day))

            if start <= holidate <= end:
                yield holidate


def simple_event(name: str, start: ThirdDay, end: ThirdDay, tags=None) -> Event:
    name, *_ = name.split(None, 1)

    return Event(
        name.lower() + '-' + str(start),
        name, start, end,
        EventType.MOVEABLE,
        tags if tags else []
    )


def generator(start: date, end: date, tags: TagDict) -> EventList:
    a_day: timedelta = timedelta(days=1)
    holidays: List[date] = list(get_holidays(start, end))
    events: List[DateMatcher] = list(get_formats())

    ptr: date = start - a_day

    while ptr < end:
        ptr += a_day

        if ptr in holidays:
            continue

        for event in events:
            if event.matches(ptr):
                e_start = from_date(ptr, event.slot_start)
                e_end = from_date(ptr, event.slot_end)
                event_tags = [tags[k] for k in tags if k in event.title.lower()]

                yield simple_event(event.title, e_start, e_end, event_tags)

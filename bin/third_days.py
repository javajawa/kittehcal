#!/usr/bin/python3
# vim: ts=4 expandtab

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

SLOTS = ["M", "A", "E"]


@dataclass
class ThirdDay:
    day: date
    slot: str

    def __str__(self: ThirdDay):
        return '%04d-%02d-%02d-%s' % (self.day.year, self.day.month, self.day.day, self.slot)


def earliest(date_str: str) -> ThirdDay:
    years, months, days, *slots = date_str.split('-', 3)

    year: int = int(years)
    month: int = int(months)
    day: int = int(days)

    if not slots:
        return ThirdDay(date(year, month, day), SLOTS[0])

    slots = list(slots[0])
    slot = len(SLOTS) - 1

    if not slots:
        slot = 0

    for slot_str in slots:
        slot = min(slot, SLOTS.index(slot_str))

    return ThirdDay(date(year, month, day), SLOTS[slot])


def latest(date_str: str) -> ThirdDay:
    years, months, days, *slots = date_str.split('-', 3)

    year: int = int(years)
    month: int = int(months)
    day: int = int(days)

    if not slots:
        return ThirdDay(date(year, month, day), SLOTS[-1])

    slots = list(slots[0])
    slot = 0

    if not slots:
        slot = len(SLOTS) - 1

    for slot_str in slots:
        slot = max(slot, SLOTS.index(slot_str))

    return ThirdDay(date(year, month, day), SLOTS[slot])


def from_date(day: date, slot: str) -> ThirdDay:
    if slot not in SLOTS:
        raise ValueError("Invalid slot " + slot)

    return ThirdDay(day, slot)

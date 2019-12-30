#!/usr/bin/python3
# vim: ts=4 expandtab

from __future__ import annotations

from dataclasses import dataclass

SLOTS = ["M", "A", "E"]


@dataclass
class ThirdDay:
    year: int
    month: int
    day: int
    slot: str


    def __str__(self: ThirdDay):
        return '%04d-%02d-%02d-%s' % (self.year, self.month, self.day, self.slot)


def earliest(date_str: str) -> ThirdDay:
    year, month, day, *slots = date_str.split('-', 3)

    year: int = int(year)
    month: int = int(month)
    day: int = int(day)

    if not slots:
        return ThirdDay(year, month, day, SLOTS[0])

    slots = slots[0]
    slot = len(SLOTS) - 1

    if len(slots) == 0:
        slot = 0

    for slot_str in slots:
        slot = min(slot, SLOTS.index(slot_str))

    return ThirdDay(year, month, day, SLOTS[slot])


def latest(date_str: str) -> ThirdDay:
    year, month, day, *slots = date_str.split('-', 3)

    year: int = int(year)
    month: int = int(month)
    day: int = int(day)

    if not slots:
        return ThirdDay(year, month, day, SLOTS[-1])

    slots = slots[0]
    slot = 0

    if len(slots) == 0:
        slot = len(SLOTS) - 1

    for slot_str in slots:
        slot = max(slot, SLOTS.index(slot_str))

    return ThirdDay(year, month, day, SLOTS[slot])


def from_date(date: 'datetime.date', slot: str) -> ThirdDay:
    if slot not in SLOTS:
        raise ValueError("Invalid slot " + slot)

    return ThirdDay(date.year, date.month, date.day, slot)

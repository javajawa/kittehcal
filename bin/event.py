#!/usr/bin/env python3
# vim: ts=4 expandtab

from __future__ import annotations

from enum import Enum
from json import JSONEncoder
from dataclasses import dataclass, field
from datetime import date
from typing import Callable, Dict, Generator, List, Optional

from third_days import ThirdDay

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


class EventJSONEncoder(JSONEncoder):
    def default(self, o):  # pylint: disable=method-hidden
        obj = o
        if not isinstance(obj, Event):
            return JSONEncoder.default(self, obj)

        return {
            'id': obj.event,
            'title': obj.title,
            'class': obj.type.value,
            'start': str(obj.start),
            'end': str(obj.end)
        }


TagDict = Dict[str, str]
EventList = Generator[Event, None, None]
EventGenerator = Callable[[date, date, TagDict], EventList]

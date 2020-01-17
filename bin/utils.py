#!/usr/bin/env python3
# vim: ts=4 expandtab

from __future__ import annotations

from typing import Generator, IO


def read_skip_comments(stream: IO) -> Generator[str, None, None]:
    while True:
        line = stream.readline()

        if not line:
            return

        line = line.strip()

        if not line or line.startswith('#'):
            continue

        yield line

#!/usr/bin/env python
# Copyright © 2022-present, Lightspark Group, Inc. - All Rights Reserved
from os import getcwd, path
from sys import stdin

from unidiff import PatchSet


def escape(s):
    return s.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


patchset = PatchSet.from_string(stdin.read())


for patch in patchset:
    for hunk in patch:
        context = [line.is_context for line in hunk]
        before_context = context.index(False)
        context.reverse()
        after_context = len(context) - context.index(False)
        diff = escape("".join(str(line) for line in hunk[before_context:after_context]))
        start_line = hunk.source_start + before_context
        end_line = hunk.source_start + hunk.source_length - context.index(False) - 1
        filename = path.join(getcwd(), patch.source_file)
        print(
            f"::notice file={filename},line={start_line},endLine={end_line},title=Python formatting::{diff}"
        )

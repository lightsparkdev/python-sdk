# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

import json
from datetime import datetime, timezone
from enum import Enum


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Enum):
            return o.name
        if isinstance(o, datetime):
            return o.replace(tzinfo=timezone.utc).isoformat()
        return json.JSONEncoder.default(self, o)

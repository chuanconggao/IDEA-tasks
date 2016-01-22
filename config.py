#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import json

with open("config.json") as f:
    j = json.load(f)

    binDir = j["storage"]["bin"]
    dataDir = j["storage"]["data"]
    tempDir = j["storage"]["temp"]

    tasksDir = j["tasksDir"]

    redisHost = j["redis"]["host"]
    redisPassword = j["redis"]["password"]

redisQueuePrefix = "IDEA:"

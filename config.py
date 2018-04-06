#!/usr/bin/env python3

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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os
import os.path

import subprocess

from config import tasksDir, redisQueuePrefix, redisHost, redisPassword

if __name__ == '__main__':
    tasks = sys.argv[1:]

    new_env = os.environ.copy()
    new_env["PYTHONPATH"] = ":".join(os.path.join(tasksDir, t) for t in tasks)

    args = [
        "rqworker", "-q", "-u", "redis://:{}@{}:6379/".format(redisPassword, redisHost),
    ] + [
        (redisQueuePrefix + t) for t in tasks
    ]

    try:
        subprocess.call(" ".join(args), env=new_env, shell=True)
    except KeyboardInterrupt:
        pass

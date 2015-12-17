#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os
import os.path

from sh import rqworker

from config import tasksDir, redisQueuePrefix, redisHost, redisPassword
from aux import print2

if __name__ == '__main__':
    tasks = sys.argv[1:]

    new_env = os.environ.copy()
    new_env["PYTHONPATH"] = ":".join(os.path.join(tasksDir, t) for t in tasks)

    for l in rqworker(
            "-u", "redis://:{}@{}:6379/".format(redisPassword, redisHost),
            *[(redisQueuePrefix + t) for t in tasks],
            _iter="err", _env=new_env
        ):
        print2(l)

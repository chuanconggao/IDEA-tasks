#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

def getTopKTable(idStr, content, k, minLen, maxLen):
    import sys
    import os
    import subprocess
    import codecs

    sys.path.append("../../")
    from config import dataDir, tasksDir
    from aux import print2

    topKDir = os.path.join(dataDir, "topk")
    if not os.path.isdir(topKDir):
        os.mkdir(topKDir)

    fileName = os.path.join(
        topKDir,
        "_".join([
            idStr,
            "k=" + str(k),
            "minlen=" + str(minLen),
            "maxlen=" + str(maxLen)
        ])
    )
    inputFileName = fileName + ".in"
    outputFileName = fileName + ".out"

    if not os.path.isfile(outputFileName):
        print2("Mining \"{}\" with: k={}, minlen={}, maxlen={}...".format(
            idStr, k, minLen, maxLen
        ))

        with codecs.open(inputFileName, 'w', 'utf-8', errors="ignore") as f:
            for i in content:
                f.write(i)
                f.write('\n')

        args = [
            "mono \"{}\"".format(os.path.join("bin", "TopKSeqPattMiner.exe")),
            "--in=\"{}\"".format(inputFileName),
            "--stopwords=\"{}\"".format(os.path.join("bin", "stopwords.txt")),
            "-k=" + str(k),
            "--minlen=" + str(minLen),
            "--maxlen=" + str(maxLen)
        ]
        output, _ = subprocess.Popen(" ".join(args), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        res = [
            tuple(p.split(' : '))
            for p in output.decode("utf-8").splitlines()
        ][:k]

        with codecs.open(outputFileName, 'w', 'utf-8', errors="ignore") as f:
            for i in res:
                f.write(str(i[0]) + " : " + str(i[1]))
                f.write('\n')
    else:
        with codecs.open(outputFileName, 'r', 'utf-8', errors="ignore") as f:
            res = [
                tuple(p.strip().split(' : '))
                for p in f
            ]

    return [
        {"pattern" : p[0], "count" : int(p[1])}
        for p in res
    ]

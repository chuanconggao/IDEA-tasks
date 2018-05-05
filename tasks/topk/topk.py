#!/usr/bin/env python3

def getTopKTable(idStr, content, k, minLen, maxLen):
    import re
    import os

    from prefixspan import PrefixSpan
    from extratools.dicttools import invert, remap

    from aux import print2, getcwd

    print2("Mining \'{}\' with: k={}, minLen={}, maxLen={}...".format(
        idStr, k, minLen, maxLen
    ))

    with open(os.path.join(getcwd("topk"), "stopwords.txt")) as f:
        stopwords = {w.strip().lower() for w in f}

    cleaner = re.compile(r'\W+', re.U)

    docs = [
        [
            w for w in cleaner.split(i.strip().lower())
            if len(w) > 1 and w not in stopwords
        ]
        for i in content
    ]

    wordMap = {}

    db = [list(remap(doc, wordMap)) for doc in docs]

    ps = PrefixSpan(db)
    ps.minlen = int(minLen)
    ps.maxlen = int(maxLen)

    results = ps.topk(int(k), closed=True)

    invWordMap = invert(wordMap)

    return [
        {"pattern" : ' '.join(invWordMap[i] for i in patt), "count" : freq}
        for (freq, patt) in sorted(results, reverse=True, key=lambda p: p[0])
    ]

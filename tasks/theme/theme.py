#!/usr/bin/env python3

def computeStat(idStr, content, themeDict):
    from tagstats import compute

    from aux import print2

    print2("Theme \'{}\'".format(
        idStr
    ))

    results = {
        tag: {
            "total": 0,
            "ranges": {}
        }
        for tag in themeDict
    }

    for timeRange, texts in content.items():
        for tag, freqs in compute(texts, themeDict).items():
            freq = sum(freqs)
            results[tag]["total"] += freq
            results[tag]["ranges"][timeRange] = freq

    return results

#!/usr/bin/env python3

def computeStat(idStr, content, themeDict):
    from tagstats.tagstats import index
    from tagstats import compute
    from joblib import Parallel, delayed

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

    root = index(themeDict)

    for timeRange, stats in zip(
            content,
            Parallel(n_jobs=4)(
                delayed(compute)(texts, themeDict, root)
                for timeRange, texts in content.items()
            )
        ):
        for tag, freqs in stats.items():
            freq = sum(freqs)
            results[tag]["total"] += freq
            results[tag]["ranges"][timeRange] = freq

    return results

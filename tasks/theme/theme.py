#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from collections import defaultdict, namedtuple
import re

Node = namedtuple('Node', 'child, category')
spliter = re.compile(r'^[^\w@#/+-]+|\W*\s+[^\w@#/+-]*')

def build(themeDict):
    root = Node({}, set())
    for theme, phrasess in themeDict.items():
        for phrase in phrasess:
            node = root
            for word in phrase:
                if word not in node.child:
                    node.child[word] = Node({}, set())
                node = node.child[word]
            node.category.add(theme)
    return root

def search(root, content, themes):
    counter = {
        t: {
            "name": t,
            "total": 0,
            "articles": defaultdict(int)
        } for t in themes
    }
    for year, abstracts in content.items():
        for abstract in abstracts:
            matchThemes = _search(root, spliter.split(abstract))
            for t in matchThemes:
                counter[t]["total"] += 1
                counter[t]["articles"][year] += 1

    return counter

def _search(root, sentence):
    matched = defaultdict(set)
    startIndx = 0
    while startIndx < len(sentence):
        node = root
        matchWords = []
        for word in sentence[startIndx:]:
            if word in node.child:
                matchWords.append(word)
                node = node.child[word]
            else:
                break

        for category in node.category:
            matched[category].add('.'.join(matchWords))
        startIndx += 1
    return matched

def computeStat(idStr, content, themeDict):
    trie = build(themeDict)

    counter = search(trie, content, themeDict.keys())

    return counter

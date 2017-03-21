#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from collections import defaultdict, namedtuple, Counter
import regex as re

Node = namedtuple('Node', ['children', 'tags'])
tokenizer = re.compile(r'^[^\w@#/+-]+|\W*\s+[^\w@#/+-]*', re.U)

def build(themeDict):
    root = Node({}, set())
    for tag, phrases in themeDict.iteritems():
        for phrase in phrases:
            words = [w for w in tokenizer.split(phrase) if len(w) > 0]
            node = root
            for word in words:
                node = node.children.setdefault(word, Node({}, set()))
            node.tags.add(tag)
    return root

def search(root, content, themeDict):
    def _search(root, words):
        matched = Counter()

        for i in xrange(len(words)):
            node = root
            for word in words[i:]:
                if word not in node.children:
                    break

                node = node.children[word]

                for tag in node.tags:
                    matched[tag] += 1

        return matched

    counter = {
        t: {
            "total": 0,
            "ranges": {textRange: 0 for textRange in content}
        } for t in themeDict
    }

    for textRange, texts in content.iteritems():
        for text in texts:
            for t, c in _search(
                    root,
                    [w for w in tokenizer.split(text) if len(w) > 0]
                ).iteritems():
                counter[t]["total"] += c
                counter[t]["ranges"][textRange] += c

    return counter

def computeStat(idStr, content, themeDict):
    return search(build(themeDict), content, themeDict)

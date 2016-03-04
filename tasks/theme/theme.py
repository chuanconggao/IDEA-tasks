#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from collections import defaultdict, namedtuple
import re

Node = namedtuple('Node', 'child, category')
spliter = re.compile('^[^\w@#/+-]+|\W*\s+[^\w@#/+-]*')

class Trie:
    def __init__(self):
        self.root = Node({}, set())
    
    def build(self, themeDict):
        for theme, phrasess in themeDict.items():
            for phrase in phrasess:
                self._build(phrase, theme)
        return themeDict.keys()
    
    def search(self, content, themeDict):
        themes = self.build(themeDict)
        counter = {
                t : {
                    "name": t,
                    "total": 0,
                    "articles": defaultdict(int)
                } for t in themes}
        for year, abstracts in content.items():
            for abstract in abstracts:
                matchThemes = self._search(spliter.split(abstract))
                for t, words in matchThemes.items():
                    counter[t]["total"] += 1
                    counter[t]["articles"][year] += 1

        return counter

    def _build(self, words, category):
        node = self.root
        for word in words:
            if word not in node.child:
                node.child[word]=Node({}, set())
            node = node.child[word]
        node.category.add(category)

    def _search(self, sentence):
        matched = defaultdict(set)
        startIndx = 0
        while startIndx < len(sentence):
            node = self.root
            # Check at the end or on each node
            shift = 0
            matchWords = []
            for word in sentence[startIndx:]:
                if word in node.child:
                    matchWords.append(word)
                    node = node.child[word]
                    shift += 0
                else:
                    break

            for category in node.category:
                matched[category].add('.'.join(matchWords))
            startIndx += max([1, shift])
        return matched

def computeStat(idStr, content, themeDict):

    trie = Trie()

    counter = trie.search(content, themeDict)

    return counter

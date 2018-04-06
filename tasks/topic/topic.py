#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

def getTopicTable(idStr, content, k, wordNum):
    import re
    import os
    from io import open

    import gensim

    from aux import print2, getcwd

    with open(os.path.join(getcwd("topic"), "stopwords.txt")) as f:
        stopwords = {w.strip().lower() for w in f}

    cleaner = re.compile(r'\W+', re.U)

    print2("Modeling \'{}\' with: k={}, wordnum={}...".format(
        idStr, k, wordNum
    ))

    docs = [
        [
            w for w in cleaner.split(i.strip().lower())
            if w not in stopwords
        ]
        for i in content
    ]

    dictionary = gensim.corpora.Dictionary(docs)
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    model = gensim.models.ldamodel.LdaModel(corpus, id2word=dictionary)

    return [
        [
            topic for (topic, _) in topics
            if topic != ""
        ]
        for (_, topics) in model.show_topics(num_topics=k, num_words=wordNum, formatted=False)
    ]

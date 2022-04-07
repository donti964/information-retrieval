import pickle
from math import log


def addNode(node, s, value):
    x = s[0]
    if x not in node['ch']:
        node['ch'][x] = {"val": None, "ch": {}}

    if len(s) == 1:
        node['ch'][x]['val'] = value
    else:
        node = node['ch'][x]
        addNode(node, s[1:], value)


with open("parsed.txt") as f:
    count = {}
    tf = {}
    docno = None
    total = 0
    docno_list = []
    for line in f:
        line = line.strip()
        if len(line) == 0:
            for token in count:
                if token not in tf:
                    tf[token] = {}
                # docno = len(docno_list) - 1
                tf[token][docno] = count[token] / sum(count.values())
            total += 1
            docno = None
            count = {}
            continue

        if docno is None:
            docno = line
            docno_list.append(docno)
            continue

        if line[0] in "0123456789":
            continue

        if line not in count:
            count[line] = 0
        count[line] += 1

    idf = {}
    for token in tf:
        idf[token] = log(total / len(tf[token]))

    tfidf = {}
    for token in tf:
        tfidf[token] = {}
        for doc, score in tf[token].items():
            tfidf[token][doc] = score * idf[token]

    # root = {"val": None, "ch": {}}
    # for token, value in tfidf.items():
    #     addNode(root, token, value)

    new_tf_idf = {}
    for token, value in tfidf.items():
        value = sorted(value.items(), key=lambda x: -x[1])
        value = list(value)[:100]
        new_tf_idf[token] = {k[0]: k[1] for k in value}

    # with open("index.pkl", "wb") as f1:
    #     pickle.dump(root, f1)
    with open("index.pkl", "wb") as f1:
        pickle.dump(new_tf_idf, f1)

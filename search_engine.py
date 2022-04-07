import pickle
import sys
# from datetime import datetime

# start = datetime.now()
with open("index.pkl", "rb") as f:
    index = pickle.load(f)

for line in sys.stdin:
    scores = {}
    line = line.strip().lower()
    for token in line.split(" "):
        for doc, tfidf in index[token].items():
            if doc not in scores:
                scores[doc] = 0
            scores[doc] += tfidf
    scores = sorted(scores.items(), key=lambda x: -x[1])
    for item in scores:
        print("{} {}".format(*item))

# print(datetime.now() - start)


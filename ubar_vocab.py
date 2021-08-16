import json
from collections import defaultdict
from spacy.lang.pt import Portuguese


with open("data_for_damd.json") as fin:
    data = json.load(fin)
    word_count = defaultdict(int)
    nlp = Portuguese()
    tokenizer = nlp.tokenizer
    for did in data:
        for entry in data[did]["log"]:
            for item in entry:
                if item == "turn_num": continue
                for word in tokenizer(entry[item]):
                    word_count[word.text] += 1
    word_count = dict(sorted(word_count.items(), key=lambda item: -item[1]))
    with open("vocab.freq.json", "w") as fout:
        json.dump(word_count, fout, indent=2)

    special_tokens = json.load(open("corrections.json"))
    with open("vocab.word2idx.json", "w") as w2i:
        counter = 0
        outdata = {}
        for (k,v) in special_tokens.items():
            outdata[v] = counter
            counter +=1
        for (k,v) in word_count.items():
            outdata[k] = counter
            counter +=1
        json.dump(outdata, w2i, indent=2)

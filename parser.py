import sys
import string
# import enchant
# d = enchant.Dict("en_US")

def parse(filename):
    index_file = open("parsed.txt", "w")
    punctuation = string.punctuation
    # punctuation = punctuation.replace("/", "")
    replace = str.maketrans(punctuation, " "*len(punctuation))
    for content in read_content(filename):
        docno, data, start, wall_street = None, "", False, False
        for line in content:
            if "DOCNO" in line:
                docno = line.replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
                continue
            if "<TEXT>" in line:
                start = True
            if "<SO>" in line and "WALL STREET JOURNAL" in line:
                wall_street = True
            if start and wall_street:
                data += " " + line

        for tag in ['HL', 'DD', 'SO', 'IN', 'DATELINE', 'TEXT']:
            data = data.replace("<"+tag+">", " ").replace("</"+tag+">", " ")

        data = data.translate(replace).lower()
        data = [x for x in data.split(" ") if len(x) > 0]
        data = [x for x in data if (len(x) > 1 and x[0] not in "0123456789")]
        data = [x for x in data if x.isalpha()]
        # data = [x for x in data if d.check(x)]
        index_file.write(docno + "\n")
        for token in data:
            index_file.write(token + "\n")
        index_file.write("\n")


def read_content(filename):
    content = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if "<DOC>" in line:
                content = []
            elif "</DOC>" in line:
                yield content
            else:
                content.append(line)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        parse(sys.argv[1])
    else:
        print("python3 parser.py some.xml")

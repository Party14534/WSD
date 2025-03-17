import html.parser
import copy
import math
from typing import OrderedDict


class Sentence:
    sentence = ""
    word = ""
    answer = ""


class MyParser(html.parser.HTMLParser):
    values = []

    def handle_starttag(self, tag, attrs):
        if valid_tag(tag):
            if tag == 'answer':
                self.values.append(tag)
                self.values.append(attrs[1][1])
            else:
                self.values.append(tag)

    def handle_endtag(self, tag):
        self.values.append(tag)

    def handle_data(self, data):
        self.values.append(data)


sentences = []
features = OrderedDict()


def valid_tag(tag: str):
    match(tag):
        case 'answer' | 'instance' | 's' | 'head' | 'context':
            return True

    return False


def score_sentence(sentence: str):
    words = sentence.split(" ")
    length = len(words)
    for key, vec in features.items():
        score = 0
        for word in words:
            if word in vec:
                score += 1

        percent = float(score) / float(length)
        print(key)
        print(percent)
        if score != 0:
            print(math.log(percent))
        print('----------------')


filename = r"line-data/line-train.txt"
file = open(filename, 'r')
data = file.read()

parser = MyParser()

parser.feed(data)

sentence = Sentence()
creatingSentence = False
insideHead = False
insideContext = False
insideS = False
insideAnswer = False
for i, tag in enumerate(parser.values):
    if not creatingSentence:
        if tag == 'instance':
            creatingSentence = True
    else:
        match(tag):
            case 'instance':
                creatingSentence = False
                sentences.append(copy.deepcopy(sentence))
                sentence.sentence = ""
                sentence.word = ""
                sentence.answer = ""
            case 'context':
                insideContext = not insideContext
            case 's':
                insideS = not insideS
            case 'head':
                insideHead = not insideHead
                insideS = not insideS
            case 'answer':
                insideAnswer = not insideAnswer
            case _:
                if insideAnswer:
                    sentence.answer = tag
                elif insideS:
                    sentence.sentence += tag
                elif insideHead:
                    sentence.word = tag
                    sentence.sentence += tag

# Now that we have the sentences, create the feature vectors
for sentence in sentences:
    if sentence.answer not in features:
        features[sentence.answer] = {}

    features[sentence.answer]
    words = sentence.sentence.split(" ")
    for word in words:
        features[sentence.answer][word] = True


score_sentence(sentences[0].sentence)

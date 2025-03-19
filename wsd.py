"""
Zachariah Dellimore V00980652

I use the html.parser library which is a built-in html parser in python.
It can default with python for me and it seems to be a default package but
if the program fails to run it may be caused by this package needing to be
installed.

I used the bag of words approach to used log-liklihood to choose the most
likely key.
"""

import html.parser
import copy
import string
import sys
import math
from typing import OrderedDict


# Sentence structure to save important data
class Sentence:
    sentence = ""
    word = ""
    answer = ""


# Parser implementation
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
feature_count = {}
answer_count = {}
num_answers = 0


# Chooses the most likely key from the features
def score_sentence(sentence: str, features: dict):
    words = sentence.split(" ")
    data = ""

    best_key = ""
    best_key_percent = 100.0
    for key, vec in features.items():
        score = 0.0

        # Sum all logs
        # If I don't use log-liklihood my model has an accuracy of 92%
        for word in words:
            if word in vec:
                score += math.log10(vec[word] / feature_count[word])

        # Calculate log-liklihood
        percent = math.log10(answer_count[key] / num_answers) + score

        # Data for model.txt
        data += "Key: " + key + " Percent: " + str(percent) + "\n"

        if percent > best_key_percent or best_key_percent == 100.0:
            best_key = key
            best_key_percent = percent

    data += "Predicted: " + best_key + "\n---\n"
    print(best_key)
    return data


# Iterate through sentences and return the debug data
def test_model(features, sentences):
    data = ""
    for sentence in sentences:
        data += score_sentence(sentence, features)

    return data


# Only care about specific tags
def valid_tag(tag: str):
    match(tag):
        case 'answer' | 'instance' | 's' | 'head' | 'context':
            return True

    return False


def main():
    if len(sys.argv) < 4:
        print("Invalid number of arguments!")
        exit(1)

    # Load file data
    train_filename = sys.argv[1]
    test_filename = sys.argv[2]
    model_filename = sys.argv[3]
    train_file = open(train_filename, 'r')
    test_file = open(test_filename, 'r')
    model_file = open(model_filename, 'w')

    train_data = train_file.read()
    test_data = test_file.read()

    # Parse data
    parser = MyParser()
    parser.feed(train_data)

    # Convert the parser data to sentences
    sentence = Sentence()
    creatingSentence = False
    insideHead = False
    insideContext = False
    insideS = False
    insideAnswer = False
    for tag in parser.values:
        if not creatingSentence:
            if tag == 'instance':
                creatingSentence = True
        else:
            match(tag):
                case 'instance':
                    creatingSentence = False
                    filtered_sentence = sentence.sentence.translate(
                            str.maketrans('', '', string.punctuation))
                    sentence.sentence = filtered_sentence

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
    global num_answers
    num_answers = len(sentences)
    for sentence in sentences:
        if sentence.answer not in features:
            features[sentence.answer] = {}

        if sentence.answer in answer_count:
            answer_count[sentence.answer] += 1
        else:
            answer_count[sentence.answer] = 1

        words = sentence.sentence.split(" ")

        # Update the count for each feature
        for word in words:
            if word in features[sentence.answer]:
                features[sentence.answer][word] += 1
            else:
                features[sentence.answer][word] = 1

            if word in feature_count:
                feature_count[word] += 1
            else:
                feature_count[word] = 1

    # Create test sentences
    test_parser = MyParser()
    test_parser.values = []
    test_parser.feed(test_data)

    # Parse the test data and convert it to sentences
    test_sentences = []
    test_sentence = Sentence()
    test_sentence.sentence = ""
    test_sentence.word = ""
    test_sentence.answer = ""
    for tag in test_parser.values:
        if not creatingSentence:
            if tag == 'instance':
                creatingSentence = True
        else:
            match(tag):
                case 'instance':
                    creatingSentence = False
                    test_sentences.append(copy.deepcopy(test_sentence))
                    test_sentence.sentence = ""
                    test_sentence.word = ""
                    test_sentence.answer = ""
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
                        test_sentence.answer = tag
                    elif insideS:
                        test_sentence.sentence += tag
                    elif insideHead:
                        test_sentence.word = tag
                        test_sentence.sentence += tag

    # Only care about the strings
    test_sentence_data = []
    for sentence in test_sentences:
        test_sentence_data.append(sentence.sentence)

    # Get the debug data from the testing the model
    test_text = test_model(features, test_sentence_data)

    # Finally we serialize the model
    data = ""
    for key, value in features.items():
        data += key + ":"
        for word, _ in value.items():
            data += word + " "

        data += "\n"

    data += "-\n" + test_text

    model_file.write(data)


if __name__ == "__main__":
    main()

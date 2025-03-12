import re


class Sentence:
    sentence = ""
    word = ""
    answer = ""


training_data = []

answer_pattern = r'<answer.*senseid="(.*)"\/>'
answer_substitution = r'\1'

sentence_pattern = r'<s>(.*)<head>(.*)</head>(.*)</s>'
sentence_substitution = r'\1 \2 \3'

word_pattern = r'(\s|\S)*<head>(.*)<\/head>(\s|\S)*'
word_substitution = r'\2'


def load_training_data(filename):
    file = open(filename, 'r')
    data = file.read()

    # Get the sentences and answers
    sentences = []
    data_units = re.findall(r'<answer.*/>\s<context>\s*<s>.*<\/s>\s*<\/context>', data)
    for data_unit in data_units:
        sentence_units = re.findall(r'<s>.*</s>', data_unit)
        sentence_unit = ""
        for s in sentence_units:
            s = re.sub(r'<.*?>', '', s)
            sentence_unit += s

        s = Sentence()

        sentence = re.sub(sentence_pattern, sentence_substitution,
                          sentence_unit)
        s.sentence = sentence

        answer_unit = re.findall(r'<answer.*/>', data_unit)
        answer = re.sub(answer_pattern, answer_substitution, answer_unit[0])
        s.answer = answer

        word = re.sub(word_pattern, word_substitution, data_unit)
        s.word = word

        print(sentence, "\n", answer, "\n", word, "\n----------")

        sentences.append(s)


def main():
    load_training_data(r"line-data/line-train.txt")


if __name__ == "__main__":
    main()

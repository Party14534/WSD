import re


class Sentence:
    words = []
    word_index = -1
    answer = ""


training_data = []

answer_pattern = r'<answer.*senseid="(.*)"/>'
answer_substitution = r'\1'

sentence_pattern = r'<s>(.*)<head>(.*)</head>(.*)</s>'
sentence_substitution = r'\1 \2 \3'


def load_training_data(filename):
    file = open(filename, 'r')
    data = file.read()

    # Get all answers
    answer_units = re.findall(r'<answer.*/>', data)
    answers = []
    for answer_unit in answer_units:
        answer = re.sub(answer_pattern, answer_substitution, answer_unit)
        answers.append(answer)

    # Get the sentences
    sentences = []
    context_units = re.findall(r'<context>(\s*<s>.*<\/s>\s*)<\/context>', data)
    for context_unit in context_units:
        sentence_units = re.findall(r'<s>.*</s>', context_unit)
        sentence_unit = ""
        for s in sentence_units:
            s = re.sub(r'<.*?>', '', s)
            sentence_unit += s

        sentence = re.sub(sentence_pattern, sentence_substitution,
                          sentence_unit)
        sentences.append(sentence)
        print(sentence)


    print(len(sentences))
    print(len(context_units))
    print(len(answers))


def main():
    load_training_data(r"line-data/line-train.txt")


if __name__ == "__main__":
    main()

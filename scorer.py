import sys

from wsd import MyParser

# Exit if there arent enough arguments
if len(sys.argv) < 3:
    print("Invalid number of arguments")
    print(len(sys.argv))
    exit(1)

# Load files
guesses_filename = sys.argv[1]
answers_filename = sys.argv[2]
guess_file = open(guesses_filename, 'r')
answer_file = open(answers_filename, 'r')

guess_data = guess_file.read()
answer_data = answer_file.read()

guesses = guess_data.split('\n')
answers = []

# Parse the answer file to get the answers
answer_parser = MyParser()
answer_parser.feed(answer_data)
for tag in answer_parser.values:
    if tag != 'answer' and tag != '\n':
        answers.append(tag)

# Go through the guesses to see if they're the same as the answers
correct_count = 0
count = len(answers)
for i, guess in enumerate(guesses):
    # The last guess is an empty string
    if guess == '':
        continue
    if guess == answers[i]:
        correct_count += 1

# Calculate the accuracy
accuracy = float(correct_count) / float(count)
print(accuracy * 100)

# Python workshop ex1

import random


def main():
    # Get the file name
    fileNameIn = raw_input("Enter the text file name: ")

    # Build the word list
    words = buildList(fileNameIn)
    if len(words) < 3:
        # can't parse this way since we don't have enough words.
        print "ERROR: Parsing file..."
        return 1

    # Get the markov test
    markovText = buildText(buildDictionary(words), words)

    # Print the results
    print "The results:"
    print "-" * 80
    print markovText
    print "-" * 80
    print ""

    # Get the output file name
    fileNameOut = raw_input(
        "Enter file name to write output to <Enter for skip>: ")

    # Print to the output file if necessary
    if fileNameOut:
        writeFile(fileNameOut, markovText)

    return 0


def buildList(fileName):
    # Open the file for reading
    filePointer = open(fileName, 'r')

    # Read the whole file
    fileData = filePointer.read()

    # Close the file
    filePointer.close()

    # Split the file's text into words
    return fileData.split()


def buildDictionary(listOfWords):
    d = {}
    i = 3

    # Iterate over the words starting from the 3rd word
    for word in listOfWords[2:]:
        # Get the current key
        key = ' '.join(listOfWords[i-3:i-1])

        # Create an empty list if the key does not exist
        if not key in d:
            d[key] = []

        # Append the current word to this key's list
        d[key].append(word)

        # Increment the index
        i += 1

    return d


def buildText(dictionary, listOfWords):
    # Get the initial key and text
    key = listOfWords[0] + ' ' + listOfWords[1]
    text = key

    # We have 2 words when starting
    countWords = 2

    # Keep adding words while we find the key and don't have too many words
    while dictionary.get(key) and countWords < 500:
        # Get a random word associated with this key
        chosenWord = random.choice(dictionary[key])

        # Append the word and get the next key
        text += ' ' + chosenWord
        key = key.split()[1] + ' ' + chosenWord

        # Increment the word count
        countWords += 1

    return text


def writeFile(fileName, markovText):
    # Open the file for writing
    filePointer = open(fileName, 'w')

    # Split the text into words
    listOfWords = markovText.split()
    counterOfChar = 0

    # Add the first word to the chunk buffer
    cutText = listOfWords[0]
    counterOfChar = len(cutText)

    # Iterate over the words starting from the second one
    for word in listOfWords[1:]:
        # Check if we have enough room in the current line
        if counterOfChar + 1 + len(word) <= 80:
            # Append the word to the current line and count its characters
            counterOfChar += 1 + len(word)
            cutText += ' ' + word
        else:
            # Not enough room - write the current line and append
            # the word to the new line, count its characters and
            # clear the buffer
            filePointer.write(cutText + '\n' + word)
            cutText = ''
            counterOfChar = len(word)

    # Write any remaining words in the line buffer (or an empty string)
    filePointer.write(cutText)

    # Close the file
    filePointer.close()

if __name__ == '__main__':
    main()

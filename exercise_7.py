def searching_word(split_words): # Finding the biggest word in the sequence
    max_word = ''
    for item in split_words:
        if len(max_word) <= len(item):
            max_word = item
    return max_word


def correct_input(): # Checking if the user's input consist of 2 apostrophes
    while True:
        try:
            seq_words = eval(input('Give the sequence of words: '))
            break
        except:
            print("\nYour sequence of words should be included between 2 apostrophes")
            print("For example: 'gold black red'\n")
    return seq_words


if __name__ == '__main__':
    seq_words = correct_input()
    split_words = seq_words.split(' ')
    biggest_word = searching_word(split_words)
    # Printing the biggest word of the sequence
    print('\n"'+biggest_word+'"')
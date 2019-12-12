import queue


def build_wordlist(wordlist_file):
    '''Method to set the dictionnary used to fuzz
    directories in a Queue object for multi-threading'''

    #print("Building the word list")
    # read in the word list
    fd = open(wordlist_file, "rb")
    raw_words = fd.readlines()
    fd.close()
    # found_resume = False
    words = queue.Queue()

    for word in raw_words:
        word = word.rstrip()
        words.put(word)
    return words

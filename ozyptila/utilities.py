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


def build_url_q(url_list):
    '''Set the queue for the urls already know of the target
    A string or a list can be given as parameter'''

    # Creating the Queue object
    target_url_queue = queue.Queue()

    # Check if object is a list or not, and convert it to good format
    if isinstance(url_list, str):
        url_list = [url_list]
    elif isinstance(url_list, list):
        pass

    # Fill the queue object with the urls already known
    for url in url_list:
        target_url_queue.put(url)

    # return the queue object containing the urls
    return target_url_queue

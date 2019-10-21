import nltk
from nltk.stem import PorterStemmer


class zipf_data:
    def __init__(self, token=None, freq=None):
        self.token = token
        self.freq = freq


exclusive_token = ['br', '/b', 'nbsp', '>', '<', '&', '.', ')', '(', ':', ',', "'", "''", '$', '%', ';']


def porter_algo(data, flag):
    porter_stemmer = PorterStemmer()
    total_freq = []
    total_word = []
    '''
        iterate each artical
    '''
    for one in data:
        freq = []
        word = []
        '''
            flag == TRUE -> xml data, we manipulate both PubMed title and content
            flag == FALSE -> json data, we only manipulate tweet content.
        '''
        if flag:
            artical = one.title + " " + one.content
        else:
            artical = one.content
        token = nltk.word_tokenize(artical)
        # token = re.split(r'\w+', artical)
        # token = artical.split()
        '''
            tokenize artical.
            calculate each word freq and sort by freq.
        '''
        token = [w.lower() for w in token]
        for index, each in enumerate(token):
            token[index] = porter_stemmer.stem(each)

        words = set(token)
        counts = [(w, token.count(w))
                  for w in words if w not in exclusive_token]
        zipf_dataset = []
        [zipf_dataset.append(zipf_data(w, c)) for (w, c) in counts]
        zipf_dataset.sort(key=lambda x: x.freq, reverse=True)

        i = 0
        for each in zipf_dataset:
            if i < 30:
                freq.append(each.freq)
                word.append(each.token)
                i = i + 1
            else:
                break
        total_freq.append(freq)
        total_word.append(word)

    # print(len(total_freq[0]))
    # print(len(total_word[0]))
    # for i, j in zip(total_word[0], total_freq[0]):
    #     print(i, " : ", j)
    # print(len(total_freq[0]), len(total_word[0]))
    return total_word, total_freq

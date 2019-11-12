import nltk


class zipf_data:
    def __init__(self, token=None, freq=None):
        self.token = token
        self.freq = freq


exclusive_token = ['br', '/b', 'nbsp', '>', '<', '&', '.', ')', '(', ':', ',', "'", "''", '$', '%', ';', '=', '+', "#", "ffff00", "00FFFF", "span", "/span", "style=", "background-color"]


def zipf(data, flag):
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
        token = nltk.word_tokenize(artical.lower())
        # token = re.split(r'\w+', artical)
        # token = artical.split()
        '''
            tokenize artical.
            calculate each word freq and sort by freq.
        '''
        token_lower = [w.lower().strip('-') for w in token]

        words = set(token_lower)
        counts = [(w, token_lower.count(w))
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

    return total_word, total_freq

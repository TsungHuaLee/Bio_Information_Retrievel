import json
import re

data_path = "/home/tsung/CODE/Information-Retrieval/IR_HW/search/data/twitter_data"


class jsondata:
    def __init__(self, user=None, content=None, date = None, urls = None, favorites = None, char_count=None, word_count=None, sentence_count=None, score=None):
        self.user = user
        self.content = content
        self.date = date
        self.urls = urls
        self.favorites = favorites
        self.char_count = char_count
        self.word_count = word_count
        self.sentence_count = sentence_count
        self.score = score


def jsonParser(file_name):
    # return 20 data
    parse_data = []
    cnt = 0
    with open(file_name, 'r', encoding="UTF-8") as inputFile:
        f = open(data_path, "w", encoding='UTF-8')

        json_array = json.load(inputFile)

        for item in json_array:
            user = ""
            content = ""
            date = ""
            urls = ""
            favorites = ""
            char_count = 0
            word_count = 0
            sentence_count = 0
            if 'Username' in item:
                user = item['Username']
            if(len(user) == 0):
                if 'author_id' in item:
                    user = item['author_id']
            if 'text' in item:
                content = item['text']
                # prevent last char did'n work in for loop => elif(k == key_match_idx[j][1]):
                content = content + ' '
            if 'date' in item:
                date = item['date']
            if 'Urls' in item:
                urls = item['Urls']
                if(len(urls) > 0):
                    urls = urls[0]
                else:
                    urls = ""
            if 'favorites' in item:
                favorites = item['favorites']

            char_count = char_count + len(re.split(r'\S', content))
            word_count = word_count + len(re.split(r'\w+', content))
            sentence_count = len(re.split('(?<!\w\.\w.)(?<!\d\d\.)(?<=\.|\?)\s(?!(\d\.){2})', content))

            # error handling for special case
            http_place = content.find("http")
            if(content[http_place-1] != ' '):
                content = content[:http_place] + " " + content[http_place:]

            # find each word
            match_idx = []
            for idx in list(re.finditer(r'\w+', content)):
                match_idx.append((idx.start(), idx.end()))

            # find each hashtag
            key_match_idx = []
            new_str = ""
            key = []
            for idx in re.finditer('# ', content):
                for word in match_idx:
                    temp = word[0]
                    if(idx.start() < temp):
                        key_match_idx.append((word[0], word[1]))
                        key.append(content[word[0]:word[1]])
                        break

            if(len(key_match_idx) > 0):
                j = 0
                # iterate each char
                for k in range(len(content)):
                    if(k == key_match_idx[j][0]):
                        temp = '<a href="https://twitter.com/search?q=%23' + key[j] + '&src=typd">'
                        print(temp)
                        new_str = new_str + temp + content[k]
                    elif(k == key_match_idx[j][1]):
                        new_str = new_str + '</a>' + content[k]
                        j = j + 1
                        if(j == len(key_match_idx)):
                            new_str = new_str + content[k + 1:]
                            break
                    else:
                        new_str = new_str + content[k]
                # add span tag, it also add \n for no reason
                content = new_str.replace('\n', ' ')

                print(content)

            output = '%s\t%s\t%s\t%s\t%d\t%d\t%d\t%d\n' % (
                user, content, date, urls, favorites, char_count, word_count, sentence_count)
            f.write(output)
            parse_data.append(
                jsondata(user, content, date, urls, favorites, char_count, word_count, sentence_count, 0))
            cnt = cnt + 1

        f.close()
    return parse_data, cnt

# jsonParser('/home/tsung/CODE/Information-Retrieval/data/tweet_dengue_ncku.json')

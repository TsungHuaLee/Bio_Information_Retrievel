import json
import re

data_path = "/home/tsung/CODE/Information-Retrieval/IR_HW/search/data/twitter_data"

class jsondata:
    def __init__(self, title=None, content=None, char_count=None, word_count=None, sentence_count=None, score=None):
        self.title = title
        self.content = content
        self.char_count = char_count
        self.word_count = word_count
        self.sentence_count = sentence_count
        self.score = score

def jsonParser(file_name):
    # return 20 data
    parse_data= []
    cnt = 0
    with open(file_name, 'r', encoding="UTF-8") as inputFile:
        f = open(data_path, "w", encoding='UTF-8')

        line = inputFile.readline()
        while line:
            # print(line)
            json_data = json.loads(line)
            if "delete" not in json_data:
                text = json_data['text']
                text = text.replace('\n', ' ')
                text = text.strip()

                user = json_data['user']['name']
                user = user + " @" + json_data['user']['screen_name']
                char_count = len(text)
                regex = r'\w+'
                word_count = len(text.split())
                sentence_count = len(re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', text))
                output = '%s\t%s\t%d\t%d\t%d\n' % (user, text, char_count, word_count, sentence_count)
                f.write(output)
                if(cnt < 20):
                    parse_data.append(jsondata(user, text, char_count, word_count, sentence_count, 0))
                    cnt = cnt+1
            line = inputFile.readline()
        f.close()
    return parse_data, cnt

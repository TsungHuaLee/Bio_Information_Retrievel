import xml.etree.ElementTree as ET
import sys
import re

PATH = "./PubmedArticleSet/PubmedArticle/MedlineCitation/Article"
data_path = "/home/tsung/CODE/Information-Retrieval/IR_HW/search/data/pubmed_data"

class xmldata:
    def __init__(self, title=None, content=None, char_count=None, word_count=None, sentence_count=None, score=None):
        self.title = title
        self.content = content
        self.char_count = char_count
        self.word_count = word_count
        self.sentence_count = sentence_count
        self.score = score

def xmlParser(file_name):
    # return 20 data
    parse_data= []
    cnt = 0

    with open(file_name, "r", encoding='UTF-8') as inputFile:
        # omit first two row
        next(inputFile)
        next(inputFile)
        print("file_name",file_name)
        fileContent = inputFile.read()
        f = open(data_path, "w", encoding='UTF-8')
        # parse multi root xml
        tree = ET.fromstring("<fake>" + fileContent +"</fake>")
        for artical in tree.findall(PATH):
            title = artical.find("ArticleTitle").text
            abstract = artical.find("Abstract")
            abstract = ''.join(abstract.itertext())
            abstract = abstract.replace('\n', ' ')
            # abstract = abstract.replace('                ', '')
            abstract = abstract.strip(' ')


            char_count = len(abstract)
            regex = r'\w+'
            word_count = len(abstract.split())
            sentence_count = len(re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', abstract))
            output = '%s\t%s\t%d\t%d\t%d\n' % (title, abstract, char_count, word_count, sentence_count)
            # print(output)
            f.write(output)
            if(cnt < 20):
                parse_data.append(xmldata(title, abstract, char_count, word_count, sentence_count, 0))
            cnt = cnt+1
        f.close()
    return parse_data, cnt


# def xmlParser(file_name):
#     # return 20 data
#     parse_data= []
#     cnt = 0
#
#
#     tree = ET.parse(file_name)
#     root = tree.getroot()
#
#     f = open(data_path, "w", encoding='UTF-8')
#     for artical in root.findall('./PubmedArticle/MedlineCitation/Article'):
#         title = artical.find('ArticleTitle').text
#         abstract = artical.find("Abstract")
#         abstract = ''.join(abstract.itertext())
#         abstract = abstract.replace('\n', ' ')
#         # abstract = abstract.replace('                ', '')
#         abstract = abstract.strip(' ')
#
#         char_count = len(abstract)
#         regex = r'\w+'
#         word_count = len(abstract.split())
#         sentence_count = len(re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', abstract))
#         output = '%s\t%s\t%d\t%d\t%d\n' % (title, abstract, char_count, word_count, sentence_count)
#         # print(output)
#         f.write(output)
#         if(cnt < 20):
#             parse_data.append(xmldata(title, abstract, char_count, word_count, sentence_count, 0))
#         cnt = cnt+1
#     f.close()
#     return parse_data, cnt

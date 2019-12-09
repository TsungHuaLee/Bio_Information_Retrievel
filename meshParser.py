import xml.etree.ElementTree as ET
import re

PATH = "./DescriptorRecordSet/DescriptorRecord"
data_path = "/home/tsung/CODE/Information-Retrieval/Whole_MESH_keyword.txt"


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
    parse_data = []
    cnt = 0

    with open(file_name, "r", encoding='UTF-8') as inputFile:
        # omit first two row
        next(inputFile)
        next(inputFile)
        fileContent = inputFile.read()
        f = open(data_path, "w", encoding='UTF-8')
        # parse multi root xml
        tree = ET.fromstring("<fake>" + fileContent + "</fake>")
        i = 0
        for artical in tree.findall(PATH):
            i = i + 1
            # keyword = artical.find("ConceptName/String")
            descriptor = artical.find("DescriptorName/String").text
            print(descriptor)
            if(descriptor is None):
                keyword = ''
            else:
                keyword = set()

                for concept in artical.findall('ConceptList/Concept'):
                    # output = keyword + " " + concept.find('ConceptName/String').text
                    for term in concept.findall('TermList/Term'):
                        # keyword = keyword + " " + term.find('String').text
                        # temp = term.find('String').text
                        keyword.add(term.find('String').text)
                        # print(keyword)

            print(keyword)
            output = ""
            for id, val in enumerate(keyword):
                if(id == 0):
                    output = descriptor.lower()+":\t"+val.lower()
                else:
                    output += "\t" + val.lower()
            # keyword.replace('\n', '')
            f.write(output+'\n')

            # if(i > 10):
            #     break
        f.close()
    # return parse_data, cnt

xmlParser("/home/tsung/CODE/Information-Retrieval/desc2020.xml")
# xmlParser("/home/tsung/CODE/Information-Retrieval/temp")

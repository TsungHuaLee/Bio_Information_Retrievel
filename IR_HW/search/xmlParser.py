import xml.etree.ElementTree as ET
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
        for artical in tree.findall(PATH):
            # fetch title
            title = artical.find("ArticleTitle")
            if(title is None):
                title = ''
            else:
                title = ''.join(title.itertext())
                title = title.replace('\n', ' ')
                title = title.replace('\t', ' ')
                title = title.strip(' ')

            # fetch abstract
            abstract = artical.find("Abstract")
            char_count = 0
            word_count = 0
            sentence_count = 0
            if(abstract is None):
                content = ''
            else:
                content = ''
                for abstractText in abstract.findall("AbstractText"):
                    if 'Label' in abstractText.attrib:
                        content = content + '<b>' + abstractText.attrib['Label'] + ':</b><br>&nbsp&nbsp&nbsp&nbsp'
                        temp_text = ''.join(abstractText.itertext())
                        temp_text = temp_text.replace('\n', ' ')
                        temp_text = temp_text.replace('\t', ' ')
                        temp_text = temp_text.strip(' ')
                        content = content + temp_text + ' <br>'
                        # char_count = char_count + len(temp_text)
                        char_count = char_count + len(re.split(r'\S', temp_text))
                        word_count = word_count + len(re.split(r'\w+', content))
                    else:
                        content = ''.join(abstractText.itertext()) + ' <br>'
                        char_count = char_count + len(re.split(r'\S', content))
                        word_count = word_count + \
                            len(re.split(r'\w+', content))

            # show partial data
            match_idx = []
            for idx in list(re.finditer('(?<!\w\.\w.)(?<!\d\d\.)(?<=\.|\?)\s(?!(\d\.){2})', content)):
                match_idx.append((idx.start(), idx.end()))

            sentence_count = len(match_idx)

            new_str = ""
            if(len(match_idx) > 0):
                j = 0
                # iterate each char
                for k in range(len(content)):
                    if(k == match_idx[j][0]):
                        new_str = new_str + \
                            '<span style="background-color:#FFB3FF">' + content[k]
                    elif(k == match_idx[j][1]):
                        new_str = new_str + '&nbsp</span>' + content[k]
                        j = j + 1
                        if(j >= len(match_idx)):
                            new_str = new_str + content[k + 1:]
                            break
                    else:
                        new_str = new_str + content[k]
                # add span tag, it also add \n for no reason
                content = new_str.replace('\n', ' ')

            output = '%s\t%s\t%d\t%d\t%d\n' % (
                title, content, char_count, word_count, sentence_count)

            f.write(output)
            parse_data.append(
                xmldata(title, content, char_count, word_count, sentence_count, 0))
            cnt = cnt + 1
        f.close()
    return parse_data, cnt

# xmlParser("/home/tsung/CODE/Information-Retrieval/data/pubmed_dengue3.xml")

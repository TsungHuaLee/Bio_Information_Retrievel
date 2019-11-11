from sklearn.feature_extraction.text import CountVectorizer
import re
import numpy as np
import math

pubmed_file = "/home/tsung/CODE/Information-Retrieval/IR_HW/search/data/pubmed_data"
data_path = "/home/tsung/CODE/Information-Retrieval/IR_HW/search/data/match_data"

color_table = ["#FFFF00", "#00FFFF"]


class xmldata:
    def __init__(self, title=None, content=None, char_count=None, word_count=None, sentence_count=None, score=None):
        self.title = title
        self.content = content
        self.char_count = char_count
        self.word_count = word_count
        self.sentence_count = sentence_count
        self.score = score


def match_and_insert(match, key, str, score, weight):
    new_str = ""
    match_idx = []

    for idx in list(re.finditer(key, str.lower())):
        match_idx.append((idx.start(), idx.end()))
        score = score + weight
        match = True
    # add font color tag
    if(len(match_idx) > 0):
        j = 0
        # iterate each char
        for i in range(len(str)):
            if(i == match_idx[j][0]):
                new_str = new_str + \
                    '<span style="background-color:#FFFF00">' + str[i]
            elif(i == match_idx[j][1]):
                new_str = new_str + '</span>' + str[i]
                j = j + 1
                if(j >= len(match_idx)):
                    new_str = new_str + str[i + 1:]
                    break
            else:
                new_str = new_str + str[i]
        str = new_str

    return match, str, score


def tf_idf(title, content, total_document, key):
    vectorizer = CountVectorizer()
    # the number of occurrences of a word
    X = vectorizer.fit_transform(title)
    # all bag of words
    word = vectorizer.get_feature_names()
    word = np.asarray(word)

    # calculate tf
    term_freq = []
    for one in X.toarray():
        total_count = np.sum(one)
        idx = np.where(word == key)
        term_count = one[idx[0][0]]
        term_freq.append(term_count/total_count)
    # calculate idf
    inverse_docu_freq = math.log10(total_document/len(title))

    result = []
    for i in term_freq:
        result.append(i*inverse_docu_freq)

    return result


def full_text_match(file_name, key):
    key = key.lower()
    match = False
    match_data = []

    key = key.split(' ')

    match_ori_title = []
    match_ori_content = []

    with open(file_name, "r", encoding='UTF-8') as inputFile:
        line = inputFile.readline()
        i = 0
        while line:
            match = False
            data = line.split('\t')
            i = i + 1
            ori_title = data[0]
            title = data[0]
            ori_content = data[1]
            content = data[1]
            char_count = data[2]
            word_count = data[3]
            sentence_count = data[4].strip()

            if(sentence_count[-1] == '\n'):
                print("error")

            score = 0
            # weight for multiple match
            pre_score = 0
            weight = 0
            # match title
            for each in key:
                match, title, score = match_and_insert(
                    match, each, title, score, 100)
                match, content, score = match_and_insert(
                    match, each, content, score, 10)
                if(score != pre_score):
                    weight = weight + 1
                pre_score = score

            score = score * (10 ** weight)

            # save matching data
            if(match == True):
                match_data.append(
                    xmldata(title, content, char_count, word_count, sentence_count, score))
                match_ori_title.append(ori_title)
                match_ori_content.append(ori_content)
            # read next data
            line = inputFile.readline()

    tf_idf_result = tf_idf(match_ori_title, match_ori_content, i, key)

    for idx, a in enumerate(match_data):
        match_data[idx].score = tf_idf_result[idx]
    # sort all match data
    match_data.sort(key=lambda x: x.score, reverse=True)

    with open(data_path, 'w', encoding='UTF-8') as outputFile:
        for i in match_data:
            output = '%s\t%s\t%s\t%s\t%s\t%d\n' % (
                i.title, i.content, i.char_count, i.word_count, i.sentence_count, i.score)
            outputFile.write(output)

    return match_data

if __name__ == '__main__':
    full_text_match(pubmed_file, "dengue")

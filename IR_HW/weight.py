from sklearn.feature_extraction.text import CountVectorizer
import re
import numpy as np
from numpy import dot
from numpy.linalg import norm

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


# the feature should be N feature vector of article
def similarity(feature):
    top_5_similarity = []
    for i in feature:
        i = np.asarray(i)
        cos_sim = []
        for j in feature:
            j = np.asarray(j)
            cos_sim.append(dot(i, j)/(norm(i)*norm(j)))
        cos_sim = np.array(cos_sim)
        sort_cos_sim = np.argsort(-cos_sim)
        top_5_similarity.append(sort_cos_sim[1:6])
    return top_5_similarity

def tf_idf(title, content, total_document, key, type = 1):
    top_5_similarity = []
    if(type == 1):
        article = []
        for idx, one_title in enumerate(title):
            article.append((one_title + " " + content[idx]).lower())
        vectorizer = CountVectorizer()
        # the number of occurrences of a word
        X = vectorizer.fit_transform(article)
        top_5_similarity = similarity(X.toarray())

        # all bag of words
        word = vectorizer.get_feature_names()
        word = np.asarray(word)

        # the index of query in bag_of_words
        idx_of_word = []
        for i in key:
            idx_of_word.append(np.where(word == i))

        # calculate tf
        # size of term_freq == number of article * number of query word
        term_freq = []
        term_count = []
        # size of docu_freq == number of query word
        docu_freq = [0 for i in range(len(key))]
        for vec in X.toarray():
            each_query_term_count = []
            total_count = np.sum(vec)
            # extract number of occurences of each query word
            for each_query_idx in idx_of_word:
                each_query_term_count.append(vec[each_query_idx[0][0]])
            # accmulate document frequency
            for idx, each in enumerate(each_query_term_count):
                if each == 0:
                    docu_freq[idx] += + 0
                else:
                    docu_freq[idx] += 1
            term_count.append(each_query_term_count)
            each_query_term_count = np.asarray(each_query_term_count)
            term_freq.append(each_query_term_count/total_count)

        # calculate idf
        inverse_docu_freq = [math.log10(total_document/np.array(freq)) for freq in docu_freq]

        inverse_docu_freq = np.asarray(inverse_docu_freq)
        term_freq = np.asarray(term_freq)
        result = term_freq * inverse_docu_freq
    elif(type == 2):
        article = []
        for idx, one_title in enumerate(title):
            article.append((one_title + " " + content[idx]).lower())
        vectorizer = CountVectorizer()
        # the number of occurrences of a word
        X = vectorizer.fit_transform(article)
        top_5_similarity = similarity(X.toarray())
        # all bag of words
        word = vectorizer.get_feature_names()
        word = np.asarray(word)

        # the index of query in bag_of_words
        idx_of_word = []
        for i in key:
            idx_of_word.append(np.where(word == i))

        # calculate tf
        # size of term_freq == number of article * number of query word
        term_freq = []
        term_count = []
        # size of docu_freq == number of query word
        # inverse document frequency smooth, initial = 1
        docu_freq = [1 for i in range(len(key))]
        for vec in X.toarray():
            each_query_term_count = []
            max_count = np.max(vec)
            # extract number of occurences of each query word
            for each_query_idx in idx_of_word:
                each_query_term_count.append(vec[each_query_idx[0][0]])
            # accmulate document frequency
            for idx, each in enumerate(each_query_term_count):
                if each == 0:
                    docu_freq[idx] += + 0
                else:
                    docu_freq[idx] += 1
            term_count.append(each_query_term_count)
            each_query_term_count = np.asarray(each_query_term_count)
            term_freq.append(0.5+0.5*each_query_term_count/max_count)

        # calculate idf
        # inverse document frequency smooth, add one
        inverse_docu_freq = [math.log10(total_document/np.array(freq))+1 for freq in docu_freq]

        inverse_docu_freq = np.asarray(inverse_docu_freq)
        term_freq = np.asarray(term_freq)
        result = term_freq * inverse_docu_freq
    elif(type == 3):
        vectorizer = CountVectorizer()
        # the number of occurrences of a word
        X = vectorizer.fit_transform(title)
        # all bag of words
        word = vectorizer.get_feature_names()
        word = np.asarray(word)

        # the index of query in bag_of_words
        idx_of_word = []
        for i in key:
            idx_of_word.append(np.where(word == i))

        # calculate tf
        # size of term_freq == number of article * number of query word
        term_freq = []
        term_count = []
        # size of docu_freq == number of query word
        # inverse document frequency smooth, initial = 1
        docu_freq = [1 for i in range(len(key))]
        for vec in X.toarray():
            each_query_term_count = []
            max_count = np.max(vec)
            # extract number of occurences of each query word
            for each_query_idx in idx_of_word:
                each_query_term_count.append(vec[each_query_idx[0][0]])
            # accmulate document frequency
            for idx, each in enumerate(each_query_term_count):
                if each == 0:
                    docu_freq[idx] += + 0
                else:
                    docu_freq[idx] += 1
            term_count.append(each_query_term_count)
            each_query_term_count = np.asarray(each_query_term_count)
            term_freq.append(0.5+0.5*each_query_term_count/max_count)

        # calculate idf
        # inverse document frequency smooth, add one
        inverse_docu_freq = [math.log10(total_document/np.array(freq))+1 for freq in docu_freq]

        inverse_docu_freq = np.asarray(inverse_docu_freq)
        term_freq = np.asarray(term_freq)
        title_result = term_freq * inverse_docu_freq

        #######################################################################################
        # the number of occurrences of a word
        X = vectorizer.fit_transform(content)
        top_5_similarity = similarity(X.toarray())
        # all bag of words
        word = vectorizer.get_feature_names()
        word = np.asarray(word)

        # the index of query in bag_of_words
        idx_of_word = []
        for i in key:
            idx_of_word.append(np.where(word == i))

        # calculate tf
        # size of term_freq == number of article * number of query word
        term_freq = []
        term_count = []
        # size of docu_freq == number of query word
        # inverse document frequency smooth, initial = 1
        docu_freq = [1 for i in range(len(key))]
        for vec in X.toarray():
            each_query_term_count = []
            max_count = np.max(vec)
            # extract number of occurences of each query word
            for each_query_idx in idx_of_word:
                each_query_term_count.append(vec[each_query_idx[0][0]])
            # accmulate document frequency
            for idx, each in enumerate(each_query_term_count):
                if each == 0:
                    docu_freq[idx] += + 0
                else:
                    docu_freq[idx] += 1
            term_count.append(each_query_term_count)
            each_query_term_count = np.asarray(each_query_term_count)
            if(max_count != 0):
                term_freq.append(0.5+0.5*each_query_term_count/max_count)
            else:
                term_freq.append(0.5+0.5*each_query_term_count)
        # calculate idf
        # inverse document frequency smooth, add one
        inverse_docu_freq = [math.log10(total_document/np.array(freq))+1 for freq in docu_freq]

        inverse_docu_freq = np.asarray(inverse_docu_freq)
        term_freq = np.asarray(term_freq)
        content_result = term_freq * inverse_docu_freq
        result = title_result + content_result
    return result, top_5_similarity


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
            if(match):
                match_data.append(
                    xmldata(title, content, char_count, word_count, sentence_count, score))
                match_ori_title.append(ori_title)
                match_ori_content.append(ori_content)
            # read next data
            line = inputFile.readline()

    tf_idf_result, top_5_similarity = tf_idf(match_ori_title, match_ori_content, i, key, 3)

    top_5_similarity_title = []
    for idx, each in enumerate(top_5_similarity):
        temp = []
        for jdx, titleIdx in enumerate(each):
            temp.append(match_ori_title[titleIdx])
        top_5_similarity_title.append(temp)

    for idx, a in enumerate(match_data):
        match_data[idx].score = round( np.sum(tf_idf_result[idx]), 5)
        match_data[idx].top_5_similarity = top_5_similarity_title[idx]
    # sort all match data
    match_data.sort(key=lambda x: x.score, reverse=True)

    with open(data_path, 'w', encoding='UTF-8') as outputFile:
        for i in match_data:
            output = '%s\t%s\t%s\t%s\t%s\t%d\n' % (
                i.title, i.content, i.char_count, i.word_count, i.sentence_count, i.score)
            outputFile.write(output)

    return match_data

if __name__ == '__main__':
    full_text_match(pubmed_file, "dengue fever")

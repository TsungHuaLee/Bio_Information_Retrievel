#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 14:43:24 2019

@author: alvinhuang
"""

import re
import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import PorterStemmer
import xml.etree.cElementTree as ET
from collections import Counter
# import matplotlib.pyplot as plt
# import matplotlib as mpl
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import numpy as np
import json

PATH = "./PubmedArticleSet/PubmedArticle/MedlineCitation"

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
    pmid = []
    with open(file_name, "r", encoding='UTF-8') as inputFile:
        # omit first two row
        next(inputFile)
        next(inputFile)
        fileContent = inputFile.read()
        # parse multi root xml
        tree = ET.fromstring("<fake>" + fileContent + "</fake>")
        for artical in tree.findall(PATH):
            # fetch title
            title = artical.find("Article/ArticleTitle")
            concate_pmid = artical.find('PMID').text
            # print(concate_pmid)
            pmid.append(concate_pmid)

            if(title is None):
                title = ''
            else:
                title = ''.join(title.itertext())
                title = title.replace('\n', ' ')
                title = title.replace('\t', ' ')
                title = title.strip(' ')

            # fetch abstract
            abstract = artical.find("Article/Abstract")
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

            '''
                some string have '\n', which will cause error
            '''
            content = content.replace('\n', ' ')
            output = '%s\t%s\t%d\t%d\t%d\n' % (
                title, content, char_count, word_count, sentence_count)

            parse_data.append(
                xmldata(title, content, char_count, word_count, sentence_count, 0))
            cnt = cnt + 1
    return pmid, parse_data

# xmlParser("/home/tsung/CODE/Information-Retrieval/data/pubmed_dengue3.xml")



def download_data_from_pubmed(keyword='fever', numbers=100, filename='example'):
    # keyword = 'african swine fever'
    # numbers = 1
    query_artical_id_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    query_artical_id_content = {'db': 'pubmed',
                                'term': str(keyword),
                                'reldate': '120',
                                'datetype': 'edat',
                                'retmax': str(numbers),
                                'usehistory': 'title',
                                'field': 'title'}
    id_xml_string = requests.post(query_artical_id_url, data=query_artical_id_content).text
    root = ET.fromstring(id_xml_string)

    id_list = []
    for ids in root.iter('Id'):
        id_list.append(ids.text)

    query_artical_abstract_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    query_artical_abstract_content = {'db': 'pubmed',
                                      'id': str(id_list),
                                      'retmode': 'xml'}
    abstract_string = requests.post(query_artical_abstract_url, data=query_artical_abstract_content).text.encode()
    # filename='pubmed_cancer_100.xml'
    f = open(filename, 'wb')
    f.write(abstract_string)
    f.close()
    # parse_xml_abstract_title(abstract_string)
    # print(abstract_string)
    return filename


def parse_xml_abstract_title(filename):
    # abstract_root = ET.fromstring(abstract_string)
    print('filename:' + filename)
    # filename='que.xml'
    tree = ET.parse(str(filename))
    abstract_root = tree.getroot()
    article_title = []
    article_content = []
    pmid = []
    count = 0
    for i in range(0, len(abstract_root.findall('./PubmedArticle'))):
        # print(i)
        # 先檢查有沒有abstract 沒有就跳出來
        if (len(abstract_root.findall('./PubmedArticle')[i].findall('./MedlineCitation/Article/Abstract')) == 0):
            # print("number "+str(i)+"artical not find abstract~")
            count = count + 1
            # print('\n')
        else:
            # print("find abstract~")
            abstract_title_element = abstract_root.findall('./PubmedArticle')[i].findall(
                './MedlineCitation/Article/ArticleTitle')
            concate_pmid = abstract_root.findall('./PubmedArticle')[i].find(
                './MedlineCitation/PMID').text
            # print(concate_pmid)
            pmid.append(concate_pmid)
            concat_title = ''
            for text in abstract_title_element[0].itertext():
                concat_title = concat_title + ' ' + text.replace('\n', " ")
                # print(text)
            # print(abstract_root.findall('./PubmedArticle')[i].findall('./MedlineCitation/Article/ArticleTitle')[0].text)
            concat_title.replace('\n', " ")
            article_title.append(concat_title)
            # print(concat_title)
            abstract_text_element = abstract_root.findall('./PubmedArticle')[i].findall(
                './MedlineCitation/Article/Abstract/AbstractText')
            if (len(abstract_text_element) > 1):
                # 多段要接成一段
                concat_to_one_passage = ''
                for j in range(0, len(abstract_text_element)):
                    for text in abstract_text_element[j].itertext():
                        concat_to_one_passage = concat_to_one_passage + ' ' + str(text)
                concat_to_one_passage.replace('\n', ' ')
                article_content.append(concat_to_one_passage.encode("UTF-8").decode("utf-8") )
                # print(concat_to_one_passage)
                # print('\n')
            else:
                concat = ''
                for text in abstract_text_element[0].itertext():
                    concat = concat + ' ' + text
                article_content.append(concat.encode("UTF-8").decode("utf-8") )
                # print(abstract_text_element[0].text)
                # print('\n')

    # print("有 " + str(count) + " 篇沒有摘要喔!")

    return pmid, article_title, article_content


def load_pubmed_from_file(path):
    f = open(path, 'r', encoding="utf-8")
    abstract_string = f.read()
    return abstract_string
    # parse_xml_abstract_title(abstract_string)


# print(type(f.read()))

def count_character(input_string):
    input_string = input_string.replace(' ','')
    return len(input_string)

def wordset_by_poter(input_string):
    ps = PorterStemmer()
    input_string = re.sub("[^A-Za-z]", " ", input_string.strip())
    wordlist_before_poter = input_string.split()
    wordlist_by_poter = []
    for w in wordlist_before_poter:
        wordlist_by_poter.append(ps.stem(w))
    wordset_by_poter_counter = Counter(wordlist_by_poter)
    #print(wordset_by_poter_counter)
    #wordcount = sum(wordset.values())
    return wordset_by_poter_counter


def count_words(input_string):
    input_string = re.sub("[^A-Za-z]", " ", input_string.strip())
    wordset = Counter(input_string.split())
    wordcount = sum(wordset.values())
    #print(wordset)
    #print(wordcount)
    return wordset,wordcount


def zipf_picture_data(wordset,length = 30):
    worset_sort = wordset.most_common()
    x = []
    y = []
    for i in range(0, len(worset_sort)):
        x.append(worset_sort[i][0])
        y.append(worset_sort[i][1])

    if (len(x) > length):
        length = length
    else:
        length = len(x)

    return x[0:length],y[0:length]

def located_keyword(keyword, searched_string):
    keyword = keyword.lower()
    searched_string = searched_string.lower()
    located = []
    for m in re.finditer(keyword, searched_string):
        located.append(list(m.span()))
    # print(located)

    if len(located) == 0:
        return False, located
    else:
        return True, located


def count_sentence2(artical):
    # with model in nltk
    return len(sent_tokenize(artical))

def count_sentence(artical):
    # with model in nltk
    regex=r'([A-Z][a-z].*?[.:!?](?=$| [A-Z]))'
    #pattern = re.compile(r'([A-Z][a-z].*?[.:!?](?=$| [A-Z]))')
    match=re.findall(regex, artical)
    #match = pattern.match(artical)
    return len(match)


def count_words_v2(artical):
    # this will count a period
    print(word_tokenize(artical))


def load_from_file():
    path = input("輸入檔案路徑:")
    keyword = input("請輸入想找的關鍵字:")
    # xml=load_pubmed_from_file(path)
    title, content = parse_xml_abstract_title(path)

    print('檔案中一共有 ' + str(len(title)) + ' 篇含有內文以及標題的文章')
    count = 1
    for i in range(0, len(title)):
        status_title, located_title = located_keyword(keyword, title[i])
        status_content, located_content = located_keyword(keyword, content[i])
        # print('關鍵字是否存在於標題中:'+ str(status))
        # print('關鍵字是否存在於摘要中:'+ str(status))

        if status_title == True or status_content == True:
            print('這是第 ' + str(count) + ' 篇含有關鍵字的文章')
            count = count + 1

            for j in range(0, len(located_title)):
                print('關鍵字存在於標題中的第:' + str(located_title[j]) + '個字元之間')
            for j in range(0, len(located_content)):
                print('關鍵字存在於摘要中的第:' + str(located_content[j]) + '個字元之間')
            print('標題:' + title[i])
            print('摘要:' + content[i])
            print('這篇的摘要有 ' + str(count_character(content[i])) + ' 個字元')
            print('這篇的摘要有 ' + str(count_words(content[i])) + ' 個詞')
            print('這篇的摘要有 ' + str(count_sentence(content[i])) + ' 個句子')


def load_from_api():
    file_cnt = 0
    size_cnt = 0
    output_name = './subdata/subdata'
    limit = 1<<20
    all_keyword = []
    indexMap = {}
    fout = open(output_name+str(file_cnt), 'w')

    with open("MESH_keyword.txt", "r") as fp:
        line = fp.readline()
        while line:
            synonym = line.split("\t")
            keywordList = []
            for keyword in synonym[1:]:
                keyword = keyword.strip("\n")
                # index: keyword to file
                indexMap[keyword] = (file_cnt, len(all_keyword))
                print("\nlen:", len(all_keyword))
                # synonym array
                keywordList.append(np.array(keyword))
                # crawler
                xml_filename = download_data_from_pubmed(keyword, 5, "temp1")
                pmid, data = xmlParser(xml_filename)
                print("keyword: {}, {}".format(keyword, pmid))
                # write to file
                for one in data:
                    one.content = one.content.replace('\n', ' ')
                    temp = '%s\t%s\t%d\t%d\t%d\n' % (
                        one.title, one.content, one.char_count, one.word_count, one.sentence_count)
                    fout.write(temp)
                    size_cnt = size_cnt + one.char_count

            all_keyword.append(np.array(keywordList))
            if(size_cnt > limit):
                size_cnt = 0
                file_cnt += 1
                fout.close()
                fout = open(output_name+str(file_cnt), 'w')
                print(file_cnt)

            line = fp.readline()
        fout.close()

    all_keyword = np.array(all_keyword)
    np.save("synonym", all_keyword)

    for key in indexMap:
        print(key, " -> ", indexMap[key])

    with open('indexMap.txt', 'w') as file:
        file.write(json.dumps(indexMap))

    # for i in all_keyword:
    #     print(i)

        #         try:
        #             connection = mysql.connector.connect(host='localhost',
        #                                                 database='mesh',
        #                                                 user='root',
        #                                                 password='lee1271232')
        #             for id, ti, co in zip(pmid, title, content):
        #                 mySql_insert_query = 'INSERT INTO pubmed (id, title, content) VALUES ({0}, "{1}", "{2}");'.format(id, ti, co)
        #                 print(mySql_insert_query)
        #                 cursor = connection.cursor()
        #                 cursor.execute(mySql_insert_query)
        #                 connection.commit()
        #                 print(cursor.rowcount, "Record inserted successfully into Laptop table")
        #                 cursor.close()
        #
        #         except mysql.connector.Error as error:
        #             print("Failed to insert record into Laptop table {}".format(error))
        #
        #         try:
        #             connection1 = mysql.connector.connect(host='localhost',
        #                                                 database='mesh',
        #                                                 user='root',
        #                                                 password='lee1271232')
        #             for art_id in pmid:
        #                 mySql_insert_query = "SELECT * FROM pubmed WHERE id = {}".format(art_id)
        #                 cursor = connection1.cursor()
        #                 cursor.execute(mySql_insert_query)
        #                 f = cursor.fetchall()
        #                 if len(f) == 0:
        #                     continue
        #                 mySql_insert_query = "INSERT INTO keywordMap (article_id, keyword) VALUES ({}, '{}');".format(art_id, keyword)
        #                 print(mySql_insert_query)
        #                 cursor = connection1.cursor()
        #                 cursor.execute(mySql_insert_query)
        #                 connection1.commit()
        #                 print(cursor.rowcount, "Record inserted successfully into Laptop table")
        #                 cursor.close()
        #         except mysql.connector.Error as error:
        #             print("Failed to insert record into Laptop table {}".format(error))
        #
        #     line = fp.readline()
        #
        # connection.close()
        # connection1.close()

load_from_api()

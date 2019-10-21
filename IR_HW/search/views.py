from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .xmlParser import xmlParser
from .jsonParser import jsonParser
from .full_text_match import full_text_match
from .tweet_full_text_match import tweet_full_text_match
from .zipf_law import zipf
from .porter_stemer import porter_algo
import os
totol_num = 0

filetype = 'xml'


class xmldata:
    def __init__(self, title=None, content=None, char_count=None, word_count=None, sentence_count=None, score=None, word = None,
                freq = None, porter_word = None, porter_freq = None, index = None, porter_index = None):
        self.title = title
        self.content = content
        self.char_count = char_count
        self.word_count = word_count
        self.sentence_count = sentence_count
        self.score = score
        self.word = word
        self.freq = freq
        self.porter_word = porter_word
        self.porter_freq = porter_freq
        self.index = index
        self.porter_index = porter_index


class jsondata:
    def __init__(self, user=None, content=None, date=None, urls=None, favorites=None, char_count=None, word_count=None, sentence_count=None, score=None, word = None,
                freq = None, porter_word = None, porter_freq = None, index = None, porter_index = None):
        self.user = user
        self.content = content
        self.date = date
        self.urls = urls
        self.favorites = favorites
        self.char_count = char_count
        self.word_count = word_count
        self.sentence_count = sentence_count
        self.score = score
        self.word = word
        self.freq = freq
        self.porter_word = porter_word
        self.porter_freq = porter_freq
        self.index = index
        self.porter_index = porter_index

# Create your views here.


def index(request):
    return render(request, 'search/index.html', locals())


def search(request):
    global filetype
    if request.method == 'GET':
        key = request.GET.get('search')

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = BASE_DIR + '/search/data/pubmed_data'

        data = full_text_match(full_path, key)
        word_in_articals, freq_in_articals = zipf(data, True)
        porter_word_in_articals, porter_freq_in_articals = porter_algo(data, True)
        for index, i in enumerate(data):
            data[index].word = word_in_articals[index]
            data[index].freq = freq_in_articals[index]
            data[index].porter_word = porter_word_in_articals[index]
            data[index].porter_freq = porter_freq_in_articals[index]
            data[index].index = index
            data[index].porter_index = "porter"+str(index)

    return render(request, 'search/index.html', locals())


def upload_file(request):
    global filetype
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(BASE_DIR, uploaded_file_url)

        # return first page data & total num data
        if(uploaded_file_url[-3:] == "xml"):
            data, total_num = xmlParser(full_path)
            word_in_articals, freq_in_articals = zipf(data, True)
            porter_word_in_articals, porter_freq_in_articals = porter_algo(data, True)
            for index, i in enumerate(data):
                data[index].word = word_in_articals[index]
                data[index].freq = freq_in_articals[index]
                data[index].porter_word = porter_word_in_articals[index]
                data[index].porter_freq = porter_freq_in_articals[index]
                data[index].index = index
                data[index].porter_index = "porter"+str(index)
        else:
            data = xmldata("ERROR FILE TYPE",
                           "Checking the file type is xml", 0, 0, 0, 0, [], [], [], [], [], [])
    return render(request, 'search/index.html', locals())


def twitter(request):
    return render(request, 'search/twitter.html', locals())


def tweetupload_file(request):
    global filetype
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(BASE_DIR, uploaded_file_url)

        # return first page data & total num data
        if(uploaded_file_url[-4:] == "json"):
            data, total_num = jsonParser(full_path)
            word_in_articals, freq_in_articals = zipf(data, False)
            porter_word_in_articals, porter_freq_in_articals = porter_algo(data, False)
            for index, i in enumerate(data):
                data[index].word = word_in_articals[index]
                data[index].freq = freq_in_articals[index]
                data[index].porter_word = porter_word_in_articals[index]
                data[index].porter_freq = porter_freq_in_articals[index]
                data[index].index = index
                data[index].porter_index = "porter"+str(index)
        else:
            data = jsondata(
                "ERROR FILE TYPE", "Checking the file type is json", "", "", 0, 0, 0, 0, 0, [], [], [], [], [], [])

    return render(request, 'search/twitter.html', locals())


def tweetsearch(request):
    if request.method == 'GET':
        key = request.GET.get('tweetsearch')

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = BASE_DIR + '/search/data/twitter_data'

        # print(key)
        data = tweet_full_text_match(full_path, key)
        word_in_articals, freq_in_articals = zipf(data, False)
        porter_word_in_articals, porter_freq_in_articals = porter_algo(data, False)
        for index, i in enumerate(data):
            data[index].word = word_in_articals[index]
            data[index].freq = freq_in_articals[index]
            data[index].porter_word = porter_word_in_articals[index]
            data[index].porter_freq = porter_freq_in_articals[index]
            data[index].index = index
            data[index].porter_index = "porter"+str(index)
    return render(request, 'search/twitter.html', locals())

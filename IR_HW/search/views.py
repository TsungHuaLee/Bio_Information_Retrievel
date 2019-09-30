from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .xmlParser import xmlParser
from .full_text_match import full_text_match
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
import os

class xmldata:
    def __init__(self, title=None, content=None, char_count=None, word_count=None, sentence_count=None, score=None):
        self.title = title
        self.content = content
        self.char_count = char_count
        self.word_count = word_count
        self.sentence_count = sentence_count
        self.score = score

totol_num = 0

# Create your views here.
def index(request):
    return render(request, 'search/index.html', locals())


def search(request):
    if request.method == 'GET':
        key = request.GET.get('search')

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = BASE_DIR + '/search/data/pubmed_data'
        data = full_text_match(full_path, key)
        print(data)
    return render(request, 'search/index.html', locals())


def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(BASE_DIR, uploaded_file_url)

        # return first page data & total num data
        data, total_num = xmlParser(full_path)
    return render(request, 'search/index.html', locals())

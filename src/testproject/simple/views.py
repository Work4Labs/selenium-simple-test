# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader


def index(request):
    t = loader.get_template('index.html')
    c = Context({'title': 'The Page Title'})
    return HttpResponse(t.render(c))


def begin(request):
    t = loader.get_template('index.html')
    c = Context({'title': 'The Next Page'})
    return HttpResponse(t.render(c))


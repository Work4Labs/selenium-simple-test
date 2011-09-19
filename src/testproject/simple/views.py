from django.shortcuts import render_to_response


def index(request):
    return render_to_response('index.html', {'title': 'The Page Title'})


def begin(request):
    return render_to_response('begin.html', {'title': 'The Next Page'})


def longscroll(request):
    return render_to_response('longscroll.html', {'title': 'Long Scroll Page'})
    

def nojs(request):
    return render_to_response('nojs.html', {'title': 'No JavaScript Test'})


def html5(request):
    return render_to_response('html5.html')

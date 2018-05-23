from django.shortcuts import render, HttpResponse


def index(request):
    return HttpResponse("<br><p>&nbsp;&nbsp;&nbsp;&nbsp;To test Login and Registration please click <a href='/login'>HERE!</a></p>")

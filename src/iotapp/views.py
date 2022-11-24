from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, this is initial page of swe573 DJango Project!")
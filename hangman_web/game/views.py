from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    # TODO: Add hard mode (with symbols)
    return render(request, 'game/index.html')

def deduct(request):
    context = {
        "life": 7
    }
    return render(request, 'game/life.html', context)

def play(request):
    body = request.POST
    word_size = int(int(body['word-size'])/100*21 + 2)
    print(word_size)
    word = ""
    for i in range(word_size):
        word += "_ "
    word.rstrip(" ")
    # TODO: Select random word
    context = {
        "lifes": 10,
        "word": word,
    }
    return render(request, 'game/play.html', context)

def update(request):
    # TODO: Return invalid form if input is not a single letter
    # TODO: Change input to upper case
    # TODO: If life reaches 0 and word is not complete, return GAME OVER
    print(request.POST)
    body = request.POST
    context = {
        "lifes": int(body['remaining-lifes'])-1,
    }
    return render(request, 'game/play.html', context)
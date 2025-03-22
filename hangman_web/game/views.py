from django.shortcuts import render
import pandas as pd # TODO: reduce imports
import random
from cryptography.fernet import Fernet

# Create your views here.

def index(request):
    # TODO: Add hard mode (with symbols)
    return render(request, 'game/index.html')

def play(request):
    body = request.POST
    word_size = int(int(body['word-size'])/100*21 + 2)
    word = ""
    for i in range(word_size):
        word += "_ "
    word.rstrip(" ")
    random_word = select_random_word(word_size)
    encrypted_word = encrypt_word(random_word)
    context = {
        "lifes": 10,
        "word": word,
        "letters": [chr(i) for i in range(65,91)],
        "key": encrypted_word,
    }
    return render(request, 'game/play.html', context)

def update(request):
    # TODO: Return invalid form if input is not a single letter
    # TODO: Change input to upper case
    body = request.POST
    word = decrypt_word(body['key'])

    # TODO: If life reaches 0 and word is not complete, return GAME OVER
    if int(body['remaining-lifes']) == 1:
        return render(request, 'game/game-over.html')

    available_letters = []
    context = {
        "lifes": int(body['remaining-lifes'])-1,
        "word": "_ _",
        "letters": available_letters,
    }
    return render(request, 'game/play.html', context)

def select_random_word(word_size: int) -> str:
    df = pd.read_csv('game/data/game_ready.csv')
    df = df.drop(df[df["has_symbol"]==True].index)
    df = df.drop(df[df["letters"]!=word_size].index)
    df = df.reset_index(drop=True)
    rows = df.shape[0]
    random_index = random.randint(0, rows-1)
    return df.iloc[random_index]["word"]

def encrypt_word(word: str) -> str:
    # TODO: Remove key from source code
    key = "LY0oni1bidvtwk_eap8YjRb26MUCYD2e24XhLKR8z6I="
    cipher = Fernet(key)
    # Encrypt a word
    encrypted_word = cipher.encrypt(word.encode())
    return encrypted_word.decode()

def decrypt_word(encrypted_word: str) -> str:
    key = "LY0oni1bidvtwk_eap8YjRb26MUCYD2e24XhLKR8z6I="
    cipher = Fernet(key)
    decrypted_word = cipher.decrypt(encrypted_word.encode()).decode()
    return decrypted_word
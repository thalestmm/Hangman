from django.shortcuts import render
import pandas as pd # TODO: reduce imports
import random
from cryptography.fernet import Fernet
import yaml

with open('game/data/config.yaml', 'r') as stream:
    data = yaml.safe_load(stream)

# Create your views here.

def index(request):
    # TODO: Add hard mode (with symbols)
    return render(request, 'game/index.html')

def play(request):
    body = request.POST
    word_size = int(int(body['word-size'])/100*21 + 2)
    text = ""
    for i in range(word_size):
        text += "_ "
    text.rstrip(" ")
    random_word = select_random_word(word_size)
    encrypted_word = encrypt_word(random_word)
    context = {
        "lives": data['starting_lives'],
        "word_placeholder": text,
        "letters": [chr(i) for i in range(65,91)],
        "key": encrypted_word,
    }
    return render(request, 'game/play.html', context)

def update(request):
    body = request.POST
    old_letters = [item for item in list(body['available-letters']) if item not in ("'", ",", " ", "[", "]")]
    word = decrypt_word(body['key'])

    letter_input = body['letter-input'].upper()
    if letter_input not in old_letters:
        # TODO: Make this page
        context = {
            "lives": int(body['remaining-lives']),
            "word_placeholder": body['word-placeholder'],
            "letters": old_letters,
            "key": body['key'],
        }
        return render(request, 'game/invalid-input.html', context)

    old_letters.remove(letter_input)
    used_letters = [item for item in [chr(i) for i in range(65,91)] if item not in old_letters]

    word_list = [letter for letter in word]
    present_list = ["_" if letter not in used_letters else letter for letter in word_list]

    if word_list == present_list:
        # TODO: Make this page
        return render(request, 'game/celebration.html')

    # TODO: If life reaches 0 and word is not complete, return GAME OVER
    if int(body['remaining-lives']) == 1:
        context = {
            "word": word,
        }
        return render(request, 'game/game-over.html', context)

    text = ""
    for i in present_list:
        text += i + " "
    text.rstrip(" ")
    if text == body['word-placeholder']:
        remaining_lives = int(body['remaining-lives']) - 1
    else:
        remaining_lives = int(body['remaining-lives'])
    available_letters = old_letters
    context = {
        "lives": remaining_lives,
        "word_placeholder": text,
        "letters": available_letters,
        "key": body['key'],
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
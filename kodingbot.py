import os
import json
import nltk
from nltk.chat.util import Chat, reflections
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

cwd = os.getcwd()
nltk_data = os.path.join(cwd, "nltk_data")
nltk.data.path.append(nltk_data)

reflections = []
with open('reflections.json', 'r') as file:
    pairs = json.load(file)

pairs = []
with open('pairs.json', 'r') as file:
    pairs = json.load(file)


def clean(str):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    str_clean = stemmer.stem(str) 
    return str_clean
    

def converse():
    chat = Chat(pairs, reflections)
    chat.converse()


def ask(str):
    chat = Chat(pairs, reflections)
    response = chat.respond(str)
    return response



if __name__ == "__main__":
    converse()




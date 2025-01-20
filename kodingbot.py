import os
from os.path import dirname, join
import json
import nltk
from nltk.chat.util import Chat, reflections
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

nltk_data_path = join(dirname(__file__), "nltk_data")
nltk.data.path.append(nltk_data_path)

reflections_path = join(dirname(__file__), "reflections.json")
reflections = []
with open(reflections_path, 'r') as file:
    pairs = json.load(file)

pairs_path = join(dirname(__file__), "pairs.json")
pairs = []
with open(pairs_path, 'r') as file:
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




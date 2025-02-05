import json
import os
from os.path import dirname, join
import random
import re
import sys
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

intent_patterns = []
intent_answers = []
intent_images = []
intent_helps = []

def get_cwd():
    if (__file__):
        root = dirname(__file__) 
    else:
        root = os.getcwd()
    return root

def get_absolute_path(cwd, file_path):
    absolute_path = ""
    if (sys.platform.startswith("win")):
        absolute_path = file_path.replace("/", "\\")
    else:
        absolute_path = file_path.replace("\\", "/")
    absolute_path = join(cwd, absolute_path)
    return absolute_path

def read_intent(file_path):
    intent = []
    with open(file_path, 'r') as file:
        intent = json.load(file)
    return intent

def read_intent_patterns(file_path):
    intent = []
    with open(file_path, 'r') as file:
        data = file.read()
        data = data.replace("\\", "\\\\")
        intent = json.loads(data)
    return intent

def get_match_intents(keyword, intent_patterns):
    match_intents = set()
    for item in intent_patterns:
        for pattern in item["patterns"]:
            match = re.match(pattern, keyword)
            if match:
                match_intents.add(item["intent"])
                break
    return match_intents

def get_match_results(match_intents, intent_answers, intent_images, intent_helps):
    results = []
    cwd = get_cwd()
    for match_intent in match_intents:
        match = {}
        match["intent"] = match_intent
        
        for item in intent_answers:
            if (item["intent"] == match_intent):
                match["answers"] = random.choice(item["answers"])

        for item in intent_images:
            if (item["intent"] == match_intent):
                match["images"] = [get_absolute_path(cwd, image) for image in item["images"]]    

        match_help = intent_helps.get(match_intent)
        if match_help:
            match["help"] = get_absolute_path(cwd, match_help)

        results.append(match)
    return results

def stem(str):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    str_clean = stemmer.stem(str) 
    return str_clean

def init():
    cwd = get_cwd()
    global intent_patterns, intent_answers, intent_images, intent_helps
    if not intent_patterns:
        intent_patterns = read_intent_patterns(get_absolute_path(cwd,"intent_patterns.json"))
    if not intent_answers:
        intent_answers = read_intent(get_absolute_path(cwd, "intent_answers.json"))
    if not intent_images:
        intent_images = read_intent(get_absolute_path(cwd, "intent_images.json"))
    if not intent_helps:
        intent_helps = read_intent(get_absolute_path(cwd, "intent_helps.json"))


def chat(keyword):
    init()
    keyword = stem(keyword)
    match_intents = get_match_intents(keyword, intent_patterns)
    match_results = get_match_results(match_intents, intent_answers, intent_images, intent_helps)
    return match_results

if __name__ == "__main__":
    init()

import json
import os
from os.path import dirname, join
import random
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

intent_patterns = []
intent_answers = []
intent_images = []
intent_helps = []


def get_file_path(file_name):
    cwd = os.getcwd()
    file_path = join(cwd, file_name)
    return file_path

def read_intent(file_name):
    intent = []
    file_path = get_file_path(file_name)
    with open(file_path, 'r') as file:
        intent = json.load(file)
    return intent

def read_intent_patterns(file_name):
    intent = []
    file_path = get_file_path(file_name)
    with open(file_path, 'r') as file:
        data = file.read()
        data = data.replace("\\", "\\\\")
        intent = json.loads(data)
    return intent

def get_match_intents(keyword, intent_patterns):
    match_intents = set()
    for intent, patterns in intent_patterns:
        for pattern in patterns:
            match = re.match(pattern, keyword)
            if match:
                match_intents.add(intent)
                break
    return match_intents


def get_match_results(match_intents, intent_answers, intent_images, intent_helps):
    results = []
    for match_intent in match_intents:
        match = {}
        match["intent"] = match_intent
        
        for intent, answers in intent_answers:
            if (intent == match_intent):
                match["answers"] = random.choice(answers)

        for intent, images in intent_images:
            if (intent == match_intent):
                match["images"] = images    

        match_help = intent_helps.get(match_intent)
        if match_help:
            match["help"] = match_help

        results.append(match)
    return results

def stem(str):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    str_clean = stemmer.stem(str) 
    return str_clean

def init():
    global intent_patterns, intent_answers, intent_images, intent_helps
    if not intent_patterns:
        intent_patterns = read_intent_patterns("intent_patterns.json")
    if not intent_answers:
        intent_answers = read_intent("intent_answers.json")
    if not intent_images:
        intent_images = read_intent("intent_images.json")
    if not intent_helps:
        intent_helps = read_intent("intent_helps.json")


def chat(keyword):
    init()
    keyword = stem(keyword)
    match_intents = get_match_intents(keyword, intent_patterns)
    match_results = get_match_results(match_intents, intent_answers, intent_images, intent_helps)
    return match_results

if __name__ == "__main__":
    init()

import json


class Config:
    SECRET_KEY = '76992bcc9c44cd541fedda87e2233119c82ca9378a7afe3e661d0023b8e20d5b'


def load_parameters():
    with open('modelmodule/ressources/nlpparams.json', 'r') as file:
        nlp_params = json.load(file)
    return nlp_params


class NlpParameters:
    def __init__(self, locale='en'):
        self.locale = locale
        self.tokenizer = load_parameters()['tokenizer']
        self.stop_words = load_parameters()['stop_words'][self.locale]
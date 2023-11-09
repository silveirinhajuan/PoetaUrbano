from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from dataset import dataset
from spacy.cli import download

download("pt_core_news_sm")

class ENGSM:
    ISO_639_1 = "pt_core_news_sm"


chatbot = ChatBot("Poeta Urbano", tagger_language=ENGSM)


def responda(texto):
    return chatbot.get_response(texto)

def treine():
    trainer = ListTrainer(chatbot)
    trainer.train(dataset)
    


import re

import spacy

# Carregar o modelo de linguagem em inglês
nlp = spacy.load("pt_core_news_sm")

def preprocess_input(user_input):
    # Define a pattern for "Meu nome é [nome]. Qual o seu?"
    patterns = [
        r"(Meu nome é )(.+\. Qual o seu\?)",  # "Meu nome é [nome]. Qual o seu?"
        r"(meu nome é )(.+)",  # "meu nome é [nome]"
        r"(eu sou )(.+)",  # "eu sou [nome]"
        r"(seu nome a partir de agora é )(.+)",  # "seu nome a partir de agora é [nome]"
        r"(seu nome é )(.+)"  # "seu nome é [nome]"
    ]
    
    for pattern in patterns:

        # Use regex to find matches
        match = re.search(pattern, user_input, re.IGNORECASE)

        # If a match is found, replace the name with "Poeta Urbano"
        if match:
            user_input = re.sub(match.group(2), "Poeta Urbano", user_input, flags=re.IGNORECASE)
    
    return user_input




def replace_named_entities(text):
    # Processar o texto
    doc = nlp(text)

    # Substituir entidades nomeadas por "Poeta Urbano"
    for ent in doc.ents:
        print(ent)
        print(ent.label_)
        if ent.label_ == 'PER':
            ent_text = str(ent)
            text = text.replace(ent_text, "Poeta Urbano")

    return text

import re

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
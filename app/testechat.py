from brain import responda

while True:
    x = input('> ')
    response = responda(x)
    print(f'Bot: {response}')
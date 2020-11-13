from os import system, name


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def yes_or_no(question):
    """ Vrátí True nebo False podle odpovědi uživatele """
    while True:
        answer = input(question)
        if answer in ['a', 'ano']:
            return True
        elif answer in ['n', 'ne']:
            return False

        print('    Nerozumím! Odpověz "ano" nebo "ne".\n')

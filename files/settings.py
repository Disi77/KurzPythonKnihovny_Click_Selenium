import json
from pathlib import Path
import time


import files.util as util


def save_settings(inputs):
    inputs['psw'] = None
    json_data = json.dumps(inputs)
    with open('settings.json', mode='w', encoding='utf-8') as file:
        file.write(json_data)


def load_settings():
    try:
        with open('settings.json', mode='r', encoding='utf-8') as file:
            json_data = file.read()
        return json.loads(json_data)
    except FileNotFoundError:
        print("Soubor settings.json neexistuje, bude použito defaultní nastavení.")
        time.sleep(3)
        inputs = default_inputs()
        save_settings(inputs)
        return inputs


def change_settings(inputs):
    while True:
        text = f'''
==========================================================

Pro změnu nastavení vyber číslo řádku a zadej
novou hodnotu nebo zvol Q pro ukončení nastavení.
1. Login = {inputs['login']}
2. Město = {inputs['city']}
3. Běh = {inputs['run']}
4. Cesta k chromedriver.exe = {inputs['driver-path']}

==========================================================
            '''
        print(text)
        choice = input('=>  ').upper()
        if choice == 'Q':
            util.clear()
            return inputs
        elif choice == '1':
            inputs['login'] = input('Zadej nový login: ')
            util.clear()
        elif choice == '2':
            util.clear()
            print('Zatím není možné změnit město')
        elif choice == '3':
            util.clear()
            print('Zatím není možné změnit běh')
        elif choice == '4':
            try:
                inputs['driver-path'] = str(Path(input('Zadej absolutní cestu k chromedriver.exe').strip()))
                util.clear()
            except:
                print('Něco se nepovedlo')


def default_inputs():
    inputs = {'login': None,
              'psw': None,
              'city': 'Ostrava',
              'run': 'podzim 2020',
              'driver-path': None}
    return inputs

import getpass
from pathlib import Path
import json
import click
import csv
from os import mkdir


from files.scraping_homeworks import scraping_homeworks_main
import files.stats as stats
import files.settings as settings
import files.util as util


def get_credentials(inputs):
    while True:
        if inputs['login']:
            login = inputs['login']
            print(f'\nLogin name: {login}')
        else:
            login = input("Login name: ")

        psw = getpass.getpass()
        if login and psw:
            inputs['login'] = login
            inputs['psw'] = psw
            return


def last_data():
    data_json_file = Path.cwd() / 'results/data.json'
    if data_json_file.exists():
        return True
    return False


def intro(inputs):
    util.clear()
    text = f'''
==========================================================================

Program stáhne data o domácích úkolech ze začátečnického kurzu Pythonu
pro město {inputs['city']} a běh {inputs['run']} a uloží je do složky
results.

Pro řádný běh programu si vytvoř virtuální prostředí a nainstaluj všechny
moduly ze souboru requirements.txt.

Také budeš potřebovat chromedriver.exe a do souboru s nastavením uložit
cestu k tomuto souboru.

Všechna tvá nastavení kromě hesla se uloží do souboru settings.json pro
opětovné použití při příštím spuštění programu. Můžeš se vrátit
i k původnímu nastavení.

==========================================================================
    '''
    print(text)


def print_inputs(inputs):
    text = f'''Nastavení obsahuje tyto hodnoty:
--------------------------------
Login = {inputs['login']}
Město = {inputs['city']}
Běh = {inputs['run']}
Cesta k chromedriver.exe = {inputs['driver-path']}
    '''
    print(text)


def create_pivot_table_data(d):
    pivot_table_data = []
    pivot_table_data.append(['Lekce', 'Jméno', 'Úkol', 'Výsledek'])
    for lesson, dataset in d.items():
        if lesson == "TimeStamp":
            continue
        for record in dataset[1:]:
            name = record[0]
            for index, task in enumerate(dataset[0][1:]):
                char = record[index+1]
                if char == '✓':
                    result = 3
                elif char == '⬤':
                    result = 2
                elif char == '◯':
                    result = 1
                elif char == '·':
                    result = 0
                else:
                    result = None
                pivot_table_data.append([lesson, name, task, result])
    return pivot_table_data


def save_as_csv(pivot_table_data):
    with open('results/data.csv', mode='w', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile,
                                delimiter=';',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        for row in pivot_table_data:
            csv_writer.writerow(row)


def create_folder_for_results():
    while True:
        path = Path.cwd() / 'results'
        if not path.exists():
            mkdir(path)
        else:
            return


@click.command()
@click.option('-l/-a', '--load/--ask',
              help='Program rovnou začne stahovat nová data. V opačném případě se program na tuto možnost zeptá',
              metavar='NEW_DATA')
@click.option('-w/-i', '--without/--intro',
              help='Program se spustí bez úvodního infa (nebo s) a načte uložené nastavení',
              metavar='NO_INTRO')
@click.option('-d/-s', '--default/--saved',
              help='Program použije defaultní nastavení (a přepíše to uložené) nebo použije uložené nastavení. ',
              metavar='DEFAULT_SETTINGS')
def main(load, without, default):
    if default:
        inputs = settings.default_inputs()
        settings.save_settings(inputs)
    else:
        inputs = settings.load_settings()

    if not without:
        intro(inputs)
        inputs = settings.load_settings()
        print_inputs(inputs)
        if util.yes_or_no('\nChceš změnit své nastavení? ano/ne  '):
            util.clear()
            inputs = settings.change_settings(inputs)
            settings.save_settings(inputs)

    if inputs['driver-path'] is None:
        print('Nebyla nastavena cesta k chromedriver.exe')
        return

    if load:
        get_credentials(inputs)
        scraping_homeworks_main(inputs)
        with open('results/data.json', mode='r', encoding='utf-8') as file:
            file_content = file.read()
        data = json.loads(file_content)
    else:
        if last_data():
            with open('results/data.json', mode='r', encoding='utf-8') as file:
                file_content = file.read()
            data = json.loads(file_content)
            print(f'Jsou k dispozici data z {data["TimeStamp"]}\n')
        else:
            print('Nejsou k dispozici žádná předchozí uložená data')

        if util.yes_or_no('\nChceš načíst nová data? ano/ne  '):
            get_credentials(inputs)
            scraping_homeworks_main(inputs)
            create_folder_for_results()
            with open('results/data.json', mode='r', encoding='utf-8') as file:
                file_content = file.read()
            data = json.loads(file_content)

    if last_data():
        with open('results/data.json', mode='r', encoding='utf-8') as file:
            file_content = file.read()
        data = json.loads(file_content)
        text = f'''
Data z {data["TimeStamp"]} najdeš v souboru results/data.json jako slovník,
kde klíč jsou názvy lekcí a hodnoty je seznam seznamů s konkrétními
hodnotami tak, jak to znáš z odevzdávátka.

Dále ve složce najdeš soubor data.csv, která obsahují stejná data
ve formátu CSV. Data obsahují sloupce: Lekce, Jméno, Číslo úkolu, Výsledek.

Výsledek je rozlišen takto:
  0 = úkol není odevzdán
  1 = úkol je odevzdán, ale vrácen k přepracování
  2 = úkol je odevzdán, ale není opraven koučem
  3 = úkol je splněn
'''
        util.clear()
        print(text)
        pivot_table_data = create_pivot_table_data(data)
        save_as_csv(pivot_table_data)

        if util.yes_or_no('Chceš vypsat základní statistiku? ano/ne  '):
            stats.quick_stats(pivot_table_data)


if __name__ == "__main__":
    main()

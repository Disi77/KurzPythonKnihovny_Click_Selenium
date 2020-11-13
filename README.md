# HomeWorks PyLadies CZ

Projekt byl vytvořen jako domácí úkol pro kurz Python a jeho knihovny, Ostrava podzim 2020 pořádaný PyLadies Ostrava.

* https://naucse.python.cz/2020/pyladies-ostrava-podzim-pokrocili/
* https://pyladies.cz/

Program si otevře stránky https://projekty.pyladies.cz/ s domácími úkoly pro Začátečnický kurz Pythonu Ostrava podzim 2020 a stáhne ze všech lekcí data o odevzdaných úkolech. Na konci vypíše krátkou statistiku a uloží všechna získaná data do složky results pro další použití. Pokud existují nějaké odevdané a neopravené úkoly, program vypíše, ve kterých lekcích se vyskytují.


## Instalace

1. Vytvoř a aktivuj si nové virtuální prostředí
1. Nainstaluj si všechny potřebné knihovny => `pip install -r requirements.txt`
1. Stáhni a ulož si Chromedriver (https://chromedriver.chromium.org/downloads) a nachystej si absolutní cestu k souboru chromedriver.exe, budeš ji později potřebovat.
1. Budeš potřebovat účet na https://projekty.pyladies.cz/, na kterém máš nastaveno oprávnění pro opravování úkolů pro Začátečnický kurz Pythonu Ostrava podzim 2020. Tento účet musí být registrován na stránkách (tedy nelze použít přihlášení přes Google nebo FB).

## Spuštění
1. Spusť soubor `start.py`
1. Po spuštění si v nastavení změň cestu k souboru chromedriver.exe a email, se kterým se přihlašuješ. Nastavení se uloží do souboru settings.json a nebude potřeba toto znovu nastavovat.
1. Pro různé nastavení spusť soubor s přepínačem `--help`.

import files.util as util


def quick_stats(pivot_table_data):
    lessons = list(set(x[0] for x in pivot_table_data[1:]))
    lessons.sort()

    names = []
    for row in pivot_table_data:
        if "Grafika" in row[0]:
            names.append(row[1])
    names.sort()

    results = []
    for lesson in lessons:
        results_lesson = {0: 0, 1: 0, 2: 0, 3: 0}
        for row in pivot_table_data[1:]:
            if row[0] == lesson:
                try:
                    results_lesson[row[3]] += 1
                except KeyError:
                    pass
        results.append((lesson, results_lesson))
    results.sort()

    tasks_waiting_for_check = []
    for row in pivot_table_data[1:]:
        if row[3] == 2:
            tasks_waiting_for_check.append(row)
    util.clear()
    print(60 * '=')
    print()
    print(f'Běh obsahuje celkem {len(lessons)} lekcí.')
    print('Jsou to tyto: ')
    for item in lessons:
        print(item, end=' * ')
    print('\n\n')
    print(f'Evidujeme celkem {len(names)} účastníků.')
    print('Jsou to tito: ')
    for item in names:
        print(item, end=' * ')
    print('\n')
    print(60 * '=')
    input('Pro pokračování zmáčkni ENTER: ')
    print('''
Výsledek je rozlišen takto:
      0 = úkol není odevzdán (·)
      1 = úkol je odevzdán, ale vrácen k přepracování (◯)
      2 = úkol je odevzdán, ale není opraven koučem (⬤)
      3 = úkol je splněn (✓)
    ''')
    header = ['LEKCE', 0, 1, 2, 3, '∑']
    template = f'{header[0]:>35} {header[1]:>4} {header[2]:>4} {header[3]:>4} {header[4]:>4} {header[5]:>5}'
    print(template)
    for lesson, stats in results:
        all = sum(stats.values())
        template = f'{lesson:>35} {stats[0]:>4} {stats[1]:>4} {stats[2]:>4} {stats[3]:>4} {all:>5}'
        print(template)

    if tasks_waiting_for_check:
        print()
        print(60 * '=')
        print()
        print('Pozor, v datasetu existují neopravené úkoly!')
        print()
        print(f'Je jich celkem {len(tasks_waiting_for_check)} a vyskytují se v těchto lekcích: ')
        lessons = list(set(x[0] for x in tasks_waiting_for_check))
        for item in lessons:
            print(item, end=' * ')
        print('\n\n')

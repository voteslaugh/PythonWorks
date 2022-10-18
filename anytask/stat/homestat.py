

def make_stat(filename):
    year_to_name_cnt = dict()
    year_to_surnames = dict()
    all_male_name = set()
    all_male_name.update(["Арсений", "Алехандро", "Роберт", "Богдан"])
    all_fem_name = set()
    all_fem_name.update(["Алиса"])
    male_endings = {"ов", "ин", "ев", "ёв", "ян", "ый"}
    fem_endings = {"ина", "яна", "ова", "ева", "ёва", "ая"}
    with open(filename, encoding="cp1251") as file:
        year_now = ""
        # Ищу первое вхождение "<table":
        while file.readline().find("<table") == -1:
            continue
        while True:
            line = file.readline()
            if line.find("</a>") != -1:
                ind1 = line.find('/>') + 3
                ind2 = line.find("</a>")
                name = line[ind1:ind2].split(" ")
                l_name = name[0]
                f_name = name[1]
                # Если имя встречалось в этом году, то кол-во += 1,
                # если нет, задается значение равное 1
                if f_name in year_to_name_cnt[year_now]:
                    year_to_name_cnt[year_now][f_name] += 1
                else:
                    year_to_name_cnt[year_now][f_name] = 1
                # Проверка на принадлежность имени к множеству имён
                if f_name not in all_fem_name and \
                        f_name not in all_male_name:
                    if l_name[-2:] in male_endings:
                        all_male_name.add(f_name)
                    elif l_name[-2:] in fem_endings or \
                            l_name[-3:] in fem_endings:
                        all_fem_name.add(f_name)
                year_to_surnames[year_now].append(list(name))
            elif line.find("<h3") != -1:
                ind1 = line.find('<h3>',) + 4
                ind2 = line.find("</h3>")
                year_now = line[ind1:ind2]
                year_to_surnames[year_now] = list()
                year_to_name_cnt[year_now] = {}
            elif line.find("table") != -1:
                break
            else:
                continue
    return [year_to_name_cnt, all_fem_name, all_male_name]


def extract_years(stat):
    years = list(stat[0].keys())
    years.sort()
    return years


def extract_general(stat):
    dicts = stat[0].values()
    names_to_count = {}
    for count_dict in dicts:
        for key in count_dict:
            if key in names_to_count:
                names_to_count[key] += count_dict[key]
            else:
                names_to_count[key] = count_dict[key]
    names_to_count = list(names_to_count.items())
    general_sorted = sorted(names_to_count, key=lambda x: (-x[1], x[0]))
    return general_sorted


def extract_general_male(stat):
    dicts = stat[0].values()
    all_male_name = stat[2]
    names_to_count = {}
    for count_dicts in dicts:
        for key in count_dicts:
            if key in names_to_count:
                names_to_count[key] += count_dicts[key]
            elif key in all_male_name:
                names_to_count[key] = count_dicts[key]
    names_to_count = list(names_to_count.items())
    general_sorted = sorted(names_to_count, key=lambda x: (-x[1], x[0]))
    return general_sorted


def extract_general_female(stat):
    dicts = stat[0].values()
    all_fem_name = stat[1]
    names_to_count = {}
    for count_dicts in dicts:
        for key in count_dicts:
            if key in names_to_count:
                names_to_count[key] += count_dicts[key]
            elif key in all_fem_name:
                names_to_count[key] = count_dicts[key]
    names_to_count = list(names_to_count.items())
    general_sorted = sorted(names_to_count, key=lambda x: (-x[1], x[0]))
    return general_sorted


def extract_year(stat, year):
    names_to_count = list(stat[0][str(year)].items())
    general_sorted = sorted(names_to_count, key=lambda x: (-x[1], x[0]))
    return general_sorted


def extract_year_male(stat, year):
    all_male_name = stat[2]
    names_to_count = list(stat[0][str(year)].items())
    general_sorted = list()
    for tup in names_to_count:
        if tup[0] in all_male_name:
            general_sorted.append(tup)
    general_sorted = sorted(general_sorted, key=lambda x: (-x[1], x[0]))
    return general_sorted


def extract_year_female(stat, year):
    all_fem_name = stat[1]
    names_to_count = list(stat[0][str(year)].items())
    general_sorted = list()
    for tup in names_to_count:
        if tup[0] in all_fem_name:
            general_sorted.append(tup)
    general_sorted = sorted(general_sorted, key=lambda x: (-x[1], x[0]))
    return general_sorted
    pass


if __name__ == '__main__':
    pass

from urllib.error import URLError, HTTPError
from urllib.request import urlopen
from urllib.parse import quote
import re


def get_content(name):
    """
    Функция возвращает содержимое вики-страницы name из русской Википедии.
    В случае ошибки загрузки или отсутствия страницы возвращается None.
    """

    link = 'http://ru.wikipedia.org/wiki/' + quote(name)
    try:
        with urlopen(link) as page:
            content = page.read().decode('utf-8', errors='ignore')
    except (URLError, HTTPError):
        return None
    return content


def extract_content(page):
    """
    Функция принимает на вход содержимое страницы и возвращает 2-элементный
    tuple, первый элемент которого — номер позиции, с которой начинается
    содержимое статьи, второй элемент — номер позиции, на котором заканчивается
    содержимое статьи.
    Если содержимое отсутствует, возвращается (0, 0).
    """

    start_index = page.find('<div id="bodyContent"')
    end_index = page.find('<div id="catlinks"')
    return start_index, end_index


def extract_links(page, begin, end):
    """
    Функция принимает на вход содержимое страницы и начало и конец интервала,
    задающего позицию содержимого статьи на странице и возвращает все имеющиеся
    ссылки на другие вики-страницы без повторений и с учётом регистра.
    """

    page = page[begin:end]
    titles = re.findall(r'"/wiki/\S+?(?!\.JPG)"(?: class="mw-redirect")? title="([^:«»]+?)"', page)
    title_set = set(titles)
    return title_set


def find_chain(start, finish):
    """
    Функция принимает на вход название начальной и конечной статьи и возвращает
    список переходов, позволяющий добраться из начальной статьи в конечную.
    Первым элементом результата должен быть start, последним — finish.
    Если построить переходы невозможно, возвращается None.
    """

    visited_set = {start}
    chain_set_list = [((start,), get_title_set(start))]
    for chain, title_set in chain_set_list:
        print(chain)
        print()
        if finish in title_set:
            return chain + (finish,)
        for title in title_set:
            if title in visited_set:
                continue
            visited_set.add(title)
            print(chain + (title,))
            chain_set_list.append((chain + (title,), get_title_set(title)))
    return None


def get_title_set(name):
    page = get_content(name)
    ind = extract_content(page)
    title_set = extract_links(page, ind[0], ind[1])
    return title_set

def main():
    pass


if __name__ == '__main__':
    main()

import re
import operator
import collections
import datetime
import unittest


class Request:
    _client = None
    _tz_time = None
    _page = None
    _browser = None
    _response_time = None

    def __init__(self, current_parted):
        self._client = current_parted.group(1)
        self._tz_time = current_parted.group(2)
        self._page = current_parted.group(3)
        self._browser = current_parted.group(4)
        if current_parted.group(5):
            self._response_time = int(current_parted.group(5))

    def get_client(self):
        return self._client

    def get_tz_time(self):
        return self._tz_time

    def get_page(self):
        return self._page

    def get_browser(self):
        return self._browser

    def get_response_time(self):
        return self._response_time


class Statistics:
    each_day_client_num = {}
    client_num = {}
    browser_num = {}
    page_num = {}
    page_total_response = {}
    fastest_page = None
    fastest_time_resp = None
    slowest_page = None
    slowest_time_resp = None

    def add_today_client(self, time_day, client):
        correct_form = datetime.datetime.strptime(time_day, '%d/%b/%Y').date()
        if correct_form not in self.each_day_client_num:
            self.each_day_client_num[correct_form] = {}
        if client in self.each_day_client_num[correct_form]:
            self.each_day_client_num[correct_form][client] += 1
        else:
            self.each_day_client_num[correct_form][client] = 1
        if client in self.client_num:
            self.client_num[client] += 1
        else:
            self.client_num[client] = 1

    def update_browser_number(self, browser):
        if browser in self.browser_num:
            self.browser_num[browser] += 1
        else:
            self.browser_num[browser] = 1

    def update_page_number(self, page):
        if page in self.page_num:
            self.page_num[page] += 1
        else:
            self.page_num[page] = 1

    def update_slowest_page(self, page, response_time):
        if not self.slowest_time_resp:
            self.slowest_page = page
            self.slowest_time_resp = response_time
        elif self.slowest_time_resp <= response_time:
            self.slowest_time_resp = response_time
            self.slowest_page = page

    def update_fastest_page(self, page, response_time):
        if not self.fastest_time_resp:
            self.fastest_page = page
            self.fastest_time_resp = response_time
        elif response_time <= self.fastest_time_resp:
            self.fastest_page = page
            self.fastest_time_resp = response_time

    def update_limit_pages(self, page, response_time):
        self.update_slowest_page(page, response_time)
        self.update_fastest_page(page, response_time)

    def update_total_response(self, page, response_time):
        if page in self.page_total_response:
            self.page_total_response[page] += response_time
        else:
            self.page_total_response[page] = response_time

    def get_most_popular_page(self):
        return max(self.page_num.items(),
                   key=operator.itemgetter(1))[0]

    def get_most_popular_browser(self):
        return max(sorted(self.browser_num.items()),
                   key=operator.itemgetter(1))[0]

    def get_most_active_client(self):
        return max(sorted(self.client_num.items()),
                   key=operator.itemgetter(1))[0]

    def get_slowest_average_page(self):
        average_response = {}
        for key, val in self.page_total_response.items():
            average_response[key] = val / self.page_num[key]
        return max(average_response.items(), key=operator.itemgetter(1))[0]

    def get_day_most_active_client(self, day):
        return max(sorted(self.each_day_client_num[day].items()),
                   key=operator.itemgetter(1))[0]


class Parser:
    _main_reg = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(\d+?/' \
                r'\S+?/\d+):\d\d:\d\d:\d\d .+?] "[A-Z]{3,7} (\S+) ' \
                r'.+?" \d+ \d+ ".+?" "(.+?)"(?: (\d*))?'
    statistics = Statistics()

    def line_parse(self, line):
        current_parted = re.search(self._main_reg, line)
        if current_parted:
            req = Request(current_parted)
            client = req.get_client()
            time_day = req.get_tz_time()
            page = req.get_page()
            browser = req.get_browser()
            response_time = req.get_response_time()
            # Обработка информации о клиенте

            self.statistics.add_today_client(time_day, client)
            # Обработка информации о браузере

            self.statistics.update_browser_number(browser)
            # Обработка информации о странице

            self.statistics.update_page_number(page)
            if response_time:
                self.statistics.update_limit_pages(page, response_time)
                self.statistics.update_total_response(page, response_time)
        else:
            return None

    def add_line(self, line):
        self.line_parse(line)

    def results(self):
        self.statistics.each_day_client_num = collections. \
            OrderedDict(sorted(self.statistics.each_day_client_num.items()))
        most_active = {}
        for day in self.statistics.each_day_client_num:
            client = self.statistics.get_day_most_active_client(day)
            most_active[day] = client
        result = {"FastestPage": self.statistics.fastest_page,
                  "MostActiveClient":
                      self.statistics.get_most_active_client(),
                  "MostActiveClientByDay": most_active,
                  "MostPopularBrowser":
                      self.statistics.get_most_popular_browser(),
                  "MostPopularPage":
                      self.statistics.get_most_popular_page(),
                  "SlowestAveragePage":
                      self.statistics.get_slowest_average_page(),
                  "SlowestPage": self.statistics.slowest_page}
        return result


def make_stat():
    return Parser()


class LogStatTests(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()
        self.parser.add_line(
            '192.100.10.10 - - [17/Feb/2013:06:37:21 +0600] "GET '
            '/tv/useUser HTTP/1.1" 200 432 "asd" "Yandex" 2')
        self.parser.add_line(
            '192.100.12.10 - - [17/Feb/2013:06:37:21 +0600] "GET '
            '/tv/Needed HTTP/1.1" 200 432 "asd" "Yandex" 2')
        self.parser.add_line(
            '192.168.12.10 - - [17/Feb/2013:06:37:21 +0600] "GET '
            '/tv/useUser HTTP/1.1" 200 432 "asd" "Yandex" 1')

    def test_bad_line(self):
        self.assertEqual(self.parser.statistics.fastest_page, "/tv/useUser")

    def test_average_time(self):
        self.assertEqual(self.parser.statistics.get_slowest_average_page(),
                         "/tv/Needed")

    def test_most_active_client(self):
        self.assertEqual(self.parser.statistics.get_most_active_client(),
                         '192.100.10.10')


def main():
    par = Parser()
    with open("example_3.log") as file:
        for line in file:
            par.add_line(line)
    res = par.results()
    for i in res:
        print(res[i])


if __name__ == "__main__":
    main()
import sys
import pprint
from datetime import datetime, time, timedelta
from bs4 import BeautifulSoup
import requests

MON_TO_FRI = '月〜金（水曜除く）'
WED = '水曜日'
SAT = '土曜日'

FROM_UNIV = '大学発'
FROM_SHRINE = '神社発'


def make_date_time(hour, minu):
    today = datetime.today()
    t = time(int(hour), int(minu), 0)

    dt = datetime.combine(today, t)

    return dt


def split_time_table(body, num):
    ret = body.find_all('td')[num].string.split('・')
    return [x for x in ret if x != '']


def get_time_table(url):
    res = requests.get('http://www.kyoto-su.ac.jp/bus/kamigamo/index.html')

    soup = BeautifulSoup(res.content, 'html.parser')

    time_table_div = soup.body.find("div", class_="wysiwyg")

    time_table_list = time_table_div.find_all('tr')

    time_table_dic = {
        MON_TO_FRI: {FROM_UNIV: [], FROM_SHRINE: []},
        WED: {FROM_UNIV: [], FROM_SHRINE: []},
        SAT: {FROM_UNIV: [], FROM_SHRINE: []}
    }

    for index in range(2, len(time_table_list)):
        if index == 3:
            continue

        # 時刻表
        hour = time_table_list[index].find('th').string
        body = time_table_list[index]

        # 月〜金　大学発
        time_table_dic[MON_TO_FRI][FROM_UNIV] +=\
            [make_date_time(hour, minu) for minu in split_time_table(body, 0)]
        # 月〜金　神社発
        # TODO: 神社発は21時以降のバス無し(2020/11/13現在)
        if index < 16:
            time_table_dic[MON_TO_FRI][FROM_SHRINE] +=\
                [make_date_time(hour, minu)
                 for minu in split_time_table(body, 1)]
        # 水曜日　大学発
        time_table_dic[WED][FROM_UNIV] +=\
            [make_date_time(hour, minu)
             for minu in split_time_table(body, 2)]
        # 水曜日　神社発
        # TODO: 神社発は21時以降のバス無し(2020/11/13現在)
        if index < 16:
            time_table_dic[WED][FROM_SHRINE] +=\
                [make_date_time(hour, minu)
                 for minu in split_time_table(body, 3)]

        # 土曜日は14時以降のバス無し(2020/11/13現在)
        if index < 9:
            # 土曜日　大学発
            time_table_dic[SAT][FROM_UNIV] +=\
                [make_date_time(hour, minu)
                 for minu in split_time_table(body, 4)]
            # 土曜日　神社発
            time_table_dic[SAT][FROM_SHRINE] +=\
                [make_date_time(hour, minu)
                 for minu in split_time_table(body, 5)]
    return time_table_dic


def search_departure(time_table, now):
    for table in time_table:
        if now < table:
            return table


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'from_shrine':
            from_ = FROM_SHRINE
            buffer = 12
        elif sys.argv[1] == 'from_univ':
            from_ = FROM_UNIV
            buffer = 7
        else:
            print("error: invalid argument: ", sys.argv[1])
            exit(1)
    else:
        print("Use argument, from_shrine or from_univ")
        exit(1)

    time_table = get_time_table(
        'http://www.kyoto-su.ac.jp/bus/kamigamo/index.html')

    now = datetime.now()
    now += timedelta(minutes=buffer)

    # 曜日検索
    days_of_week = now.strftime('%a')
    if days_of_week != 'Wed' and days_of_week != 'Sat' and days_of_week != 'Sun':
        day = MON_TO_FRI

    elif days_of_week == 'Wed':
        day = WED
    elif days_of_week == 'Sat':
        day = SAT
    else:
        day = ''

    # バスの出発時刻検索
    if day in time_table:
        departure = search_departure(time_table[day][from_], now)

    if departure is not None:
        print(f'🚌 {from_} {departure.hour}:{departure.minute}')
    else:
        print(None)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3.6
import requests
import sys
import bs4 as bs
from datetime import datetime as dt
from itertools import islice

try:
    url = 'http://esportlivescore.com/g_dota.html'
    s = requests.get(url, timeout=10)
    s.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
    sys.exit(1)

b = bs.BeautifulSoup(s.text, 'html.parser')


def print_list(columns=0, lst=[]):
    i, llen = [], len(lst)
    for n in range(columns):
        i.append(islice(iter(lst), n, llen, columns))

    for x in zip(*i):
        print(' '.join(('{}',)*columns).format(*x))


def get_table(columns=2, tag='', lst=[]):
    lst.append(dt.fromtimestamp(int(tag['data-unixtime'])))
    lst.append(tag.select('div.mobile-tournament-info > span')[0].text.strip())
    if columns == 4:
        lst.append(':'.join(x for x in
                            (tag.select('span.home-runningscore')[0].text,
                             tag.select('span.away-runningscore')[0].text)))
    lst.append(tag.select('div.event-date a')[0]['title'])


def get_tag(marker='', score='with-score'):
    live = 'is-not-live'
    if marker == 'div#upcoming' and score == 'with-score':
        live = 'is-live'
    return b.select('{} > div.match-event.event.{}.{}'
                    .format(marker, live, score))


rec = []
queue = [('div#upcoming', 'with-score', 'Live matches', 4),
         ('div#upcoming', 'without-score', 'Upcoming matches', 3),
         ('div#finished', 'with-score', 'Finished matches', 4)]

for marker, score, header, columns in queue:
    for tag in get_tag(marker, score):
        get_table(columns, tag, rec)
    print('\n{}:'.format(header))
    print_list(columns, rec)
    rec.clear()

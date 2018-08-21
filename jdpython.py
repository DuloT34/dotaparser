#!/usr/bin/env python
import requests, bs4, datetime

try:
    s = requests.get('http://esportlivescore.com/g_dota.html')
    s.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
    sys.exit(1)

b=bs4.BeautifulSoup(s.text, "html.parser")

liveTag = b.find_all("div", {"id": "live"})
livematches=[]
for tag in liveTag:
    notliveTags = tag.find_all("div", {"class": ["match-event event without-score is-not-live"]})
    for tag in notliveTags:
        timestamp = str(datetime.datetime.fromtimestamp(float((tag.find("span", {"class": ["hide phpunixtime"]})).text[0:10])))
        gameformat = str(tag.find("div", {"class": ["event-tournament-info"]}).text.strip())
        teams = str(tag.find("div", {"class": ["team-home"]}).text.strip()) + " vs " + str(tag.find("div", {"class": ["team-away"]}).text.strip())
        livematches.append(timestamp + '\t' + gameformat + '\t' + teams)
str1 = '\n'.join(livematches)

upcTag = b.find_all("div", {"id": "upcoming"})
upcomingmatches=[]
for tag in upcTag:
    notliveTags = tag.find_all("div", {"class": ["match-event event without-score is-not-live"]})
    for tag in notliveTags:
        timestamp = str(datetime.datetime.fromtimestamp(float((tag.find("span", {"class": ["hide phpunixtime"]})).text[0:10])))
        gameformat = str(tag.find("div", {"class": ["event-tournament-info"]}).text.strip())
        teams = str(tag.find("div", {"class": ["team-home"]}).text.strip()) + " vs " + str(tag.find("div", {"class": ["team-away"]}).text.strip())
        upcomingmatches.append(timestamp + '\t' + gameformat + '\t' + teams)
str2 = '\n'.join(upcomingmatches)

resTag = b.find_all("div", {"id": "finished"})
finishedmatches=[]
for tag in resTag:
    finishedTags = tag.find_all("div", {"class": ["match-event event with-score is-not-live"]})
    for tag in finishedTags:
        timestamp = str(datetime.datetime.fromtimestamp(float((tag.find("span", {"class": ["hide phpunixtime"]})).text[0:10])))
        score = str(tag.find("span", {"class": ["home-runningscore"]}).text) + ":" + str(tag.find("span", {"class": ["away-runningscore"]}).text)
        teams = str(tag.find("div", {"class": ["team-home"]}).text.strip()) + " vs " + str(tag.find("div", {"class": ["team-away"]}).text.strip())
        finishedmatches.append(timestamp + '\t' + score + '\t' + teams)
str3 = '\n'.join(finishedmatches)

if str1 and str1.strip():
    print('Live matches:\n' + str1 + '\n')
else:
    print('Live matches:\n' + "No live matches" +'\n')

if str2 and str2.strip():
    print('Upcoming matches:\n' + str2 + '\n')
else:
    print('Upcoming matches:\n' + "No upcoming matches" +'\n')

if str3 and str3.strip():
    print('Finished matches:\n' + str3)
else:
    print('Finished matches:\n' + "No recent results" +'\n')

#!/usr/bin/python3
import requests, bs4, datetime

s=requests.get('http://esportlivescore.com/g_dota.html')

b=bs4.BeautifulSoup(s.text, "html.parser")

liveTag = b.find_all("div", {"id": "live"})
livematches=[]
for tag in liveTag:
    notliveTags = tag.find_all("div", {"class": ["match-event event without-score is-not-live"]})
    for tag in notliveTags:
        timestamp = str(datetime.datetime.fromtimestamp(float((tag.find("span", {"class": ["hide phpunixtime"]})).text[0:10])))
        gameformat = str(tag.find("div", {"class": ["event-tournament-info"]}).text)
        teams = str(tag.find("div", {"class": ["team-home"]}).text.strip()) + " vs " + str(tag.find("div", {"class": ["team-away"]}).text.strip())
        livematches.append(timestamp + gameformat + teams)
str1 = '\n'.join(livematches)

upcTag = b.find_all("div", {"id": "upcoming"})
upcomingmatches=[]
for tag in upcTag:
    notliveTags = tag.find_all("div", {"class": ["match-event event without-score is-not-live"]})
    for tag in notliveTags:
        timestamp = str(datetime.datetime.fromtimestamp(float((tag.find("span", {"class": ["hide phpunixtime"]})).text[0:10])))
        gameformat = str(tag.find("div", {"class": ["event-tournament-info"]}).text)
        teams = str(tag.find("div", {"class": ["team-home"]}).text.strip()) + " vs " + str(tag.find("div", {"class": ["team-away"]}).text.strip())
        upcomingmatches.append(timestamp + gameformat + teams)
str2 = '\n'.join(upcomingmatches)

resTag = b.find_all("div", {"id": "finished"})
finishedmatches=[]
for tag in resTag:
    finishedTags = tag.find_all("div", {"class": ["match-event event with-score is-not-live"]})
    for tag in finishedTags:
        timestamp = str(datetime.datetime.fromtimestamp(float((tag.find("span", {"class": ["hide phpunixtime"]})).text[0:10])))
        score = str(tag.find("span", {"class": ["home-runningscore"]}).text) + ":" + str(tag.find("span", {"class": ["away-runningscore"]}).text)
        teams = str(tag.find("div", {"class": ["team-home"]}).text.strip()) + " vs " + str(tag.find("div", {"class": ["team-away"]}).text.strip())
        finishedmatches.append(timestamp + " " + score + " " + teams)
str3 = '\n'.join(finishedmatches)

print('Live matches:\n' + str1 + '\n')
print('Upcoming matches:\n' + str2 + '\n')
print('Finished matches:\n' + str3)

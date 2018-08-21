#!/usr/bin/env python
import requests, bs4, datetime

str1=[]
str2=[]
str3=[]

try:
    s = requests.get('http://esportlivescore.com/g_dota.html')
    s.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
    sys.exit(1)

b=bs4.BeautifulSoup(s.text, "html.parser")

livematches=[]
try:
    for tag in b.find("div", {"id": "live"}).find_all("div", {"class": ["match-event event without-score is-live"]}): 
        timestamp = str(datetime.datetime.fromtimestamp(float((tag.find("span", {"class": ["hide phpunixtime"]})).text[0:10])))
        gameformat = str(tag.find("div", {"class": ["event-tournament-info"]}).text.strip())
        teams = str(tag.find("div", {"class": ["team-home"]}).text.strip()) + " vs " + str(tag.find("div", {"class": ["team-away"]}).text.strip())
        livematches.append(timestamp + '\t' + gameformat + '\t' + teams)
    str1 = '\n'.join(livematches)
except:
    tag = None 

upcomingmatches=[]
try:
    for tag in b.find("div", {"id": "upcoming"}).find_all("div", {"class": ["match-event event without-score is-not-live"]}): 
            timestamp = str(datetime.datetime.fromtimestamp(float((tag.find("span", {"class": ["hide phpunixtime"]})).text[0:10])))
            gameformat = str(tag.find("div", {"class": ["event-tournament-info"]}).text.strip())
            teams = str(tag.find("div", {"class": ["team-home"]}).text.strip()) + " vs " + str(tag.find("div", {"class": ["team-away"]}).text.strip())
            upcomingmatches.append(timestamp + '\t' + gameformat + '\t' + teams)
    str2 = '\n'.join(upcomingmatches)
except:
    tag = None 

finishedmatches=[]
try:
    for tag in b.find("div", {"id": "finished"}).find_all("div", {"class": ["match-event event with-score is-not-live"]}):
            timestamp = str(datetime.datetime.fromtimestamp(float((tag.find("span", {"class": ["hide phpunixtime"]})).text[0:10])))
            score = str(tag.find("span", {"class": ["home-runningscore"]}).text) + ":" + str(tag.find("span", {"class": ["away-runningscore"]}).text)
            teams = str(tag.find("div", {"class": ["team-home"]}).text.strip()) + " vs " + str(tag.find("div", {"class": ["team-away"]}).text.strip())
            finishedmatches.append(timestamp + '\t' + score + '\t' + teams)
    str3 = '\n'.join(finishedmatches)
except:
    tag = None

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

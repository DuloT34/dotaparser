import requests, bs4, datetime

s=requests.get('http://esportlivescore.com/g_dota.html')

b=bs4.BeautifulSoup(s.text, "html.parser")
upcTag = b.find_all("div", {"id": "upcoming"})
upcomingmatches=[]

for tag in upcTag:
    notliveTags = tag.find_all("div", {"class": ["match-event event without-score is-not-live"]})
    for tag in notliveTags:
        timestamp = str(datetime.datetime.fromtimestamp(float((tag.find("span", {"class": ["hide phpunixtime"]})).text[:-3])))
        gameformat = str(tag.find("div", {"class": ["event-tournament-info"]}).text)
        teams = str(tag.find("div", {"class": ["team-home"]}).text.strip()) + " vs " + str(tag.find("div", {"class": ["team-away"]}).text.strip())
        upcomingmatches.append(timestamp + gameformat + teams)
str1 = '\n'.join(upcomingmatches)
print('Upcoming matches:\n' + str1)

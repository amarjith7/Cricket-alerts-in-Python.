import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import re
from time import sleep
def get_current_matches():
# Function to fetch the live matches currently
in play
page =
requests.get('http://static.cricinfo.com/rss/livesco
res.xml')
soup = BeautifulSoup(page.text, 'lxml')
matches = soup.find_all('description')
live_matches = [s.get_text() for s in matches
if '*' in s.get_text()]
return live_matches
def fetch_score(matchNum):
# Function to return the live score of the
match specified
page =
requests.get('http://static.cricinfo.com/rss/livesco
res.xml')
soup = BeautifulSoup(page.text, 'lxml')
matches = soup.find_all('description')
live_matches = [s.get_text() for s in matches
if '*' in s.get_text()]
scorecard = live_matches[matchNum]
return re.sub(r'<.+?>', '', scorecard) # remove
HTML tags
def notify(score, prev_score):
# Function for Windows toast desktop
notification
toaster = ToastNotifier()
ifscore != prev_score:
if '4 runs' in score:
toaster.show_toast(score, "A boundary
was scored!")
elif 'OUT' in score:
toaster.show_toast(score, "A wicket has
fallen!")
elif '6 runs' in score:
toaster.show_toast(score, "A six was
scored!")
prev_score = score
return prev_score
if name == " main ":
matches = get_current_matches()
print('Current matches in play')
print('=' * 23)
for i, match in enumerate(matches):
print('[{}] '.format(i) +
re.search('\D+',
match.split('v')[0]).group() + 'vs.' +
re.search('\D+',
match.split('v')[1]).group()
)
print()
matchNum = int(input('Pick the match
number [0,1,2...] => '))
prev_score = ''
# show desktop notification for events
while True:
current_score = fetch_score(matchNum)
prev_score = notify(current_score,
prev_score)
sleep(30)

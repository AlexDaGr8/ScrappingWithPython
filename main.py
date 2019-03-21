import requests
import urllib
import time
from bs4 import BeautifulSoup
import csv
from datetime import datetime

from region import Region
from game import Game
from team import Team

def byYear(year):
    print(str(year))
    url = 'https://en.wikipedia.org/wiki/' + str(year) + '_NCAA_Division_I_Men%27s_Basketball_Tournament'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # tables = soup.findAll('table')
    h3s = soup.findAll('h3')
    for i, h3 in enumerate(h3s):
        lst = list(h3.children)
        if len(lst) == 3 and i < 10:
            if not 'First Four' in lst[1].text and not 'Opening Round Game' in lst[1].text:
                parseHead(h3)
    print('--------------------')

def parseHead(data):
    h3Chld = list(data.children)
    print(str('Regional' in h3Chld[1].text) + ' - ' + h3Chld[1].text)
    region = Region(h3Chld[1].text)
    parseTable(data.find_next_sibling('table'), region)

def parseTable(tbl, region):
    tblLst = tbl.findAll('tr')
    sublist = [tblLst[x:x+3] for x in range(0, len(tblLst), 3)]
    sublist.pop(0)
    for sub in sublist:
        game = Game()
        if len(sub) == 3:
            game.team1 = getGameTeamInfo(sub[0].findAll('td'))
            game.team2 = getGameTeamInfo(sub[2].findAll('td'))
            print('score - ' + str(game.team1.score) + ' to ' + str(game.team2.score))
            print('yyyyyyyyyyyyyyyyyyyy')
            region.games.append(game)

def getGameTeamInfo(tds):
    team = Team()
    if len(tds) >= 3:
        if not tds[1].text:
            print('rank - ' + tds[2].text.strip()) # rank
            team.rank = tds[2].text.strip()
            if tds[3].b is None:
                print(tds[3].text.strip() + ' LOST')
                team.name = tds[3].text.strip()
                team.win = False
            else:
                print(tds[3].b.text.strip() + ' WON')
                team.name = tds[3].b.text.strip()
                team.win = True
            print(tds[4].text.strip()) # score
            team.score = tds[4].text.strip()
        else:
            print('rank - ' + tds[1].text.strip()) # rank
            if tds[2].b is None:
                print(tds[2].text.strip() + ' LOST') # name
                team.name = tds[2].text.strip()
                team.win = False
            else:
                print(tds[2].text.strip() + ' WON') # name
                team.name = tds[2].text.strip()
                team.win = True
            print(tds[3].text.strip()) # score
            team.score = tds[3].text.strip()
        print('xxxxxxxxxxxxxxxxx')
    return team

def writeline(row):
    with open('index.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file)



for i in range(2008, 2019, 1):
    byYear(i)


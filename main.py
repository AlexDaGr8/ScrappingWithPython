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
    h3s = soup.findAll('h3')
    difh3s = list(filter(lambda x: True if (len(list(x.children)) == 3 and '[edit]' in x.text and not 'First Four' in x.text and not 'Opening Round Game' in x.text and not 'Internet/other' in x.text) else False, h3s))
    regions = []
    for h3 in difh3s:
        regions.append(parseHead(h3))
    print('--------------------')
    return regions

def parseHead(data):
    h3Chld = list(data.children)
    #print(str('Regional' in h3Chld[1].text) + ' - ' + h3Chld[1].text)
    region = Region(h3Chld[1].text)
    region.games = parseTable(data.find_next_sibling('table'))
    return region

def parseTable(tbl):
    tblLst = tbl.findAll('tr')
    sublist = [tblLst[x:x+3] for x in range(0, len(tblLst), 3)]
    sublist.pop(0)
    games = []
    finalFour = True if len(sublist) < 5 else False
    for i, sub in enumerate(sublist):
        game = Game(getRound(i+1, finalFour))
        if len(sub) == 3:
            game.team1 = getGameTeamInfo(sub[0].findAll('td'))
            game.team2 = getGameTeamInfo(sub[2].findAll('td'))
            #print('score - ' + str(game.team1.score) + ' to ' + str(game.team2.score) + ' | ' + game.round)
            #print('yyyyyyyyyyyyyyyyyyyy')
            games.append(game)
    return games

def getGameTeamInfo(tds):
    team = Team()
    if len(tds) >= 3:
        if not tds[1].text:
            print('rank - ' + tds[2].text.strip()) # rank
            team.rank = tds[2].text.strip()
            if tds[3].b is None:
                #print(tds[3].text.strip() + ' LOST')
                team.name = tds[3].text.strip()
                team.win = False
            else:
                #print(tds[3].b.text.strip() + ' WON')
                team.name = tds[3].b.text.strip()
                team.win = True
            #print(tds[4].text.strip()) # score
            team.score = tds[4].text.strip()
        else:
            print('rank - ' + tds[1].text.strip()) # rank
            team.rank = tds[1].text.strip()
            if tds[2].b is None:
                #print(tds[2].text.strip() + ' LOST') # name
                team.name = tds[2].text.strip()
                team.win = False
            else:
                #print(tds[2].text.strip() + ' WON') # name
                team.name = tds[2].text.strip()
                team.win = True
            #print(tds[3].text.strip()) # score
            team.score = tds[3].text.strip()
        #print('xxxxxxxxxxxxxxxxx')
    return team

def writeline(row):
    with open('index.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])


def getRound(val, finalfour):
    if not (val % 2) == 0:
        return 'round5' if finalfour else 'round1'
    else:
        if ((val - 2) % 4) == 0:
            return 'round6' if finalfour else 'round2'
        elif ((val - 4) % 8) == 0:
            return 'round3'
        else:
            return 'round4'
with open('index.csv', 'w+') as csv_file:
    fieldnames = ['year', 'region', 'round', 't1Name', 't1Rank', 't1Score', 't1Win', 't2Name', 't2Rank', 't2Score', 't2Win']
    writer = csv.writer(csv_file)
    writer.writerow(fieldnames)
    for i in range(2008, 2019, 1):
        for reg in byYear(i):
            print(reg.name)
            for game in reg.games:
                print(game.round)
                writer.writerow([str(i), reg.name, game.round, game.team1.name, str(game.team1.rank), str(game.team1.score), game.team1.win, game.team2.name, game.team2.rank, game.team2.score, game.team2.win])




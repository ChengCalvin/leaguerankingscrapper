import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

url = 'https://na.op.gg/ranking/ladder/'

# success = return response 200
page = requests.get(url)
page_number = 2

soup = BeautifulSoup(page.content, 'html.parser')

player_list = []
total_game = []
game_data = []
count = 0

for name in soup.find_all("td", class_="select_summoner ranking-table__cell ranking-table__cell--summoner"):
    player_list.append(name.get_text())
    # print(name.get_text())

for page in range(2, 10):
    if page_number <= 100:
        next_page = 'https://na.op.gg/ranking/ladder/page={}'.format(page_number)
        page = requests.get(next_page)
        soup = BeautifulSoup(page.content, 'html.parser')
        for name in soup.find_all("td", class_="select_summoner ranking-table__cell ranking-table__cell--summoner"):
            player_list.append(name.get_text())
            # print(name.get_text())
        page_number += 1

    for player_number in range(0, len(player_list)):
        player = player_list[player_number]
    # get player stat URL
    player_url = 'https://na.op.gg/summoner/userName={}'.format(player)
    player_page = requests.get(player_url)
    soup = BeautifulSoup(player_page.content, 'html.parser')

    scoreboards = soup.find_all("div", class_="GameItemWrap")

    for scoreboard in scoreboards:
        game_team = []
        teams = scoreboard.find_all('div', {'class': 'Team'})

        team_text1 = teams[0].get_text().split('\n')

        team_a = [str(team_text1[4]), str(team_text1[13]), str(team_text1[22]), str(team_text1[31]),
                  str(team_text1[40])]
        game_team.append(team_a)

        team_text2 = teams[1].get_text().split('\n')
        team_b = [str(team_text2[4]), str(team_text2[13]), str(team_text2[22]), str(team_text2[31]),
                  str(team_text2[40])]
        game_team.append(team_b)

        summoner_requesters = scoreboard.find_all('div', 'Summoner Requester')
        results = scoreboard.find_all('div', 'GameResult')
        result = results[0].get_text().replace('\n', '').replace('\t', '')

        for summoner_requester in summoner_requesters:
            summoner = summoner_requester.find_all('a')
            if str(summoner[0].get_text()) in team_text1 and ('Victory' in result):
                a_win = 'Team A'
                game_team.append(a_win)
                game_data.append({'Team A': team_a, 'Team B': team_b, 'Result': a_win})
                count += 1
            else:
                b_win = 'Team B'
                game_team.append(b_win)
                game_data.append({'Team A': team_a, 'Team B': team_b, 'Result': b_win})
                count += 1


with open('gamedata.json', 'w') as f:
  f.write(json.dumps({'data': game_data}))

import requests
from bs4 import BeautifulSoup

url = 'https://na.op.gg/ranking/ladder/'

# success = return response 200
page = requests.get(url)
page_number = 2

soup = BeautifulSoup(page.content, 'html.parser')

player_list = []
total_game = []
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

        # for i in range(len(teams)):
        team_text1 = teams[0].get_text().split('\n')
        # print(team_text)
        team_a = ['Team A: ' + str(team_text1[4]) + ', ' + str(team_text1[13]) + ', ' + str(team_text1[22]) + ', ' + str(
            team_text1[31]) + ', ' + str(team_text1[40])]
        game_team.append(team_a)
        team_text2 = teams[1].get_text().split('\n')
        team_b = ['Team B: ' + str(team_text2[4]) + ', ' + str(team_text2[13]) + ', ' + str(team_text2[22]) + ', ' + str(
            team_text2[31]) + ', ' + str(team_text2[40])]
        game_team.append(team_b)

        summoner_requesters = scoreboard.find_all('div', 'Summoner Requester')
        results = scoreboard.find_all('div', 'GameResult')
        result = results[0].get_text().replace('\n', '').replace('\t', '')

        for summoner_requester in summoner_requesters:
            summoner = summoner_requester.find_all('a')
            #print(summoner.get_text())
            if str(summoner[0].get_text()) in team_text1 and ('Victory' in result):
                game_team.append('Team A')
            else:
                game_team.append('Team B')


        #game_team.append(result)
        #total_game.append(game_team) # every player has their own total game summing their match history
        print(game_team)

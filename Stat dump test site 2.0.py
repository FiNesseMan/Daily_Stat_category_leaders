import requests
import os
import datetime
from requests_oauthlib import OAuth1Session
import time

# Twitter OAuth setup
access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')

oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)




# NHL API endpoint and initial pagination parameters
url = "https://api.nhle.com/stats/rest/en/skater/summary"
params = {
    'isAggregate': 'false',
    'start': 0,
    'limit': 100,  # Adjust the page size as needed
    'factCayenneExp': 'gamesPlayed>29',
    'cayenneExp': 'gameTypeId=2 and seasonId>=20232024'
}

all_players = []

# Pagination handling
while True:
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        players = data['data']
        all_players.extend(players)

        if len(players) < params['limit']:
            break  # Exit the loop if last page

        params['start'] += params['limit']  # Prepare for next page
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        break

players_sorted = sorted(all_players, key=lambda x: x['points'], reverse=True)

most_points = None
player_count = 0
rank = 0
output_lines = []
processed_players_highpoints = set()
for player in players_sorted[:5]:
    if player['skaterFullName'] in processed_players_highpoints:
        continue

    player_count += 1
    processed_players_highpoints.add(player['skaterFullName'])
    if player['points'] != most_points:
        rank = player_count
        most_points = player['points']
    output_lines.append(f"{rank}. {player['skaterFullName']} ({player['teamAbbrevs']}), {player['points']} Points, {player['gamesPlayed']} GP.")

output = "Points Leaders NHL:\n\n" + "\n".join(output_lines)
# print(output)
payload = {"text": output}
response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
time.sleep(100)


# Process the retrieved players data
# Least points in the NHL with over 30 GP
players_sorted = sorted(all_players, key=lambda x: x['points'], reverse=False)

last_points = None
player_count = 0
rank = 0
output_lines = []
processed_players_lowpoints = set()
for player in players_sorted[:5]:
    if player['skaterFullName'] in processed_players_lowpoints:
        continue

    player_count += 1
    processed_players_lowpoints.add(player['skaterFullName'])
    if player['points'] != last_points:
        rank = player_count
        last_points = player['points']
    output_lines.append(f"{rank}. {player['skaterFullName']} ({player['teamAbbrevs']}), {player['points']} points, {player['gamesPlayed']} GP.")

output = "Least Points in the NHL (Over 30 GP):\n\n" + "\n".join(output_lines)
# print(output)
payload = {"text": output}
response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
time.sleep(100)
##--------------------------------------------------------------------------------------



## Most goals in the NHL
players_sorted = sorted(all_players, key=lambda x: x['goals'], reverse=True)

most_goals = None
player_count = 0
rank = 0
output_lines =[]
processed_players_goals = set()
for player in players_sorted[:5]:
    if player['skaterFullName'] in processed_players_goals:
        continue

    player_count += 1
    processed_players_goals.add(player['skaterFullName'])

    if player['goals'] != most_goals:
        rank = player_count
        most_goals = player['goals']

    output_lines.append(f"{rank}. {player['skaterFullName']} ({player['teamAbbrevs']}), {player['goals']} goals, {player['gamesPlayed']} GP.")

output = "Most Goals in the NHL:\n\n" + "\n".join(output_lines)
# print(output)
payload = {"text": output}
response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
time.sleep(100)
##--------------------------------------------------------------------------------------

## Most goals by DMEN
filtered_players = [player for player in all_players if player['positionCode'] in ['D']]

# # Sorting the filtered players by goals in descending order
players_sorted = sorted(filtered_players, key=lambda x: x['goals'], reverse=True)

most_goals = None
player_count = 0
rank = 0
output_lines =[]
processed_players_dgoals = set()
for player in players_sorted[:5]:
    if player['skaterFullName'] in processed_players_dgoals:
        continue

    player_count += 1
    processed_players_dgoals.add(player['skaterFullName'])

    if player['goals'] != most_goals:
        rank = player_count
        most_goals = player['goals']

    output_lines.append(f"{rank}. {player['skaterFullName']} ({player['teamAbbrevs']}), {player['goals']} goals, {player['gamesPlayed']} GP.")

output = "Most Goals in the NHL by Defensemen:\n\n" + "\n".join(output_lines)
# print(output)
payload = {"text": output}
response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
time.sleep(100)
##--------------------------------------------------------------------------------------

## Most Shots in the NHL

players_sorted = sorted(all_players, key=lambda x: x['shots'], reverse=True)

most_shots = None
player_count = 0
rank = 0
output_lines =[]
processed_players_highshot = set()
for player in players_sorted[:5]:
    if player['skaterFullName'] in processed_players_highshot:
        continue

    player_count += 1
    processed_players_highshot.add(player['skaterFullName'])

    if player['shots'] != most_shots:
        rank = player_count
        most_shots = player['shots']

    output_lines.append(f"{rank}. {player['skaterFullName']} ({player['teamAbbrevs']}), {player['shots']} Shots, {player['gamesPlayed']} GP.")
output = "Most Shots in the NHL:\n\n" + "\n".join(output_lines)
# print(output)
payload = {"text": output}
response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
time.sleep(100)
##--------------------------------------------------------------------------------------
## Least Shots in the NHL (over 30 GP)

players_sorted = sorted(all_players, key=lambda x: x['shots'], reverse=False)

least_assists = None
player_count = 0
rank = 0
output_lines =[]
processed_players_lowshot = set()
for player in players_sorted[:5]:
    if player['skaterFullName'] in processed_players_lowshot:
        continue

    player_count += 1
    processed_players_lowshot.add(player['skaterFullName'])

    if player['shots'] != least_assists:
        rank = player_count
        least_assists = player['shots']

    output_lines.append(f"{rank}. {player['skaterFullName']} ({player['teamAbbrevs']}), {player['shots']} Shots, {player['gamesPlayed']} GP.")
output = "Least Shots in the NHL(Over 30 GP):\n\n" + "\n".join(output_lines)
# print(output)
payload = {"text": output}
response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
time.sleep(100)
##--------------------------------------------------------------------------------------
# Most assists in the NHL

players_sorted = sorted(all_players, key=lambda x: x['assists'], reverse=True)

most_assists = None
player_count = 0
rank = 0
output_lines =[]
processed_players_highAss = set()
for player in players_sorted[:5]:
    if player['skaterFullName'] in processed_players_highAss:
        continue

    player_count += 1
    processed_players_highAss.add(player['skaterFullName'])

    if player['shots'] != most_assists:
        rank = player_count
        most_assists = player['assists']

    output_lines.append(f"{rank}. {player['skaterFullName']} ({player['teamAbbrevs']}), {player['assists']} assists, {player['gamesPlayed']}  GP.")
output = "Most assists in the NHL:\n\n" + "\n".join(output_lines)
# print(output)
payload = {"text": output}
response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
time.sleep(100)
##--------------------------------------------------------------------------------------
## +/- leaders in the NHL

players_sorted = sorted(all_players, key=lambda x: x['plusMinus'], reverse=True)

plus_minus = None
player_count = 0
rank = 0
output_lines =[]
processed_players_highPM = set()
for player in players_sorted[:5]:
    if player['skaterFullName'] in processed_players_highPM:
        continue

    player_count += 1
    processed_players_highPM.add(player['skaterFullName'])

    if player['plusMinus'] != plus_minus:
        rank = player_count
        plus_minus = player['plusMinus']

    output_lines.append(f"{rank}. {player['skaterFullName']} ({player['teamAbbrevs']}), +{player['plusMinus']}.")
output = "+/- leaders in the NHL:\n\n" + "\n".join(output_lines)
# print(output)
payload = {"text": output}
response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
time.sleep(100)
##--------------------------------------------------------------------------------------
## Worst +/-  in the NHL

players_sorted = sorted(all_players, key=lambda x: x['plusMinus'], reverse=False)

plus_minus = None
player_count = 0
rank = 0
output_lines =[]
processed_players_lowPM = set()
for player in players_sorted[:5]:
    if player['skaterFullName'] in processed_players_lowPM:
        continue

    player_count += 1
    processed_players_lowPM.add(player['skaterFullName'])
    if player['plusMinus'] != plus_minus:
        rank = player_count
        plus_minus = player['plusMinus']

    output_lines.append(f"{rank}. {player['skaterFullName']} ({player['teamAbbrevs']}), {player['plusMinus']}.")
output = "Worst +/- in the NHL:\n\n" + "\n".join(output_lines)
# print(output)
payload = {"text": output}
response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
time.sleep(100)

#--------------------------------------------------------------------------------------
# Goalie NHL API endpoint and initial pagination parameters
url = "https://api.nhle.com/stats/rest/en/goalie/summary"
params = {
    'isAggregate': 'false',
    'start': 0,
    'limit': 50,  # Adjust the page size as needed
    'factCayenneExp': 'gamesPlayed>20',
    'cayenneExp': 'gameTypeId=2 and seasonId>=20232024'
}

all_golies = []
# Pagination handling
while True:
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        players = data['data']
        all_golies.extend(players)

        if len(players) < params['limit']:
            break  # Exit the loop if last page

        params['start'] += params['limit']  # Prepare for next page
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        break

##--------------------------------------------------------------------------------------
## Save % leaders in the NHL

players_sorted = sorted(all_golies, key=lambda x: x['savePct'], reverse=True)

saveperct = None
player_count = 0
rank = 0
output_lines =[]
processed_players_highSV = set()
for player in players_sorted[:5]:
    if player['goalieFullName'] in processed_players_highSV:
        continue

    player_count += 1
    processed_players_highSV.add(player['goalieFullName'])

    if player['savePct'] != saveperct:
        rank = player_count
        saveperct = player['savePct']

    output_lines.append(f"{rank}. {player['goalieFullName']} ({player['teamAbbrevs']}), {player['savePct']}%, {player['gamesPlayed']} GP.")
output = "Save Percentage leaders in the NHL:\n\n" + "\n".join(output_lines)
# print(output)
payload = {"text": output}
response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
time.sleep(100)

##--------------------------------------------------------------------------------------
## worst save % over 20 GP

players_sorted = sorted(all_golies, key=lambda x: x['savePct'], reverse=False)

saveperct = None
player_count = 0
rank = 0
output_lines =[]
processed_players_lowSV = set()
for player in players_sorted[:5]:
    if player['goalieFullName'] in processed_players_lowSV:
        continue

    player_count += 1
    processed_players_lowSV.add(player['goalieFullName'])

    if player['savePct'] != saveperct:
        rank = player_count
        saveperct = player['savePct']

    output_lines.append(f"{rank}. {player['goalieFullName']} ({player['teamAbbrevs']}), {player['savePct']}%, {player['gamesPlayed']} GP.")
output = "Worst Save Percentage in the NHL(over 20 GP):\n\n" + "\n".join(output_lines)
# print(output)
payload = {"text": output}
response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
time.sleep(100)

#--------------------------------------------------------------------------------------

## Most wins in the NHL

players_sorted = sorted(all_golies, key=lambda x: x['wins'], reverse=True)

wins = None
player_count = 0
rank = 0
output_lines =[]
processed_players_highwin = set()
for player in players_sorted[:5]:
    if player['goalieFullName'] in processed_players_highwin:
        continue

    player_count += 1
    processed_players_highwin.add(player['goalieFullName'])

    if player['wins'] != wins:
        rank = player_count
        wins = player['wins']

    output_lines.append(f"{rank}. {player['goalieFullName']} ({player['teamAbbrevs']}), {player['wins']} wins, {player['gamesPlayed']} GP.")
output = "Most Wins in the NHL:\n\n" + "\n".join(output_lines)
# print(output)
payload = {"text": output}
response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
time.sleep(100)
##--------------------------------------------------------------------------------------
## NHL API endpoint and initial pagination parameters
url = "https://api.nhle.com/stats/rest/en/skater/summaryshooting"
params = {
    'isAggregate': 'false',
    'start': 0,
    'limit': 100,  # Adjust the page size as needed
    'factCayenneExp': 'gamesPlayed>30',
    'cayenneExp': 'gameTypeId=2 and seasonId>=20232024'
}

all_players = []
# Pagination handling
while True:
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        players = data['data']
        all_players.extend(players)

        if len(players) < params['limit']:
            break  # Exit the loop if last page

        params['start'] += params['limit']  # Prepare for next page
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        break

##--------------------------------------------------------------------------------------
## Shooting % leaders in the NHL


players_sorted = sorted(all_players, key=lambda x: x['satTotal'], reverse=True)

highshootingpct = None
player_count = 0
rank = 0
output_lines =[]
processed_players_highSAT = set()
for player in players_sorted[:5]:
    if player['skaterFullName'] in processed_players_highSAT:
        continue

    player_count += 1
    processed_players_highSAT.add(player['skaterFullName'])

    if player['satTotal'] != highshootingpct:
        rank = player_count
        highshootingpct = player['satTotal']

    output_lines.append(f"{rank}. {player['skaterFullName']} ({player['teamAbbrevs']}), +{player['satTotal']}, {player['gamesPlayed']} GP.")
output = "SAT/CORSI leaders in the NHL:\n\n" + "\n".join(output_lines)
# print(output)
payload = {"text": output}
response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
time.sleep(100)
##--------------------------------------------------------------------------------------

players_sorted = sorted(all_players, key=lambda x: x['satTotal'], reverse=False)

lowshootingpct = None
player_count = 0
rank = 0
output_lines =[]
processed_players_lowSAT = set()
for player in players_sorted[:5]:
    if player['skaterFullName'] in processed_players_lowSAT:
        continue

    player_count += 1
    processed_players_lowSAT.add(player['skaterFullName'])

    if player['satTotal'] != lowshootingpct:
        rank = player_count
        lowshootingpct = player['satTotal']

    output_lines.append(f"{rank}. {player['skaterFullName']} ({player['teamAbbrevs']}), {player['satTotal']}, {player['gamesPlayed']} GP.")
output = "Worst SAT/CORSI  in the NHL:\n\n" + "\n".join(output_lines)
# print(output)
# payload = {"text": output}
# response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
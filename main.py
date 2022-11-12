import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import matplotlib as mlp
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch


def get_data(match_id):
    base_url = 'https://understat.com/match/'
    url = base_url + match_id
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    scripts = soup.find_all('script')

    strings = scripts[1].string

    ind_start = strings.index("('") + 2
    ind_end = strings.index("')")
    json_data = strings[ind_start:ind_end]
    json_data = json_data.encode('utf8').decode('unicode_escape')
    return json.loads(json_data)


def append_data(shot_data, shot_event, team):
    shot_data['x_loc'].append((shot_event['X']))
    shot_data['y_loc'].append(shot_event['Y'])
    shot_data['xg'].append(shot_event['xG'])
    shot_data['team'].append(shot_event[f'{team}_team'])
    shot_data['player'].append(shot_event['player'])
    shot_data['minute'].append(shot_event['minute'])


def pitch_testing():
    text_color ='w'
    # Get data in data frame

    # Minute Second Team x y Outcome


def main():
    match_ids = ['18345','18346', '18347', '18351', '18344', '18343', '18342', '18348', '18350', '18349']
    shot_data = {
        'x_loc': [],
        'y_loc': [],
        'xg': [],
        'team': [],
        'player': [],
        'minute': [],   
    }

    for match_id in match_ids:
        data = get_data(match_id)
        # print(json_data)

        data_home = data['h']
        data_away = data['a']

        for shot_event in data_home:
            if shot_event['result'] == 'Goal':
                append_data(shot_data, shot_event, 'h')

        for shot_event in data_away:
            if shot_event['result'] == 'Goal':
                append_data(shot_data, shot_event, 'a')


    df = pd.DataFrame(shot_data)

main()

# https://www.youtube.com/watch?v=2RhTuRWNqUc&ab_channel=McKayJohns
# Check for video on pitches he mentions in intro
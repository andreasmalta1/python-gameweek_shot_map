import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import matplotlib as mlp
import matplotlib.pyplot as plt
from mplsoccer.pitch import VerticalPitch


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
    team_against = 'h'
    if team == 'h':
        team_against = 'a'
    
    shot_data['x_loc'].append(float(shot_event['X'])*120)
    shot_data['y_loc'].append(float(shot_event['Y'])*80)
    shot_data['xg'].append(float(shot_event['xG']))
    shot_data['team'].append(shot_event[f'{team}_team'])
    shot_data['team_against'].append(shot_event[f'{team_against}_team'])
    shot_data['player'].append(shot_event['player'])
    shot_data['minute'].append(shot_event['minute'])


def pitch_testing(df):
    text_color ='w'
    pitch = VerticalPitch(pitch_type='statsbomb', pitch_color='#22312B',
                            line_color='#C7D5CC', half=True)

    fig, ax = pitch.draw(figsize=(13, 8.5), constrained_layout=True, tight_layout=False)
    fig.set_facecolor('#22312B')
    ax.patch.set_facecolor('#22312B')

    print(df['x_loc'])
    print(df['y_loc'])
    print(df['player'])

    plt.gca().invert_yaxis()

    pitch.scatter(df['x_loc'], df['y_loc'], ax=ax, c='#EA6969', s=100, alpha=0.7)
    # For different colours for teams, use multiple plots
    # Check for size.
    # Check for annotation
    plt.title('Matchweek x Goals Represenatation')

    plt.show()


def main():
    match_ids = ['18345','18346', '18347', '18351', '18344', '18343', '18342', '18348', '18350', '18349']
    shot_data = {
        'x_loc': [],
        'y_loc': [],
        'xg': [],
        'team': [],
        'team_against': [],
        'player': [],
        'minute': [],   
    }

    for match_id in match_ids:
        data = get_data(match_id)

        data_home = data['h']
        data_away = data['a']

        for shot_event in data_home:
            if shot_event['result'] == 'Goal':
                append_data(shot_data, shot_event, 'h')

        for shot_event in data_away:
            if shot_event['result'] == 'Goal':
                append_data(shot_data, shot_event, 'a')

    df = pd.DataFrame(shot_data)
    pitch_testing(df)
    print(df.loc[df['xg'].idxmax()])

main()

# https://www.youtube.com/watch?v=2RhTuRWNqUc&ab_channel=McKayJohns
# Check for video on pitches he mentions in intro
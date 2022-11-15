import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import matplotlib as mlp
import matplotlib.pyplot as plt
from mplsoccer.pitch import VerticalPitch


def team_colours(col):
    primary_colour = {
        "Arsenal": "#EF0107",
        "Aston Villa": "#95BFE5",
        "Bournemouth": "#DA291C",
        "Brentford": "#E30613",
        "Brighton": "#0057B8",
        "Chelsea": "#034694",
        "Crystal Palace": "#1B458F",
        "Everton": "#003399",
        "Fulham": "#FFFFFF",
        "Leeds": "#FFCD00",
        "Leicester": "#003090",
        "Liverpool": "#C8102E",
        "Manchester City": "#6CABDD",
        "Manchester United": "#DA291C",
        "Nottingham Forest": "#E53233",
        "Newcastle United": "#241F20",
        "Southampton": "#D71920",
        "Tottenham": "#132257",
        "West Ham": "#7A263A",
        "Wolverhampton Wanderers": "#FDB913",
    }

    clr = []

    for team in col:
        if team in primary_colour:
            clr.append(primary_colour[team])
        else:
            print(team)
    return clr


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
    
    shot_data['x_loc'].append(float(shot_event['X'])*100)
    shot_data['y_loc'].append(float(shot_event['Y'])*80)
    shot_data['xg'].append(float(shot_event['xG']))
    shot_data['team'].append(shot_event[f'{team}_team'])
    shot_data['team_against'].append(shot_event[f'{team_against}_team'])
    shot_data['player'].append(shot_event['player'])
    shot_data['minute'].append(shot_event['minute'])


def pitch_testing(df):
    text_color ='w'
    pitch = VerticalPitch(pitch_type='custom', pitch_color='#22312B',
                          line_color='#C7D5CC', half=True,
                          pitch_length=100, pitch_width=80,
                          spot_scale=0.003)

    fig, ax = pitch.draw(figsize=(13, 8.5), constrained_layout=True, tight_layout=False)
    fig.set_facecolor('#22312B')
    ax.patch.set_facecolor('#22312B')

    pitch.scatter(df['x_loc'], df['y_loc'], color=team_colours(df["team"]), s=df['xg']*150, ax=ax)
    
    for index, row in df.iterrows():
        if row['xg'] > 0.77 or row['xg'] < 0.1:
            pitch.annotate(text=row['player'], xy=(row['x_loc'] + 0.5, row['y_loc'] + 2), ax=ax)
    
    plt.title('Matchweek 16 XG Representation')

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
    print(df)
    # print(df[df.xg == df.xg.max()])
    # print(df[df.xg == df.xg.min()])

main()

# https://www.youtube.com/watch?v=2RhTuRWNqUc&ab_channel=McKayJohns
# Own goals are not inlcuded as goals but misses

# Change point size accoridng to xg
# How can I make players more spread out?
# Add text box
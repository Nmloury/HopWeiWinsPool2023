# Imports
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from nba_api.stats import endpoints
import warnings

# Suppress SettingWithCopyWarning
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

# Initialize App
external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Create Team Owner Dict for wins pool
owner_map = {
    'Celtics': 'Eric',
    'Nuggets': 'Divya',
    'Mavericks': 'Divya',
    '76ers': 'Zach',
    'Warriors': 'Kent',
    'Bucks': 'Nehemiah',
    'Hawks': 'Eric',
    'Timberwolves': 'Nehemiah',
    'Pelicans': 'Divya',
    'Pacers': 'Richard',
    'Magic': 'Cuente',
    'Thunder': 'Nehemiah',
    'Cavaliers': 'Cuente',
    'Clippers': 'Zach',
    'Rockets': 'N/A',
    'Nets': 'Divya',
    'Knicks': 'Kent',
    'Spurs': 'Kent',
    'Lakers': 'Cuente',
    'Heat': 'Richard',
    'Suns': 'Richard',
    'Raptors': 'Nehemiah',
    'Bulls': 'Kent',
    'Trail Blazers': 'Eric',
    'Kings': 'Eric',
    'Hornets': 'Richard',
    'Jazz': 'Zach',
    'Pistons': 'Cuente',
    'Grizzlies': 'Zach',
    'Wizards': 'N/A'
}

# Create Team Owner Dict for wins pool...again
owner_map_2 = {
    'ATL': 'Eric',
    'BKN': 'Divya',
    'BOS': 'Eric',
    'CHA': 'Richard',
    'CHI': 'Kent',
    'CLE': 'Cuente',
    'DAL': 'Divya',
    'DEN': 'Divya',
    'DET': 'Cuente',
    'GSW': 'Kent',
    'HOU': 'N/A',
    'IND': 'Richard',
    'LAC': 'Zach',
    'LAL': 'Cuente',
    'MEM': 'Zach',
    'MIA': 'Richard',
    'MIL': 'Nehemiah',
    'MIN': 'Nehemiah',
    'NOP': 'Divya',
    'NYK': 'Kent',
    'OKC': 'Nehemiah',
    'ORL': 'Cuente',
    'PHI': 'Zach',
    'PHX': 'Richard',
    'POR': 'Eric',
    'SAC': 'Eric',
    'SAS': 'Kent',
    'TOR': 'Nehemiah',
    'UTA': 'Zach',
    'WAS': 'N/A'

}

# Create over/under Dict for wins pool
ou_map = {
    'Celtics': 54.5,
    'Nuggets': 52.5,
    'Mavericks': 45.5,
    '76ers': 48.5,
    'Warriors': 48.5,
    'Bucks': 54.5,
    'Hawks': 42.5,
    'Timberwolves': 44.5,
    'Pelicans': 44.5,
    'Pacers': 38.5,
    'Magic': 37.5,
    'Thunder': 44.5,
    'Cavaliers': 50.5,
    'Clippers': 46.5,
    'Rockets': 31.5,
    'Nets': 37.5,
    'Knicks': 45.5,
    'Spurs': 28.5,
    'Lakers': 47.5,
    'Heat': 45.5,
    'Suns': 51.5,
    'Raptors': 36.5,
    'Bulls': 37.5,
    'Trail Blazers': 28.5,
    'Kings': 44.5,
    'Hornets': 31.5,
    'Jazz': 35.5,
    'Pistons': 28.5,
    'Grizzlies': 45.5,
    'Wizards': 24.5
}

# Create color Dict for wins pool
color_map = {
    'Celtics': '#007A33',
    'Nuggets': '#0E2240',
    'Mavericks': '#00538C',
    '76ers': '#006BB6',
    'Warriors': '#1D428A',
    'Bucks': '#00471B',
    'Hawks': '#E03A3E',
    'Timberwolves': '#0C2340',
    'Pelicans': '#0C2340',
    'Pacers': '#002D62',
    'Magic': '#0077C0',
    'Thunder': '#007AC1',
    'Cavaliers': '#860038',
    'Clippers': '#C8102E',
    'Rockets': '#CE1141',
    'Nets': '#000000',
    'Knicks': '#F58426',
    'Spurs': '#C4CED4',
    'Lakers': '#552583',
    'Heat': '#98002E',
    'Suns': '#E56020',
    'Raptors': '#CE1141',
    'Bulls': '#CE1141',
    'Trail Blazers': '#E03A3E',
    'Kings': '#5A2D81',
    'Hornets': '#00788C',
    'Jazz': '#002B5C',
    'Pistons': '#C8102E',
    'Grizzlies': '#5D76A9',
    'Wizards': '#002B5C'
}

# Fetch NBA standings data
standings_full = endpoints.leaguestandings.LeagueStandings().get_data_frames()[0]

# Limit to relevant columns
col = ['TeamCity', 'TeamName', 'WINS', 'LOSSES']
standings = standings_full[col]

# Assign Wins Pool Owners
standings['Owner'] = standings['TeamName'].map(owner_map)

# Assign Wins Pool Owners
standings['O/U'] = standings['TeamName'].map(ou_map)

# Calculate Points Per Team
standings['Points'] = standings.apply(lambda row: row['WINS'] + 2 * max(row['WINS'] - row['O/U'], 0), axis=1)

# Drop Teams With No Owner
standings = standings[standings['Owner'] != 'N/A']

# Calculate Total Points Per Owner
total_points = standings.groupby(['Owner'])['Points'].sum().reset_index()
total_points.rename({'Points': 'TotalPoints'}, axis=1, inplace=True)
standings = standings.merge(total_points, on='Owner')

# Sort Standings
standings = standings.sort_values(by=['TotalPoints', 'Owner'], ascending=False)

gamelog_full = endpoints.LeagueGameLog().get_data_frames()[0]
gamelog = gamelog_full[['TEAM_ABBREVIATION', 'GAME_DATE', 'WL']]

# Assign Wins Pool Owners
gamelog['Owner'] = gamelog['TEAM_ABBREVIATION'].map(owner_map_2)

# Wins Boolean
gamelog['WinMask'] = gamelog['WL'] == 'W'

# Change to Dates
gamelog['GAME_DATE'] = pd.to_datetime(gamelog['GAME_DATE'])

# Drop Teams With No Owner
gamelog = gamelog[gamelog['Owner'] != 'N/A']

# Pivot to get cumulative points
gamelog_pivot = gamelog.pivot_table(index='GAME_DATE', columns='Owner', values='WinMask', aggfunc='sum').cumsum().reset_index()

# Fill NA
gamelog_pivot.fillna(method='ffill', inplace=True)
gamelog_pivot.fillna(0, inplace=True)

# Plots

# Stacked Point Bar Chart
fig1 = px.bar(standings,
              x='Owner',
              y='Points',
              color='TeamName',
              color_discrete_map=color_map,
              title='Wins Pool Points',
              barmode='stack',
              text='TeamName')

fig1.update_traces(texttemplate='%{text}', textposition='inside', showlegend=False)

for i, owner in enumerate(total_points['Owner']):
    total = total_points['TotalPoints'][i]
    fig1.add_annotation(x=owner, y=total, text=str(total),
                        showarrow=False, font=dict(color='black'), yshift=10)

# Season Long Points Chart
fig2 = px.line(gamelog_pivot,
               x='GAME_DATE',
               y=gamelog_pivot.columns[1:],
               title='Wins Pool Points By Date')

fig2.update_layout(xaxis_title='Date',
                   yaxis_title='Points',
                   legend={'title': {'text': 'Owner'}})

app.layout = html.Div(children=[
    html.H1(children='Hop Wei NBA Wins Pool 2023-2024', style={'textAlign': 'center'}),

    html.H2(children='NBA Wins Pool Rules'),

    dcc.Markdown('''
    - Winner - highest point total at the conclusion of the NBA Finals
    - $10 Buy-in -> $15 to Regular Season Winner, $55 to Overall Winner, $10 to 2nd Place
    - 1 Trade per team, at conclusion of the trade, you inherit past performance of the team as well (Trade Deadline is 24 hours BEFORE NBA Trade Deadline!)
    - No waiver wire or team swapping allowed (there will be 2 leftover teams)
    '''),

    html.H2(children='Scoring System'),

    html.H3(children='Regular Season'),

    dcc.Markdown('''
    - 1 Point per Win
    - 2 Points per Win above the Spread
    - In-season Tourney Finals winner = 3 Points (to be added at an end of regular season)
    '''),

    html.H3(children='Post-Season'),

    dcc.Markdown('''
    - Managers can wager their regular season points on each playoff series
    - Must have a 5 point minimum bet on each series
    - Max bet until conference finals 12 points
    - Conference Finals and Finals max bet is 20 points per series
    '''),

    dcc.Graph(
        id='stacked-bar-graph',
        figure=fig1
    ),

    dcc.Graph(
        id='example-graph',
        figure=fig2
    )
])

if __name__ == '__main__':
    app.run(debug=True)

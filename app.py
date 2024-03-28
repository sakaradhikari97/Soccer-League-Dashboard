#Name: Sakar Adhikari Andrew id: sakara Subject Code: 12780-A2   Final Poject Code
#Importing the relevant libraries
from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from plotly.utils import PlotlyJSONEncoder

#initializing the flask app
app = Flask(__name__)

# Loading the dataset and calculating the points 
file_path = '/Users/sakaradhikari/Desktop/stats.csv'
df = pd.read_csv(file_path) #reading data from csv
df['points'] = df['wins'] * 3 #calculating points 

@app.route('/', methods=['GET', 'POST']) #defining the route for main page
def index():
    seasons = df['season'].unique() #getting unique season
    selected_season = request.form.get('season') if request.method == 'POST' else seasons[0]  #asking user to select the season 

    # data visualization for top teams
    top_teams = df[df['season'] == selected_season].sort_values(by='points', ascending=False).head(10)
    fig_top_teams = px.bar(top_teams, x='team', y='points', title=f'Top Teams in {selected_season}') #creating bar chat for top team
    graphJSON_top_teams = json.dumps(fig_top_teams, cls=PlotlyJSONEncoder) #chaning plotly into jason for rendering in HTML

    # Preparing data for goals scored visualization
    fig_goals_scatter = px.scatter(top_teams, x='team', y='goals', title=f'Goals Scored in {selected_season}', color='goals',
                                   color_continuous_scale='Viridis', labels={'goals': 'Goals Scored'})
    graphJSON_goals_scatter = json.dumps(fig_goals_scatter, cls=PlotlyJSONEncoder) #converting scatter plot to json

    return render_template('index.html', seasons=seasons, selected_season=selected_season,
                           graphJSON_top_teams=graphJSON_top_teams, graphJSON_goals=graphJSON_goals_scatter)

@app.route('/team_analysis', methods=['GET', 'POST']) #defining route for team analysis
def team_analysis():
    teams = df['team'].unique()
    seasons = df['season'].unique()
    selected_team = request.form.get('team') if request.method == 'POST' else teams[0] #select the team 
    selected_season = request.form.get('season') if request.method == 'POST' else seasons[0]

    # Team performance analysis with radar chart
    team_data = df[(df['team'] == selected_team) & (df['season'] == selected_season)].iloc[0]
    categories = ['wins', 'losses', 'goals', 'clean_sheet']
    values = [team_data[metric] for metric in categories]

    #radar chart for team performance 
    fig_radar = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself'))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False)
    graphJSON_radar = json.dumps(fig_radar, cls=PlotlyJSONEncoder)

    # finding relationship between total_pass and goals scored using scatter plot
    team_history = df[df['team'] == selected_team]
    fig_pass_goals_scatter = px.scatter(team_history, x='total_pass', y='goals', color='season',
                                        title=f'Relationship between Total Pass and Goals Scored for {selected_team}')
    graphJSON_pass_goals_scatter = json.dumps(fig_pass_goals_scatter, cls=PlotlyJSONEncoder)

    return render_template('team_analysis.html', teams=teams, seasons=seasons,
                           selected_team=selected_team, selected_season=selected_season,
                           graphJSON_radar=graphJSON_radar, graphJSON_pass_goals_scatter=graphJSON_pass_goals_scatter)

if __name__ == '__main__':
    app.run(debug=True) #running flask app in debug mode
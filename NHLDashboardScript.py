#imports
import pandas as pd
import numpy as np
import panel as pn
import hvplot.pandas
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import ipywidgets as widgets
from IPython.display import display
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.io import curdoc
from bokeh.transform import linear_cmap
from bokeh.palettes import Viridis256
from bokeh.models import ColumnDataSource, Select
from bokeh.models import Range1d





firstOveralls = pd.read_csv('data/first_overalls.csv')
firstOverallsPlayerData = pd.read_csv('data/first_overalls_player_data.csv')
nhlDraftData = pd.read_csv('data/nhl_draft_data.csv')
nhlPlayerData = pd.read_csv('data/nhl_player_data_2000-2020.csv')
playsGoal = pd.read_csv('data/playsGoalWithFOInfo.csv')

#Make dataframe pipeline interactive
#thin playsGoal to only include columns we want to use(xCoord, yCoord, scoringPlayerId, playerName)
# Make a copy of the slice
cordToGoals = playsGoal[['xCoord', 'yCoord', 'scoringPlayerId', 'playerName']].copy()

# Find rows where xCoord is negative
negative_xCoord = cordToGoals['xCoord'] < 0

# Invert yCoord for these rows
cordToGoals.loc[negative_xCoord, 'yCoord'] = cordToGoals.loc[negative_xCoord, 'yCoord'] * -1

# Make xCoord positive only
cordToGoals['xCoord'] = cordToGoals['xCoord'].abs()



# Assuming df is your DataFrame and it has columns 'xCoord', 'yCoord', and 'playerName'

# Create a ColumnDataSource
source = ColumnDataSource(data=dict(x=[], y=[]))

# Remove NaN values
cordToGoals = cordToGoals.dropna(subset=['playerName'])

# Create a dropdown menu
menu = Select(options=sorted(list(cordToGoals['playerName'].unique())), value=cordToGoals['playerName'].unique()[0], title='Player')

# Create a figure
p = figure(height=600, width=600, title="", toolbar_location=None)

# Assuming the image is located at 'path_to_image'
image_url = 'Half_ice_hockey_rink.png'

# Set the x_range and y_range to match the image dimensions
p.x_range=Range1d(0, 1)
p.y_range=Range1d(0, 1)

# Add the image
p.image_url(url=[image_url], x=0, y=0, w=1, h=1)

# Create a scatter plot
p.circle(x="x", y="y", source=source, size=5, color=linear_cmap('y', Viridis256, -1, 1))

# Create a dropdown menu
menu = Select(options=list(cordToGoals['playerName'].unique()), value=cordToGoals['playerName'].unique()[0], title='Player')

# Callback function to update the plot
def update():
    player = menu.value
    df_player = cordToGoals[cordToGoals['playerName'] == player]
    source.data = dict(
        x=df_player['xCoord'],
        y=df_player['yCoord']
    )

# Update the plot when the dropdown value changes
menu.on_change('value', lambda attr, old, new: update())

# Layout
layout = column(menu, p)

# Update the plot for the initial player
update()

# Add the layout to the current document
curdoc().add_root(layout)
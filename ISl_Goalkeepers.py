# Data Manipulation libraries:
import streamlit as st
import stlabels
import io
import pandas as pd
from copy import deepcopy
from sklearn.preprocessing import MinMaxScaler

# Plotting libraries:
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Determining the filepath
filepath = 'isl_player_final.csv'

# reading the CSV file
isl_df = pd.read_csv(filepath)

# we just need Goalkeepers for this so we will store them in a variable as there is position ID assigned
gk_df = isl_df[isl_df["position_id"] == 4]

# numerical exploration using group by
clean_sheets = gk_df.groupby(["short_name","tour_name"])["events.cleansheet"].sum()

def clean_sheets_stats(gk_df):
    fig = px.bar(x="short_name", y="events.cleansheet", barmode="group", data_frame=gk_df,
                 color="tour_name", text="events.cleansheet", title="No. of Cleansheets (per season)",
                 labels={"short_name": "", "events.cleansheet": "", "tour_name": "Tour"},
                 color_discrete_map={"ISL 6": "#00FE35", "ISL 7": "#ff9933"})

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to black
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set plot paper color to black
        font_color='white',  # Set font color to white
        width=1000,  # Adjust width as needed
        margin=dict(l=50, r=50, t=50, b=50),  # Adjust margins as needed
        xaxis=dict(
            showgrid=True,  # Show gridlines on x-axis
            gridcolor='rgba(255, 255, 255, 0.5)',  # Set gridline color to white with transparency
            gridwidth=2,  # Set gridline width
            showline=True,  # Show x-axis line
            linecolor='rgba(255, 255, 255, 0.5)',  # Set x-axis line color to white with transparency
            linewidth=2,  # Set x-axis line width
            tickfont=dict(color='white'),  # Set tick font color to white
            title=dict(text='Player', font=dict(color='white'))  # Set x-axis title and color
        ),
        yaxis=dict(
            showgrid=True,  # Show gridlines on y-axis
            gridcolor='rgba(255, 255, 255, 0.5)',  # Set gridline color to white with transparency
            gridwidth=2,  # Set gridline width
            showline=True,  # Show y-axis line
            linecolor='rgba(255, 255, 255, 0.5)',  # Set y-axis line color to white with transparency
            linewidth=2,  # Set y-axis line width
            tickfont=dict(color='white'),  # Set tick font color to white
            title=dict(text='Number of Clean Sheets', font=dict(color='white'))  # Set y-axis title and color
        )
    )

    return fig

# Assuming gk_df is your DataFrame containing goalkeeper statistics
# Call the function to generate and display the plot
clean_sheets_plot = clean_sheets_stats(gk_df)
st.plotly_chart(clean_sheets_plot)




















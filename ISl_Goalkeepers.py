# Data Manipulation libraries:
import streamlit as st

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


# Because of wrong analyses we need to declutter the plot as some of the players only played one season.
# Now we will take the GKs which have played more than 180 minutes to get the right data using "deepcopy"
# We will analyze goals conceded per minutes played.

gk_df_mins_df = deepcopy(gk_df[gk_df["actual_minutes_played"] > 180])

# we will create a side by side comparison using subplots
def goals_conc(gk_df_mins_df):
    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.1,
                        subplot_titles=("Goals Conceded (per season", "Mins Played (per season)"))
    fig.add_trace(go.Bar(x=gk_df_mins_df["short_name"],
                         y=gk_df_mins_df["events.goals_conceded"],
                         text=gk_df_mins_df["events.goals_conceded"],
                         textposition="inside",
                         marker_color=px.colors.qualitative.Plotly[0],  # Using first color from Plotly color palette
                         name="Total Conceded"),
                  row=1, col=1)
    fig.add_trace(go.Bar(x=gk_df_mins_df["short_name"],
                         y=gk_df_mins_df["actual_minutes_played"],
                         text=gk_df_mins_df["actual_minutes_played"],
                         textposition="inside",
                         marker_color=px.colors.qualitative.Plotly[1],  # Using second color from Plotly color palette
                         insidetextfont={"color": "white"},
                         name="Total Minutes"),
                  row=2, col=1)

    # Set plot properties to match clean_sheets_plot
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
            title=dict(text='Number of Goals Conceded', font=dict(color='white'))  # Set y-axis title and color
        )
    )

    return fig

# Considering only players who have played atleast 900 mins (punches vs catches)
gk_df_mins_df = deepcopy(gk_df_mins_df[gk_df_mins_df["actual_minutes_played"] > 180])
gk_df_mins_df["events.catchesPer90"] = gk_df_mins_df["events.catches"].divide(gk_df_mins_df["actual_minutes_played"]).multiply(90)
gk_df_mins_df["events.punchesPer90"] = gk_df_mins_df["events.punches"].divide(gk_df_mins_df["actual_minutes_played"]).multiply(90)
gk_df_mins_df["goaltenders.savesPer90"] = gk_df_mins_df["goaltenders.saves"].divide(gk_df_mins_df["actual_minutes_played"]).multiply(90)
gk_df_mins_df["events.cleansheetPer90"] = gk_df_mins_df["events.cleansheet"].divide(gk_df_mins_df["actual_minutes_played"]).multiply(90)

# Assigning variables for ease
markerSize = "goaltenders.savesPer90"
markerColor = "events.cleansheetPer90"
x_col = "events.punchesPer90"
y_col = "events.catchesPer90"
hoverName = "team_short_name"
markerLabelText = "short_name"
markerSymbol="tour_name"


def played_900(gk_df_mins_df):
    fig = px.scatter(y=y_col, x=x_col, data_frame=gk_df_mins_df,
                     size=markerSize, color=markerColor, opacity=.8,
                     hover_name=hoverName, text=markerLabelText, symbol=markerSymbol,
                     labels={y_col: "Catches", x_col: "Punches", markerSymbol: "tour"},
                     color_continuous_scale=["#ff4500", "#39ff14", "#800080"])  # Neon red, neon green, and purple

    # Add average lines for punches and catches:
    fig.add_trace(go.Scatter(x=gk_df_mins_df[x_col],
                             y=[gk_df_mins_df[y_col].mean()] * len(gk_df_mins_df),
                             name="Avg. catches"))
    fig.add_trace(go.Scatter(x=[gk_df_mins_df[x_col].mean()] * len(gk_df_mins_df),
                             y=gk_df_mins_df[y_col],
                             name="Avg. punches"))

    # Annotations for each quadrant
    # Right top quadrant #
    fig.add_annotation(x=gk_df_mins_df[x_col].max(),
                       y=gk_df_mins_df[y_col].max(),
                       text="High Punch-Catch Zone",
                       showarrow=False, xshift=-150, yshift=-50, font={"size": 20})
    # Right bottom quadrant #
    fig.add_annotation(x=gk_df_mins_df[x_col].max(),
                       y=gk_df_mins_df[y_col].min(),
                       text="High Punch Low Catch Zone",
                       showarrow=False, xshift=-150, font={"size": 20})
    # Left bottom quadrant #
    fig.add_annotation(x=gk_df_mins_df[x_col].min(),
                       y=gk_df_mins_df[y_col].min(),
                       text="Low Punch-Catch Zone",
                       showarrow=False, xshift=150, font={"size": 20})
    # Left top quadrant #
    fig.add_annotation(x=gk_df_mins_df[x_col].min(),
                       y=gk_df_mins_df[y_col].max(),
                       text="Low Punch High Catch Zone",
                       showarrow=False, xshift=150, yshift=-50, font={"size": 20})

    # Additional plot parameters:
    fig.update_traces(textposition='top center', textfont_size=10, marker_line_width=0)  # Remove outlines on shapes
    fig.update_layout(showlegend=False, height=600, width=1000, coloraxis_colorbar=dict(title='Tour'))  # Adjusted height and width, added colorbar title
    return fig

#These are the columns i extracted to get per90 stats.
per90Cols = ['actual_minutes_played', 'events.punches', 'events.catches', 'events.goals_conceded', 'events.cleansheet',
             'touches.total', 'goaltenders.shots_faced', 'goaltenders.goals_allowed', 'goaltenders.saves', 'goaltenders.catches']

id_names_df = gk_df_mins_df.groupby(["id"]).agg({"short_name": "first"})
radar_cols_df = gk_df_mins_df.groupby(["id"])[per90Cols].sum()

final_df_for_radar = pd.concat([id_names_df, radar_cols_df], axis=1)
final_df_for_radar.reset_index(inplace=True)

per90Cols.remove('actual_minutes_played')


for col in per90Cols:
    final_df_for_radar[col + "Per90"] = final_df_for_radar[col].divide(final_df_for_radar["actual_minutes_played"]).multiply(90)

cols_for_radar = [i + "Per90" for i in per90Cols]
print(cols_for_radar)

scaler = MinMaxScaler()
final_df_for_radar[cols_for_radar] = scaler.fit_transform(final_df_for_radar[cols_for_radar])

isl_max = final_df_for_radar[cols_for_radar].max().max()
print(isl_max)


# Creating Function to plot Polar graphs using already extracted ID's

def Max_polar(final_df, player_names):
    player_ids = []
    for player_name in player_names:
        # Find player ID based on player name
        player_id = final_df.loc[final_df["short_name"] == player_name, "id"]
        if not player_id.empty:
            player_ids.append(player_id.item())

    if player_ids:
        # Calculate the number of rows based on the number of selected players
        num_rows = (len(player_ids) + 1) // 2  # Round up to the nearest integer
        specs = [[{"type": "polar"}] * 2] * num_rows  # Two plots per row

        fig = make_subplots(rows=num_rows, cols=2, subplot_titles=player_names, specs=specs)

        for i, player_id in enumerate(player_ids):
            row = i // 2 + 1
            col = i % 2 + 1
            fig.add_trace(px.line_polar(final_df,
                                        r=final_df.loc[final_df["id"] == player_id, cols_for_radar].values.flatten(),
                                        theta=cols_for_radar, line_close=True).data[0],
                          row=row, col=col)
            fig.update_traces(fill='toself')

            # Additional properties for the plot:
            fig.update_layout(showlegend=False)

        return fig
    else:
        return None












# User Interface layout starts here

st.set_page_config(layout="wide")


col1, col2 = st.columns([1, 3])
with col1:
    st.image("isl_logo.jpg", width=200)
with col2:
    st.markdown(
        "<span style='color: #39ff14; font-size: 48px; font-weight: bold; font-family: Arial, sans-serif;'>ISL GOALKEEPER ANALYSIS</span>",
        unsafe_allow_html=True)
    st.subheader("Analyzing the top rated Goalkeepers in ISL for scouting.")

st.write("")

col3, empty_col, col4 = st.columns([3, 1, 1.5])

with col3:
    content1 = """ **1. Lets start by comparing the No. of cleans sheets of the Goalkeepers in Two 
    consecutive seasons of ISL 2016 and 2017.** """
    st.info(content1)
    clean_sheets_plot = clean_sheets_stats(gk_df)
    st.plotly_chart(clean_sheets_plot)

    st.write("")

    content2 = """**2.  As the Plot for number of clean sheets was a good starting point, I think
    it would be a better idea two declutter the graph and take into consideration the players who have played 
    more than 180 minutes in two consecutive seasons. Clean sheets is a great way to see GK performance but a better 
    way would be too see sub plots of Goals conceded per season with minutes played**"""
    st.info(content2)

    st.write("")
    goals_conceded_plot = goals_conc(gk_df_mins_df)
    st.plotly_chart(goals_conceded_plot)

    st.write("")
    content3 = """**3. Now that we have a good understanding of the macro aspects of the statistics of our GK's which is based on How they performed in the matches in two 
     consecutive seasons, now i think to figure out the individual capabilities we need to understand the best attributes of the GK's. 
     The below graph shows 4 quadrants with zones for Catches Vs Punches and their individual stats for those zones**"""
    st.info(content3)
    punches_vs_catches_plot = played_900(gk_df_mins_df)
    st.plotly_chart(punches_vs_catches_plot)

    st.write("")
    content4 ="""4. For the last comparison i think the best way to compare all Goalkeepers is using a Polar Plot which is the best way to actually differentiate between the Game stats"""
    st.info(content4)
    selected_players = st.multiselect("Select players:", final_df_for_radar["short_name"],
                                      default=[final_df_for_radar.iloc[0]["short_name"]])

    # Call the Max_polar function with the DataFrame and the player name input
    if selected_players:
        radar_fig = Max_polar(final_df_for_radar, selected_players)
        if radar_fig:
            st.plotly_chart(radar_fig)
        else:
            st.write("Player not found!")
with col4:
    st.markdown("<span style='color: #ff4500; font-size: 24px;'>KEY TAKEAWAY AND ANALYSIS</span>",
                unsafe_allow_html=True)
    st.markdown("<span style='color: #39ff14;'>1. Insight:</span> Most Goalkeepers had more clean-sheets\nin 2017 making the season low scoring."
                "Also,some of the GK's did not play in 2016 making the analysis skewed", unsafe_allow_html=True)
    st.markdown("<span style='color: #39ff14;'>2. Analysis:</span> Looking at the Graph you can find 3 keepers had same amount of clean sheets "
                "which includes Amrinder Singh, Arindam B. and Phurba L which is = 10.", unsafe_allow_html=True)
    st.markdown("<span style='color: #39ff14;'>3. Key Takeaway:</span> If we compare the top 3 candidates, It is safe to say the best performer would be Arindam B. as "
                "he had 17 cleansheets, making it more than most of the players combined.", unsafe_allow_html=True)

    st.title("")
    st.title("")
    st.title("")
    st.title("")
    st.title("")
    st.title("")
    st.title("")

    st.markdown("<span style='color: #ff4500; font-size: 24px;'>KEY TAKEAWAYS AND ANALYSIS</span>",
                unsafe_allow_html=True)
    st.markdown(
        "<span style='color: #39ff14;'>1. Insight:</span> To scout the best GK's from the group we need to find the Goalie's "
        "which played the most minutes and conceded the least amount of goals.", unsafe_allow_html=True)
    st.markdown(
        "<span style='color: #39ff14;'>2. Analysis:</span> Now as we can see Amrinder S. , Arindam B, Gurpreet Singh and Vishal K "
        "had the most minutes played but it safe to say if we had to pick the top 3 out of them we need to eliminate Vishal K as "
        "he conceded the most amount of goals. Arindam B leads the charts as he conceded the least amount of goals and played the most minutes compared to any other Goalie", unsafe_allow_html=True)
    st.markdown(
        "<span style='color: #39ff14;'>3. Key Takeaway:</span> It's best to use these stats for filtering the top GK's but we also need to consider the defensive team players of these GK's "
        "before making any conclusions but still these stats put a lot of weight to understand the best GK performences.", unsafe_allow_html=True)

    st.title("")
    st.title("")
    st.title("")
    st.title("")
    st.title("")
    st.title("")


    st.markdown("<span style='color: #ff4500; font-size: 24px;'>KEY TAKEAWAYS AND ANALYSIS</span>",
                unsafe_allow_html=True)
    st.markdown(
        "<span style='color: #39ff14;'>1. Insight:</span> Now as we can see how the Goalkeepers have performed on the basis of the zones we"
        "are able to identify the probability of catches and punches on the basis of zones", unsafe_allow_html=True)
    st.markdown(
        "<span style='color: #39ff14;'>2. Analysis:</span> Goalkeepers generally who have the ability to catch more and punch less are rated superior to the other "
        "GK's and it makes sense because the teams ability to have less threat and more chance of possession increases with that.So based on individual ability"
        "we are able to see that our top three candidates are in three different quadrants. Where Gurpreet S. stands in the High Punch High Catch zone. "
        "So according to the Analysis, Arindam B who was the best performing GK prefers more punches than catches. ", unsafe_allow_html=True)
    st.markdown(
        "<span style='color: #39ff14;'>3. Key Takeaway:</span> I think there is reason Gurpreet Sigh Sandhu makes the starting team for Indian National Football as "
        "he has the most punches and catches cobined with good amount of clean sheets as well.", unsafe_allow_html=True)

    st.title("")
    st.title("")
    st.title("")
    st.title("")
    st.title("")
    st.title("")









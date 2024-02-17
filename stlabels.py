import streamlit as st
import ISl_Goalkeepers

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
    content1 = """ **1. Lets start by comparing the cleans sheets of the Goalkeepers in Two 
    consecutive seasons of ISL 2016 and 2017.** """
    st.info(content1)
    clean_sheets_plot = ISl_Goalkeepers.clean_sheets_stats(ISl_Goalkeepers.gk_df)
    st.plotly_chart(clean_sheets_plot)

with col4:
    st.markdown("<span style='color: #ff4500; font-size: 24px;'>KEY TAKEAWAYS AND ANALYSIS</span>",
                unsafe_allow_html=True)
    st.markdown("<span style='color: #39ff14;'>1. Insight:</span> Most Goalkeepers had more clean-sheets\nin 2017 making the season low scoring."
                "Also,some of the GK's did not play in 2016 making the analysis skewed", unsafe_allow_html=True)
    st.markdown("<span style='color: #39ff14;'>2. Analysis:</span> Looking at the Graph you can find 3 keepers had same amount of clean sheets "
                "which includes Amrinder Singh, Arindam B. and Phurba L which is = 10.", unsafe_allow_html=True)
    st.markdown("<span style='color: #39ff14;'>3. Key Takeaway:</span> If we compare the top 3 candidates, It is safe to say the best performer would be Arindam B. as "
                "he had 17 cleansheets, making it more than most of the players combined.", unsafe_allow_html=True)





















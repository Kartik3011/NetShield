import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests
import altair as alt
import os

# STREAMLIT PAGE CONFIG
st.set_page_config(page_title="Social Content Report", layout="wide", initial_sidebar_state="expanded")

# CSS FOR NETSHIELD LOGO AND UI STYLING
st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem !important; 
            padding-bottom: 0rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        [data-testid="stSidebar"] {
            background-color: #1f2937;
            color: white;
        }
        [data-testid="stSidebar"]::before {
            content: "NetShield 🛡️";
            display: block;
            font-size: 26px;
            font-weight: bold;
            color: #ffffff;
            text-align: left;
            padding: 20px 0 10px 20px;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            margin-bottom: 10px;
        }
        [data-testid="stSidebar"]::after {
            content: "Use the sidebar to navigate through NetShield features.";
            position: absolute;
            bottom: 10px; 
            left: 0;
            right: 0;
            padding: 10px 15px;
            text-align: center;
            font-size: 14px;
            color: rgba(255, 255, 255, 0.5); 
            z-index: 10000;
        }
        .description-box {
            background-color: #262626;
            padding: 15px;
            border-radius: 5px;
            border-left: 5px solid #3498db;
            margin-bottom: 30px;
        }
        .bottom-note-box {
            margin-top: 20px; 
            margin-bottom: 40px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Social Content Report")

st.markdown("""
    <div class="description-box">
              <strong style="font-size: 16px; margin-left: 10px; display: block;">Report Overview:</strong> 
       <ul style="font-size: 16px; margin: 0; color: #fff; padding-left: 20px;">
    <li>This page provides a comprehensive report based on the data fetched from YouTube.</li>
    <li>Please see the filters to analyze video view trends across selected channels.</li>
</ul>
    </div>
""", unsafe_allow_html=True)

# ROBUST DATA LOADING LOGIC
def load_data():
    """Loads the video data CSV, checking both session memory and physical disk."""
    # 1. Check session state memory first
    if 'video_data_df' in st.session_state and st.session_state['video_data_df'] is not None:
        if not st.session_state['video_data_df'].empty:
            return st.session_state['video_data_df']
        
    # 2. Check physical disk with direct pathing
    # We use a simple filename first as it's most reliable in Streamlit Cloud root dirs
    file_name = "video_data.csv"
    
    if os.path.exists(file_name):
        try:
            df = pd.read_csv(file_name)
            # Cache it back to session state for the current session
            st.session_state['video_data_df'] = df
            return df
        except Exception as e:
            st.error(f"Error reading {file_name}: {e}")
            return pd.DataFrame()
    
    # 3. Fallback to full path check if simple name fails
    full_path = os.path.join(os.getcwd(), file_name)
    if os.path.exists(full_path):
        return pd.read_csv(full_path)

    return pd.DataFrame()

# LOAD DATA
df = load_data()

if df.empty:
    st.error("⚠️ Error: 'video_data.csv' not found. Please go back to the 'Request Analysis' page and click 'Fetch Data'.")
    st.info("If you just fetched data, try refreshing the page (F5) to clear the browser cache.")
    st.stop()

# RAW DATA DISPLAY
st.subheader("Raw Data Table")
st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("---")

# VIEW TREND ANALYSIS
try:
    if "Published At" not in df.columns or "Views" not in df.columns:
        st.error("The dataset is missing required columns: 'Published At' or 'Views'.")
    else:
        df["Published At"] = pd.to_datetime(df["Published At"])
        st.subheader("Video View Trend Analysis")
        
        channels = st.multiselect("Select Channels to filter the chart:", df["Channel Title"].unique(), [])

        df_filtered = df
        if channels:
            df_filtered = df[df["Channel Title"].isin(channels)]

        if df_filtered.empty:
            st.warning("No data available for the selected channels.")
        else:
            plot_data = df_filtered.groupby(df_filtered["Published At"].dt.date)["Views"].sum().reset_index()
            plot_data["Published At"] = pd.to_datetime(plot_data["Published At"])

            chart = (
                alt.Chart(plot_data)
                .mark_line(color="#28a745", size=3) 
                .encode(
                    x=alt.X("Published At:T", title="Published Date"),
                    y=alt.Y("Views:Q", title="Total Views"),
                    tooltip=["Published At:T", "Views:Q"]
                )
                .properties(title="Views Over Time for Published Videos")
                .interactive()
            )
            st.altair_chart(chart, use_container_width=True)

            st.markdown(
                "<p style='font-size: 14px; color: #888888; text-align: center;'>⚠️ Trends may not appear if the data set is very small or videos share the same date.</p>", 
                unsafe_allow_html=True
            )

except Exception as e:
    st.error(f"An error occurred while generating trends: {e}")

st.markdown(
    """
    <div class="bottom-note-box" style="background-color: #262626; padding: 15px; border-radius: 5px; border-left: 5px solid #28a745;">
      <ul style="font-size: 16px; margin: 0; color: #fff; padding-left: 20px; list-style-type: disc;">
       <strong>NOTE:</strong> 
        <li>This report displays raw data returned by the YouTube API.</li>
        <li>AI-powered filtering and misinformation detection (Green/Yellow/Red status) is performed in the <strong>AUTOMATE</strong> section.</li>
    </ul>
    </div>
    """, 
    unsafe_allow_html=True
)

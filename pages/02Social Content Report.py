import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

import requests
import altair as alt
import os


st.set_page_config(page_title="Social Content Report", layout="wide", initial_sidebar_state="expanded")



st.markdown("""
    <style>
        /* 1. GAP REDUCTION: Main content block padding */
        .block-container {
            padding-top: 0rem !important; /* REDUCES GAP ABOVE TITLE */
            padding-bottom: 0rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }

        /* 2. SIDEBAR BACKGROUND */
        [data-testid="stSidebar"] {
            background-color: #1f2937; /* Dark background */
            color: white;
        }

        /* 3. FIXED LOGO INJECTION (Top Left Sidebar) */
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
        
        /* 4. SIDEBAR FOOTER (Navigation Text at Bottom) */
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
        
        /* Custom style for the description box */
        .description-box {
            background-color: #262626; /* Very light blue background */
            padding: 15px;
            border-radius: 5px;
            border-left: 5px solid #3498db; /* Blue accent color */
            margin-bottom: 30px; /* Space after the description box */
        }
        
        /* Custom style for the note box at the bottom */
        .bottom-note-box {
            /* Reduced margin-top for less space between graph and note */
            margin-top: 20px; 
            margin-bottom: 40px; /* Increased space after the note box */
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <div style="display: none;">
        NetShield🛡️
    </div>
""", unsafe_allow_html=True)



st.title("Social Content Report")

# -  BOXED DESCRIPTION AT THE TOp OF THE PAGE -
st.markdown("""
    <div class="description-box">
              <strong style="font-size: 16px; margin-left: 10px; display: block;">Report Overview:</strong> 
       <ul style="font-size: 16px; margin: 0; color: #fff; padding-left: 20px;">
    <li>
        This page provides a comprehensive report based on the data fetched from YouTube. The raw dataset is displayed below for initial inspection.
    </li>
    <li>
        Please see the filters to analyze video view trends across selected channels. 
    </li>
    
</ul>
    </div>
""", unsafe_allow_html=True)
# --------


@st.cache_data
def load_data():
    """Loads the video data CSV, handling file not found errors."""
    if 'video_data_df' in st.session_state and not st.session_state['video_data_df'].empty:
        # Load from memory, bypassing the need for immediate disk access
        return st.session_state['video_data_df']
        
    file_path = os.path.join(os.getcwd(), "video_data.csv") 
    
    # Check if the file exists before attempting to read
    if not os.path.exists(file_path):
        st.error(f"Error: Data file not found at {file_path}. Please go back and run the data fetching step.")
        return pd.DataFrame() # Return empty DataFrame on error
        
    return pd.read_csv(file_path)


df = load_data()

st.subheader("Raw Data Table")

# Use the highly readable st.dataframe for the table

st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("---")


try:
    if df.empty:
         
         # Skip the rest of the chart logic if the DataFrame is empty

         pass 
    elif "Published At" not in df.columns or "Views" not in df.columns:
        st.error("The dataset must contain 'Published At' and 'Views' columns.")
    else:

        # Data processing and selection

        df["Published At"] = pd.to_datetime(df["Published At"])
        
        st.subheader("Video View Trend Analysis")
        
        channels = st.multiselect("Select Channels to filter the chart:", df["Channel Title"].unique(), [])

        df_filtered = df
        if channels:
            df_filtered = df[df["Channel Title"].isin(channels)]

        if df_filtered.empty:
            st.warning("No data available for the selected channels.")
        else:

            # Chart generation

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
                .properties(
                    title="Views Over Time for Published Videos"
                )
                .interactive()
            )
            st.altair_chart(chart, use_container_width=True)

            st.markdown(
                "<p style='font-size: 14px; color: #888888; text-align: center;'>⚠️ The chart may not display trends if the data set of selected videos is very small or if they were published on the same day/recently.</p>", 
                unsafe_allow_html=True
            )

except Exception as e:
    st.error(f"An error occurred: {e}")



st.markdown(
    """
    <div class="bottom-note-box" style="background-color: #262626; padding: 15px; border-radius: 5px; border-left: 5px solid #28a745;">
      <ul style="font-size: 16px; margin: 0; color: #fff; padding-left: 20px; list-style-type: disc;">
       <strong>NOTE:</strong> 
        <li>
            This report displays all videos returned by the YouTube API for the broad search query.  It often includes videos with misleading tags (junk content).
        </li>
        <li>
            The process of <strong>AI-powered filtering and misinformation detection (Green/Yellow/Red status)</strong> is performed in the <strong>AUTOMATE</strong> section.
        </li>
    </ul>
    </div>
    """, 
    unsafe_allow_html=True
)


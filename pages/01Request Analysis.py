import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from module import yextractor as youtube
import requests
import os



def get_coordinates(city_name):
    """Fetch latitude and longitude for a given city name."""
    url = f'https://nominatim.openstreetmap.org/search?city={city_name}&format=json'
    headers = {
        'User-Agent': 'stream/1.0'
    }
    try:
        # --- FIX: Increased timeout from 5 to 10 seconds ---
        response = requests.get(url, headers=headers, timeout=10) 
        response.raise_for_status() # raise an exception for bad status codes
        data = response.json()
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return float(lat), float(lon)
        else:
            st.warning(f"Could not find coordinates for {city_name}. Proceeding without location filter.")
            return None, None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching coordinates: {e}. Proceeding without location filter.")
        return None, None
    except Exception as e:
        st.error(f"An unexpected error occurred during coordinate lookup: {e}")
        return None, None



# STREAMLIT PAGE CONFIg
st.set_page_config(page_title="NetShield", layout="wide", initial_sidebar_state="expanded")

# cSS FOR NETSHIELD LOGO, SIDEBAR FOOTER, AND TOP GAP REDUCTION
st.markdown("""
    <style>
        /* 1. GAP REDUCTIOn Main content block padding */
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

        /* 3. FIXED LOGO INJECTION Top Left Sidebar */
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
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <div style="display: none;">
        NetShield🛡️
    </div>
""", unsafe_allow_html=True)

# SESSION STATE INITIALIZATION kept for consistency, though data_fetchedis less critical now

if 'csv_filename' not in st.session_state:
    st.session_state.csv_filename = "video_data.csv"


# MAIN DASHBOARD LAYouyt
st.title("YouTube Content Analysis Dashboard")
st.markdown("### Parameters for Data Fetching")

# yt Data Fetching Section
with st.form("video_fetch_form"):
    col1, col2, col3 = st.columns(3)

    # Input column 1
    with col1:
        hashtag = st.text_input("Enter a keyword or hashtag to search for:", value="Air pollution and AQI news")
        city = st.text_input("Enter a city name:", value="New Delhi")

    # Input colu 2
    with col2:
        radius = st.text_input("Enter search radius (E.g., '50km'):", "50km")
        start_date = st.date_input("Start date", value=datetime(2025, 11, 1))

    # I 3
    with col3:
        max_results = st.number_input("Maximum results to fetch:", min_value=1, max_value=20, value=5)
        end_date = st.date_input("End date", value=datetime(2025, 11, 30))

 
    csv_filename = st.text_input("Enter the filename to save data (must end in .csv):", st.session_state.csv_filename)

    # Buttons
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        # button label to be clearer about the action
        submitted = st.form_submit_button("Fetch Data & Go to Content Report Page")
    with col_b2:
        autox = st.form_submit_button("Complete Analysis & Switch to Automate Page")

# -DATA PROCESSING logicc
if submitted or autox:
    st.session_state.csv_filename = csv_filename # Store the filename
    try:
        # Convert dates to datetime objects
        progress_bar = st.progress(0)

        start_date_dt = datetime.combine(start_date, datetime.min.time())
        end_date_dt = datetime.combine(end_date, datetime.max.time())

        progress_bar.progress(25)

        #  Get Coordinates
        lat, lon = None, None
        if city:
            lat, lon = get_coordinates(city)

        if lat and lon:
             st.info(f"📍 Location set: **{city}** (Lat: {lat:.2f}, Lon: {lon:.2f}) with radius **{radius}**.")
        elif city:
            st.warning(f"Could not use location data for '{city}'. Searching globally by hashtag.")


        # Fetch video data
        progress_bar.progress(50, text="Fetching video data from YouTube...")

        youtube.video_info(hashtag, lat, lon, radius, max_results, start_date_dt, end_date_dt, csv_filename)

        progress_bar.progress(100, text="Data fetching complete.")

        st.success(f"✅ Data fetched and saved to **{csv_filename}**.")
        
        # PAGE SWITCHING 
        if autox:
            st.switch_page("pages/06Automate.py") # GO TO AUTOMATE
        elif submitted:
             st.switch_page("pages/02Social Content Report.py") # GO TO REPORT


    except Exception as e:
        st.error(f"❌ An error occurred during data fetching: {e}")
        progress_bar.empty()

st.markdown(
    """
    <div class="bottom-note-box" style="background-color: #262626; padding: 15px; margin-top: 40px;
    border-radius: 5px;
     border-left: 5px solid #28a745;">
      <ul style="font-size: 16px; margin: 0; color: #fff; padding-left: 20px; list-style-type: disc;">
       <strong>Note on Re-Searching:</strong> 
        <li>
            If you are searching for a new tag or video for a second time, please <strong>refresh your browser page and clear the cache of the wesbite(Top right 3 dots).</strong>
        </li>
        <li>
             This clears the application's cache and ensures the dashboard loads the new data you just fetched to avoid conflict with previous data.
        </li>
    </ul>
    </div>
    """, 
    unsafe_allow_html=True
)

    
    

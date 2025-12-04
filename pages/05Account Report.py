import streamlit as st
import os
import pandas as pd
import altair as alt


st.set_page_config(page_title="Account Report", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
        /* 1. GAP REDUCTION & MAIN CONTAINER STYLING */
        .block-container {
            padding-top: 0rem !important; 
            padding-bottom: 0rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }

        /* 2. SIDEBAR BACKGROUND */
        [data-testid="stSidebar"] {
            background-color: #1f2937; /* Dark background remains for contrast */
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
        
        /* Custom style for the Description Box (Reusing dark theme) */
        .report-description-box {
            background-color: #333d47; /* Dark background */
            padding: 15px;
            border-radius: 5px;
            border-left: 5px solid #28a745; /* Green/Success accent */
            margin-bottom: 30px; 
        }
        
        .report-description-box strong {
            font-size: 18px;
            display: block; 
            margin-bottom: 5px; 
            color: #ffffff; /* Light text color */
        }
        
        .report-description-box ul {
            margin: 5px 0 0 0; 
            color: #f0f0f0; /* Light text color for list items */
            padding-left: 20px;
            list-style-type: disc;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <div style="display: none;">
        NetShield🛡️
    </div>
""", unsafe_allow_html=True)



st.title("Account Report")


st.markdown("""
    <div class="report-description-box">
        <strong>Misinformation Account Analysis:</strong>
        <ul>
            <li>This report sorts accounts based on the level of misinformation detected in their content (Red, Yellow, Green).</li>
            <li>Chart filter shows the breakdown of accounts on the basis of severity status.</li>
            <li>Accounts marked Red are automatically flagged for immediate review and termination.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)
# -----------------------------

# Path to the CSV file  Use relative pathing

csv_file_path = os.path.join(os.getcwd(), "Accountreport.csv") 

# Check if the file exists

if not os.path.exists(csv_file_path):
    st.header("Account Analysis Not Available")
    st.markdown("""
No 'Accountreport.csv' found. Please run the complete AUTOMATE step to generate the analysis report.

IMP: Please allow the AUTOMATE process to complete fully in order to ensure report generation on this page.
""")

    with st.form(key='request_analysis_form'):
        submitted = st.form_submit_button("Go to Automate Page")
        
        if submitted:
            st.switch_page("pages/06Automate.py")
else:
    # Load the CSV file
    df = pd.read_csv(csv_file_path)
    st.header("Account Analysis Report")
    st.dataframe(df, use_container_width=True) # Display full DataFrame

    st.markdown("---")
    st.subheader("Filter Status and Visualize Breakdown")

    c = st.multiselect(
        "Choose Status for Visualization", ["Red", "Green", "Yellow"], ["Red", "Green", "Yellow"] # Changed default to include all

    )

    # If no status is selected, show an error message

    if not c:
        st.error("Please select at least one status to visualize.")
    else:
        # Filter the data based on the selected statuses

        data = df[df['Status'].isin(c)]

        # Prepare data for charting

        status_counts = data['Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        # Define color scale based on severity

        color_scale = alt.Scale(domain=["Red", "Yellow", "Green"], range=["#e74c3c", "#f39c12", "#2ecc71"]) 

        st.markdown("### Status Count Breakdown")
        
        # Create an Altair chart to visualize the counts of each status
        chart = (
            alt.Chart(status_counts)
            .mark_bar()
            .encode(
                x=alt.X("Status:N", title="Status"),
                y=alt.Y("Count:Q", title="Number of Accounts"),
                color=alt.Color("Status:N", scale=color_scale, legend=None),
                tooltip=['Status', 'Count']
            )
            .properties(
                title="Account Status Distribution"
            )
        )

        # Display the chart in the Streamlit app

        st.altair_chart(chart, use_container_width=True)

        # Termination Accounts Section 
        red_data = df[df['Status'] == "Red"]
            
        st.markdown("---")
        st.subheader("Red Flagged Accounts for Termination 🚨")
        
        if red_data.empty:
            st.info("No accounts currently flagged with 'Red' status.")
        else:
            # Display the filtered Red accounts

            st.dataframe(red_data, use_container_width=True, hide_index=True)

            # Save the filtered Red accounts to a CSV file for termination
            terminate_file_path = "terminate.csv"
            red_data.to_csv(terminate_file_path, index=False)
            st.success(f"Red accounts (requiring termination) successfully saved to **{terminate_file_path}**.")
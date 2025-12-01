import streamlit as st
import groq 
import os 

# streamlit page configuration
st.set_page_config(page_title="NetShield Dashboard", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    
        /* main content block padding */
            
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }

        /* sIDEBAR BACKGROUND */
            
        [data-testid="stSidebar"] {
            background-color: #1f2937; /* Dark background */
            color: white;
        }

        /* 3. fixed LOGO INJECTION (Top Leftabove Dashboard) */
            
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
        
        /* 4. SIDEBAR FOOTER navig text bottom */
            
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

        /* titlee */
        .maintitle {
            font-size: 50px;
            font-weight: bold;
            color: white;
            margin-top: 20px; 
            margin-left: 20px; 
        }
        
        /* Introductory text spacing */
        .introspacing {
            margin-left: 20px; 
        }
            
        /*  Card Style */
        .card {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            background-color: #f9f9f9;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin: 20px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .card:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }

        .card h3 {
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
        }

        .card p {
            font-size: 18px;
            color: #7f8c8d;
        }
        
        /* centering and Highlighting the Button --- */
        
        /* 1 targeting the inner button container to adjust minimal top/bottom spacing */
            
        div[data-testid="stForm"] > div > div {
           
           display: flex;
           justify-content: center; 
           width: 100%; 
           /* Reduced space above the button */
           margin-top: 10px; 
           /* Reduced space below the button */
           margin-bottom: 10px; 
        }
        
        /* 2. targeting the form to control its size and spacing */
        div[data-testid="stForm"] {
           
            max-width: 400px; 
      
            margin-left: auto;
            margin-right: auto;
         
            padding-bottom: 10px; 
        }
        
        /* 3. Highlight and style the actual button */
            
        .stButton button {
            background-color: #e74c3c; 
            color: white;
            border-radius: 8px;
            padding: 10px 40px; 
            font-size: 20px; 
            font-weight: bold;
            border: none;
            box-shadow: 0 4px #c0392b; 
            transition: background-color 0.1s ease, box-shadow 0.1s ease;
        }

        .stButton button:hover {
            background-color: #c0392b; 
            box-shadow: 0 2px #9c2d22;
            transform: translateY(2px); 
        }
    

       /*  rule for the popover - */
            
        [data-testid="stPopover"] {
            position: fixed !important; 
            bottom: 20px;
            right: 40px;
            left: auto !important;   /* <-- This was the fix */
            width: auto !important;  
            z-index: 1001;
        }
        
        /* -- hover color for the popover button- */
            
        [data-testid="stPopover"] button:hover {
            background-color: #324885; /* Your chosen blue color */
            color: white !important;           /* Makes text white on hover */
            border-color: #0056b3;     /* A darker blue border */
        }
            
    </style>
""", unsafe_allow_html=True)

# inject the logo text invisibly to avoid conflict with sidebar CSS

st.markdown("""
    <div style="display: none;">
        NetShield🛡️
    </div>
""", unsafe_allow_html=True) 

# -\\The Sidebar Python Content mmust be empty now to avoid conflict ---
with st.sidebar:
    pass 
# ------

# -- Main Page Conten
st.markdown('<div class="maintitle"><h1>Welcome to NetShield!</div>', unsafe_allow_html=True)
st.markdown("""
    <div class="introspacing">
        In this dashboard, we focus on identifying and combating the growing problem of fake news in the form of misleading videos and blogs circulating across the country.
    </div>
""", unsafe_allow_html=True)

# --- Flash Card
st.markdown("""
    <div class="card">
        <h3>Fake News: A Growing Threat</h3>
        <p>Fake news videos and blogs have become a major issue, leading to the spread of misinformation, social unrest, and a general erosion of trust in media sources. The rapid dissemination of misleading content has caused confusion and harm to society, and it is crucial to have reliable tools to identify and counteract these threats.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="card">
        <h3>Impact of Fake News</h3>
        <p>The consequences of fake news are far-reaching, affecting public opinion, political stability, and even public health. From misleading information about elections to harmful medical advice, fake news is a serious concern that needs to be addressed immediately.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="card">
        <h3>How NetShield Helps</h3>
        <p>NetShield aims to identify fake news by analyzing video content and blogs. Through the power of artificial intelligence and machine learning, we provide tools for detecting fraudulent content, empowering users to make informed decisions and contribute to a more informed society.</p>
    </div>
""", unsafe_allow_html=True)

# --- Start Form 
with st.form(key='dashboard_start_form'):
    # The submit button is automatically centered due to the new flexbox Css
    submitted = st.form_submit_button("Let's Start")
    if submitted:
       
        st.switch_page("pages/01Request Analysis.py")



# --- CHATBot


# This is the brain of bot 

KNOWLEDGE_BASE = """
- **About NetShield:** NetShield is a multi-page dashboard designed to find and analyze YouTube videos for misinformation. It works by comparing video content against factual news articles.

- **Dashboard (Main Page):** This is the welcome page. It gives a brief overview of the fake news problem. It has one button, 'Let's Start', which takes the user to the 'Request Analysis' page.

- **01. Request Analysis (Start Here):** This is the first step. The user provides search criteria like a keyword (e.g., 'Air pollution'), a city, a date range, and the max number of videos to fetch.
    - **Actions:**
        1.  Clicking 'Fetch Data & Go to Content Report Page' will find the videos, save them to 'video_data.csv', and take the user to the 'Social Content Report' page to see the raw data.
        2.  Clicking 'Complete Analysis & Switch to Automate Page' will find the videos, save them, and take the user directly to the 'Automate' page to start the full AI analysis.

- **02. Social Content Report:** This page shows the *raw, un-analyzed data* fetched from 'Request Analysis'. It displays a full table of the videos found and a line chart of their views over time. This page is for *viewing* the data before the AI pipeline is run. A note on this page confirms that the AI filtering happens in the 'Automate' section.

- **03. Content Forensic:** This page performs a deep dive into the video's *audio*. It loads the 'video_data.csv' file, downloads the audio for each video using 'yt-dlp.exe', and uses the **AssemblyAI** service to generate a full text transcript. The transcript for each video is displayed in a text box and saved as a '.txt' file.

- **04. Current Context Report:** This page finds the *factual context* for the videos. It loads 'video_data.csv', takes each video's title, and searches Google News for related articles. It then scrapes the full text of those articles and displays them in expandable sections. This allows a user to manually compare what the video says with what news sources report.

- **06. Automate (The AI Engine):** This is the main analysis page. It runs the full AI pipeline on the videos from 'video_data.csv'. For each video, it:
    1.  **Transcribes** the audio (using 'transcribe.py').
    2.  **Summarizes** the video's transcript (using 'summarize.py' with a Mistral 7B model).
    3.  **Finds** related news articles (using 'nextractor.py').
    4.  **Summarizes** the news articles (using 'summarize.py').
    5.  **Validates** the content by sending both summaries to a **Llama 3 70B** model (in 'identifier.py').
    6.  The Llama 3 model assigns a final status: **'Green'** (Accurate), **'Yellow'** (Inconclusive/Junk), or **'Red'** (Misinformation/Content Abuse).
    7.  The final results are saved to **'Accountreport.csv'**.

- **05. Account Report (Final Results):** This page shows the *final results* after the 'Automate' page is finished. It reads the **'Accountreport.csv'** file and displays a complete table with the 'Green', 'Yellow', or 'Red' status for each video. It also shows a bar chart of the status breakdown.
    - **Critical Feature:** This page has a section named 'Red Flagged Accounts for Termination 🚨' which filters all 'Red' status videos and saves them to a new file, **'terminate.csv'**, for action.
"""

try:
    client = groq.Groq(api_key=st.secrets["GROQ_API_KEY"])
    chat_available = True
except Exception:
    client = None
    chat_available = False

# 1 Initialize session state (for chat reset)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_active" not in st.session_state:
    st.session_state.chat_active = False

# 2 Check if chat was active. if not, clear history
if not st.session_state.chat_active:
    st.session_state.messages.clear()

# 3. Reset the flag for this run
st.session_state.chat_active = False


# 4. Create the Popover Chat

if chat_available:
    with st.popover("Netshield AI Assistant 🛡️"):
        
        #  Set the active flag (so reset logic works)
        st.session_state.chat_active = True 
        
        #  Create a scrollable container for the chat history
        chat_container = st.container(height=400)
        
        #  Display existing messagesinside this container
        with chat_container:
            for message in st.session_state.messages:
                
                # Assign avatars based on role
                if message["role"] == "user":
                    avatar_logo = "🧑‍💻" 
                else:
                    avatar_logo = "🛡️" 
                
                # Display the message
                with st.chat_message(message["role"], avatar=avatar_logo):
                    st.markdown(message["content"])

        #  Get new user input (this stays at the bottom)
        if prompt := st.chat_input("How can I help you?"):
            
            # Add user message to state
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # -- This is the training part 
            system_prompt = f"""
            You are a helpful AI assistant for a website called "NetShield".
            Your job is to answer user questions about the website's features.

            Here is all the information about the NetShield website:
            ---
            {KNOWLEDGE_BASE}
            ---
            
            RULES:
            1. Answer the user's question based *only* on the information provided above.
            2. If the user asks about something *not* in the context (like the weather, news, or a random question),
               politely say: "I can only answer questions about the NetShield dashboard."
            3. Be friendly and helpful.
            """
            
            #  Get AI response and add to state
            try:
                # Create the message list to send to the API
                messages_to_send = [
                    {"role": "system", "content": system_prompt}
                ] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]

                # Call Groq API
                chat_completion = client.chat.completions.create(
                    messages=messages_to_send,
                    model="llama-3.1-8b-instant",
                )
                response = chat_completion.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            except Exception as e:
                error_message = f"Error communicating with servers: {e}"
                st.session_state.messages.append({"role": "assistant", "content": error_message})
            
            # rerun the script to show the new messages
            st.rerun()

else:
    
    st.popover("💬 Chat (Unavailable)", disabled=True, help="GROQ_API_KEY not found in st.secrets.")

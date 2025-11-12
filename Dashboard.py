import streamlit as st

# Set up Streamlit page configuration
st.set_page_config(page_title="NetShield Dashboard", layout="wide")

# Adding some custom CSS for enhanced styling
st.markdown("""
    <style>
        .maintitle {
            font-size: 50px;
            font-weight: bold;
            color: #2c3e50;
            margin-top: 20px;
        }

        .subheader {
            font-size: 24px;
            font-weight: bold;
            color: #34495e;
            margin-bottom: 20px;
        }

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

        .button-container {
            margin-top: 40px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Title of the Dashboard
st.markdown('<div class="maintitle"><h1>Welcome to NetShield!</div>', unsafe_allow_html=True)

# Introduction Text
st.write("In this dashboard, we focus on identifying and combating the growing problem of fake news in the form of misleading videos and blogs circulating across the country.")

# Flash Card for Fake News Problem
st.markdown("""
    <div class="card">
        <h3>Fake News: A Growing Threat</h3>
        <p>Fake news videos and blogs have become a major issue, leading to the spread of misinformation, social unrest, and a general erosion of trust in media sources. The rapid dissemination of misleading content has caused confusion and harm to society, and it is crucial to have reliable tools to identify and counteract these threats.</p>
    </div>
""", unsafe_allow_html=True)

# Flash Card for Impact of Fake News
st.markdown("""
    <div class="card">
        <h3>Impact of Fake News</h3>
        <p>The consequences of fake news are far-reaching, affecting public opinion, political stability, and even public health. From misleading information about elections to harmful medical advice, fake news is a serious concern that needs to be addressed immediately.</p>
    </div>
""", unsafe_allow_html=True)

# Flash Card for Social Guard's Role
st.markdown("""
    <div class="card">
        <h3>How NetShield Helps</h3>
        <p>NetShield aims to identify fake news by analyzing video content and blogs. Through the power of artificial intelligence and machine learning, we provide tools for detecting fraudulent content, empowering users to make informed decisions and contribute to a more informed society.</p>
    </div>
""", unsafe_allow_html=True)


with st.form(key='dashboard_start_form'):
    submitted = st.form_submit_button("Let's Start")
    if submitted:
        st.switch_page("pages/01Request Analysis.py") # Corrected page switch destination
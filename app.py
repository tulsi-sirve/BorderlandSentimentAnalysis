import streamlit as st
import joblib
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

def set_bg_color(color="#f4d03f"):
    """
    Set background color using CSS.
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color} !important;
        }}
        body {{
            background-color: #f4d03f;
            background-size: cover;
            color: #ffcc00;
            font-family: 'Orbitron', sans-serif;
        }}
        .stButton>button {{
            background-color: #ff4500;
            color: white;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(255, 69, 0, 0.8);
        }}
        .stTextArea>textarea {{
            background-color: #333;
            color: #ffcc00;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px;
        }}
        .stProgress>div>div>div {{
            background-color: #ff4500;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Apply Borderlands-styled background
set_bg_color()

# User Authentication
users = {"vault_hunter": "pandora123"}  # Example user credentials
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login_page():
    st.title("🔐 Vault Login - Borderlands Sentiment Analyzer")
    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type="password")
    
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state["authenticated"] = True
            st.success("Access Granted! Welcome to Pandora!")
            st.rerun()

        else:
            st.error("Incorrect username or password!")

def tweet_input_page():
    st.sidebar.subheader("🔫 Enter Your Tweet Below")
    tweet = st.sidebar.text_area("📝 What's on your mind, Vault Hunter?")
    
    if st.sidebar.button("💀 Predict Sentiment"):
        st.session_state["tweet"] = tweet
        st.rerun()

def dashboard_page():
    st.title("🎮 Borderlands-Themed Sentiment Analyzer")
    st.markdown("**Feel the chaos! Predict tweet sentiments in a true Borderlands style.**")
    
    model = joblib.load("twitter_sentiment.joblib")
    tweet = st.session_state.get("tweet", "")
    
    if tweet:
        with st.spinner("🚀 Deploying Claptrap AI..."):
            start = time.time()
            prediction = model.predict([tweet])
            end = time.time()
            st.success(f"Predicted Sentiment: **{prediction[0]}**")
            st.write(f"⏳ Processing Time: **{round(end-start, 2)} sec**")
            st.progress(100)
    
    try:
        df = pd.read_csv("C:\\Users\\hp\\OneDrive\\Desktop\\TY Sem VI practicals\\STQA\\twitter_training.csv", encoding="ISO-8859-1")
        df.columns = df.columns.str.strip()
        sentiment_counts = df["sentiment"].value_counts()
        
        st.subheader("📊 Sentiment Distribution in Pandora")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette=["#ffcc00", "#ff4500", "#0088ff"], ax=ax)
        ax.set_xlabel("Sentiment", fontsize=14, color="#ffcc00")
        ax.set_ylabel("Frequency", fontsize=14, color="#ffcc00")
        plt.xticks(fontsize=12, color="#ffcc00")
        plt.yticks(fontsize=12, color="#ffcc00")
        st.pyplot(fig)
    except FileNotFoundError:
        st.warning("🚨 No dataset found. Claptrap is confused!")

# Control Flow
if not st.session_state["authenticated"]:
    login_page()
elif "tweet" not in st.session_state:
    tweet_input_page()
else:
    dashboard_page()

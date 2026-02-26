import streamlit as st
import openai
import pandas as pd
import os
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. Website Styling
st.set_page_config(page_title="LionCompass", page_icon="🦁")
st.title("🦁 LionCompass")
st.subheader("Your AI Guide to Columbia Campus Life")

# 3. Load ALL your data
@st.cache_data # This makes the website fast
def load_data():
    df = pd.read_csv('source_data/daily_events.csv')
    return df

df = load_data()

# 4. The Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask about events, study spaces, or food..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. RAG: Search the data
    # We'll give the AI the full list of events now!
    context = ""
    for _, row in df.iterrows():
        context += f"- {row['Title']} at {row['Source']}\n"

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are LionCompass. Use this data: {context}"},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
import openai
import pandas as pd
import os
from dotenv import load_dotenv

# This line finds the .env file and reads the key
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def lion_compass_chat():
    # Load your scraped data
    df = pd.read_csv('source_data/daily_events.csv')
    
    # Turn the data into a single block of text the AI can read
    knowledge_base = ""
    for _, row in df.head(10).iterrows(): # We'll start with the first 10 events
        knowledge_base += f"- {row['Title']} (Source: {row['Source']})\n"

    print("--- LionCompass is Live! (Type 'quit' to exit) ---")
    
    while True:
        user_query = input("Student: ")
        if user_query.lower() == 'quit':
            break

        # 2. This is the RAG (Retrieval-Augmented Generation) part!
        # We tell the AI: "Use this info to answer the question"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are LionCompass, a helpful assistant for Columbia students. Use ONLY the following events to answer: {knowledge_base}"},
                {"role": "user", "content": user_query}
            ]
        )

        print(f"\nLionCompass: {response.choices[0].message.content}\n")

if __name__ == "__main__":
    lion_compass_chat()
import pandas as pd
import os

def process_campus_data():
    print("--- LionBrain: Starting Data Processing ---")
    
    # 1. Load the data we scraped earlier
    file_path = 'source_data/daily_events.csv'
    
    if not os.path.exists(file_path):
        print("Error: No data file found! Run your scraper first.")
        return

    df = pd.read_csv(file_path)
    
    # 2. Convert the table into "Sentences" for the AI
    # Instead of a row in a table, the AI likes reading descriptions
    knowledge_base = []
    
    for index, row in df.iterrows():
        # We create a clear string for each event
        entry = f"Event: {row['Title']}. Source: {row['Source']}. Information accurate as of {row['Retrieved_At']}."
        knowledge_base.append(entry)
    
    # 3. For now, let's just print the first 3 "memories" to see if it works
    print(f"Successfully processed {len(knowledge_base)} events.")
    print("Here are the first 3 things I learned:")
    for memory in knowledge_base[:3]:
        print(f"- {memory}")

if __name__ == "__main__":
    process_campus_data()
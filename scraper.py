import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def scrape_columbia_events():
    url = "https://events.columbia.edu/cal" # Using a more general Columbia link
    print(f"--- Step 1: Attempting to connect to {url} ---")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"--- Step 2: Website responded with Status Code: {response.status_code} ---")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Let's see if we can find ANY links on the page at all
            links = soup.find_all('a')
            print(f"--- Step 3: Found {len(links)} links on the page. ---")
            
            events = []
            # This is a broader search for event titles
            for link in links:
                title = link.get_text(strip=True)
                if len(title) > 10: # Only look at links with actual text
                    events.append({
                        "Title": title,
                        "Source": url,
                        "Retrieved_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
            
            if events:
                # Ensure the folder exists
                if not os.path.exists('source_data'):
                    os.makedirs('source_data')
                
                df = pd.DataFrame(events)
                df.to_csv('source_data/daily_events.csv', index=False)
                print(f"--- Step 4: SUCCESS! Saved {len(events)} items to source_data/daily_events.csv ---")
            else:
                print("--- Step 4: Found the website, but couldn't identify any events. ---")
        else:
            print("--- Step 2: Failed to reach the site. Is your internet connected? ---")
            
    except Exception as e:
        print(f"--- ERROR: Something went wrong: {e} ---")

if __name__ == "__main__":
    scrape_columbia_events()
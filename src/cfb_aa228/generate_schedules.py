import requests
from bs4 import BeautifulSoup
import pandas as pd

def generate_schedules(url="https://www.sports-reference.com/cfb/years/2024-schedule.html"):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    schedule_list = []
    table = soup.find('table', {'id': 'schedule'})

    for row in table.find_all('tr'):
        # Skip rows without data or with header classes
        if 'thead' in row.get('class', []):
            continue

        cells = row.find_all('td')
        if len(cells) < 9:  # Skip rows that don't contain game data
            continue
        
        week = int(cells[0].get_text(strip=True))
        date = cells[2].get_text(strip=True)
        team1 = cells[4].get_text(strip=True)
        score1 = cells[5].get_text(strip=True)
        team2 = cells[7].get_text(strip=True)
        score2 = cells[8].get_text(strip=True)
        
        schedule_list.append({
            'week': week,
            'date': date,
            'team1': team1,
            'score1': score1,
            'team2': team2,
            'score2': score2,
        })
    
    schedule_df = pd.DataFrame(schedule_list)
    return schedule_df

if __name__ == "__main__":
    schedule_df = generate_schedules()
    schedule_df.to_csv("college_football_schedule.csv", index=False)
    print(schedule_df.head()) 
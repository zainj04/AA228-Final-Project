import requests
from bs4 import BeautifulSoup
import pandas as pd

SEC_TEAMS = [
    "Alabama", "Arkansas", "Auburn", "Florida", "Georgia", "Kentucky",
    "LSU", "Mississippi State", "Missouri", "Oklahoma", "Ole Miss",
    "South Carolina", "Tennessee", "Texas", "Texas A&M", "Vanderbilt"
]

def generate_schedules(url="https://www.sports-reference.com/cfb/years/2024-schedule.html"):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    schedule_list = []
    table = soup.find('table', {'id': 'schedule'})

    for row in table.find_all('tr'):
        if 'thead' in row.get('class', []):
            continue

        cells = row.find_all('td')
        if len(cells) < 9:
            continue
        
        week = int(cells[0].get_text(strip=True))
        date = cells[1].get_text(strip=True)
        team1 = cells[4].get_text(strip=True)
        score1 = cells[5].get_text(strip=True)
        team2 = cells[7].get_text(strip=True)
        score2 = cells[8].get_text(strip=True)
        
        # Filter for SEC teams only
        if team1 in SEC_TEAMS or team2 in SEC_TEAMS:
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
    schedule_df.to_csv("sec_football_schedule.csv", index=False)
    print(schedule_df.head()) 
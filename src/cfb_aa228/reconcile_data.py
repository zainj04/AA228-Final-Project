import requests
import pandas as pd
import json

API_KEY = '430c86481b9341c42723273223812460'  # Use your actual API key

def fetch_odds_data(week, region='us', markets=['h2h', 'spreads']):
    url = f"https://api.the-odds-api.com/v4/sports/americanfootball_ncaaf/odds/"
    params = {
        'apiKey': API_KEY,
        'regions': region,
        'markets': ','.join(markets),
        'oddsFormat': 'american',
        'dateFormat': 'iso'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        return pd.DataFrame()
    
    # Save the full JSON response to a file
    with open(f"api_response_week_{week}.json", "w") as json_file:
        json.dump(response.json(), json_file, indent=4)
    
    print(f"API response saved to api_response_week_{week}.json")
    
    # Proceed with existing code to process odds data
    odds_data = response.json()
    odds_list = []

    for game in odds_data:
        home_team = game['home_team']
        away_team = game['away_team']
        
        # Initialize odds and spread values
        home_odds = None
        away_odds = None
        home_spread = None
        away_spread = None
        
        for bookmaker in game['bookmakers']:
            for market in bookmaker['markets']:
                if market['key'] == 'h2h':  # Head-to-head Moneyline odds
                    home_odds = market['outcomes'][0]['price'] if market['outcomes'][0]['name'] == home_team else market['outcomes'][1]['price']
                    away_odds = market['outcomes'][1]['price'] if market['outcomes'][1]['name'] == away_team else market['outcomes'][0]['price']
                elif market['key'] == 'spreads':  # Spread odds
                    home_spread = market['outcomes'][0]['point'] if market['outcomes'][0]['name'] == home_team else market['outcomes'][1]['point']
                    away_spread = market['outcomes'][1]['point'] if market['outcomes'][1]['name'] == away_team else market['outcomes'][0]['point']
                    
        # Append only if odds were found
        if home_odds is not None and away_odds is not None:
            odds_list.append({
                'week': week,
                'home_team': home_team,
                'away_team': away_team,
                'home_odds': home_odds,
                'away_odds': away_odds,
                'home_spread': home_spread,
                'away_spread': away_spread
            })

    odds_df = pd.DataFrame(odds_list)
    return odds_df

if __name__ == "__main__":
    week = 0  # Set this to the desired week for testing
    odds_df = fetch_odds_data(week)
    print(odds_df.head())
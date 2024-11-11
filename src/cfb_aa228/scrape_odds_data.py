import json
import pandas as pd
from datetime import datetime

def fetch_odds_from_json(json_path='api_response.json', date=None, week=None, save_csv=False):
    """
    Fetch odds data from the JSON file, filter by date or week if specified, and return as a DataFrame.
    
    Parameters:
    - json_path (str): Path to the JSON file containing the API response with odds data.
    - date (str, optional): Date in 'YYYY-MM-DD' format to filter games up to this date.
    - week (int, optional): Week number to filter games up to this week.
    - save_csv (bool): If True, saves the filtered data to a CSV file.
    
    Returns:
    - pd.DataFrame: DataFrame containing the filtered schedule and odds data.
    """
    
    # Load JSON data from the specified file path
    with open(json_path, 'r') as f:
        data = json.load(f)

    games = []
    target_date = datetime.strptime(date, '%Y-%m-%d') if date else None
    
    # Iterate through each game in the JSON data
    for game in data:
        game_week = game.get('week')  # Week number, if available in the JSON
        game_date = datetime.fromisoformat(game['commence_time'][:-1])  # Convert ISO format to datetime
        
        # Filter by date or week if parameters are provided
        if target_date and game_date > target_date:
            continue
        if week and game_week and game_week > week:
            continue
        
        # Initialize dictionary to collect game data
        odds = {
            'week': game_week,
            'date': game_date,
            'home_team': game['home_team'],
            'away_team': game['away_team']
        }
        
        # Extract odds information from each bookmaker
        for bookmaker in game['bookmakers']:
            for market in bookmaker['markets']:
                if market['key'] == 'h2h':  # Moneyline odds
                    outcomes = market['outcomes']
                    odds['line1'] = next((outcome['price'] for outcome in outcomes if outcome['name'] == odds['home_team']), None)
                    odds['line2'] = next((outcome['price'] for outcome in outcomes if outcome['name'] == odds['away_team']), None)
                elif market['key'] == 'spreads':  # Spread odds
                    outcomes = market['outcomes']
                    odds['spread'] = next((outcome['point'] for outcome in outcomes if outcome['name'] == odds['home_team']), None)
        
        # Append processed game data to the list
        games.append(odds)

    # Convert the list of games into a DataFrame
    odds_df = pd.DataFrame(games)
    
    # Save the DataFrame to a CSV file if save_csv is True
    if save_csv:
        filename = f'odds_data_up_to_{date or "week_" + str(week) if week else "full_season"}.csv'
        odds_df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    
    return odds_df

# Example usage within main or another script:
if __name__ == "__main__":
    # Example: Fetch odds up to a specified date, and save to CSV
    odds_df = fetch_odds_from_json(date="2024-10-01", save_csv=True)
    print(odds_df.head())
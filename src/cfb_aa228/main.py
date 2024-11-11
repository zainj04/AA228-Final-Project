import pandas as pd
import json
from datetime import datetime

# Load CSV and JSON data
def load_data():
    # Load the schedule CSV into a DataFrame
    schedule_df = pd.read_csv("college_football_schedule_2024.csv")
    
    # Load the betting odds JSON file
    with open("api_response.json") as f:
        api_data = json.load(f)
    
    # Convert JSON data to DataFrame for easier filtering and merging
    api_df = pd.json_normalize(api_data, 'bookmakers', ['home_team', 'away_team', 'commence_time'], errors='ignore')
    return schedule_df, api_df

# Get all games up to the requested week for the specified team
def get_team_schedule(schedule_df, api_df, team_name, week_number):
    # Filter the schedule for games with the team up to the requested week
    team_schedule = schedule_df[
        ((schedule_df['team1'] == team_name) | (schedule_df['team2'] == team_name)) &
        (schedule_df['week'] <= week_number)
    ]

    # Initialize report string
    report = f"Schedule for {team_name} up to Week {week_number}:\n\n"

    # Iterate through each game in the filtered schedule
    for _, game in team_schedule.iterrows():
        # Determine if the team is home or away
        is_home = game['team1'] == team_name
        opponent = game['team2'] if is_home else game['team1']
        
        # Get betting info from the API data
        game_date = game['date']
        betting_info = api_df[
            (api_df['home_team'] == game['team1']) & 
            (api_df['away_team'] == game['team2']) & 
            (api_df['commence_time'].str.contains(game_date))
        ]

        # Display betting odds and spread if available
        if not betting_info.empty:
            spread = betting_info['markets'][0].get('outcomes', [{}])[0].get('point', 'N/A')
            moneyline = betting_info['markets'][0].get('outcomes', [{}])[0].get('price', 'N/A')
        else:
            spread = "---"
            moneyline = "---"
        
        # Check if the game has already occurred
        game_result = game['result'] if 'result' in game else '---'

        # Add game details to the report
        report += (
            f"Week {game['week']} - {game_date}\n"
            f"Opponent: {opponent}\n"
            f"Spread: {spread}, Moneyline: {moneyline}\n"
            f"Result: {game_result}\n\n"
        )

    # Print the final report to standard output
    print(report)

# Main function to execute the logic
def main():
    # Load data
    schedule_df, api_df = load_data()
    
    # Get user input
    team_name = input("Enter team name (e.g., 'Stanford Cardinal'): ")
    week_number = int(input("Enter week number (e.g., '1'): "))
    
    # Generate and display the team's schedule up to the requested week
    get_team_schedule(schedule_df, api_df, team_name, week_number)

if __name__ == "__main__":
    main()
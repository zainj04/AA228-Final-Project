import pandas as pd
import re
from generate_schedules import generate_schedules
from scrape_odds_data import fetch_odds_data
from datetime import datetime
import os

# Mapping dictionary for team name standardization
team_name_mapping = {
    "Alabama": "Alabama Crimson Tide",
    "Arkansas": "Arkansas Razorbacks",
    "Auburn": "Auburn Tigers",
    "Florida": "Florida Gators",
    "Georgia": "Georgia Bulldogs",
    "Kentucky": "Kentucky Wildcats",
    "LSU": "LSU Tigers",
    "Mississippi State": "Mississippi State Bulldogs",
    "Missouri": "Missouri Tigers",
    "Oklahoma": "Oklahoma Sooners",
    "Ole Miss": "Ole Miss Rebels",
    "South Carolina": "South Carolina Gamecocks",
    "Tennessee": "Tennessee Volunteers",
    "Texas": "Texas Longhorns",
    "Texas A&M": "Texas A&M Aggies",
    "Vanderbilt": "Vanderbilt Commodores",
    "Miami (FL)": "Miami Hurricanes",
    "Southern Mississippi": "Southern Mississippi Golden Eagles",
    "Clemson": "Clemson Tigers",
    # Add more mappings as needed
}

def main():
    # Generate or load the schedule data
    schedule_df = generate_schedules()
    
    # Clean and standardize team names in schedule data
    schedule_df['team1'] = schedule_df['team1'].apply(lambda x: re.sub(r"\(\d+\)", "", x).strip())
    schedule_df['team2'] = schedule_df['team2'].apply(lambda x: re.sub(r"\(\d+\)", "", x).strip())
    schedule_df['team1'] = schedule_df['team1'].replace(team_name_mapping)
    schedule_df['team2'] = schedule_df['team2'].replace(team_name_mapping)

    # Initialize a DataFrame to store the full season's schedule and odds data
    full_season_data = pd.DataFrame()

    # Iterate through each week and fetch odds data
    for week in sorted(schedule_df['week'].unique()):
        # Fetch or load odds data for the current week
        odds_filename = f"betting_odds_week_{week}.csv"
        if os.path.exists(odds_filename):
            print(f"Loading betting data from {odds_filename}")
            odds_df = pd.read_csv(odds_filename)
        else:
            print(f"Fetching betting data for week {week}")
            odds_df = fetch_odds_data(week)
            odds_df.to_csv(odds_filename, index=False)  # Save for future use

        # Merge schedule and odds data
        week_data = schedule_df[schedule_df['week'] == week].merge(
            odds_df[['home_team', 'away_team', 'home_odds', 'away_odds', 'home_spread']],
            left_on=['team1', 'team2'], right_on=['home_team', 'away_team'], how='left'
        )

        # Standardize column names and select relevant columns
        week_data = week_data.rename(columns={
            'team1': 'home_team', 'team2': 'away_team',
            'home_odds': 'line1', 'away_odds': 'line2', 'home_spread': 'spread'
        })[['week', 'date', 'home_team', 'away_team', 'line1', 'line2', 'spread']]

        # Append to the full season data
        full_season_data = pd.concat([full_season_data, week_data], ignore_index=True)

    # Save the full season data to a CSV
    full_season_data.to_csv("full_season_schedule_with_odds.csv", index=False)
    print("Full season data saved to full_season_schedule_with_odds.csv")
    print(full_season_data.head())

if __name__ == "__main__":
    main()
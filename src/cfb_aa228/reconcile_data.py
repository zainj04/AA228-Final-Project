import pandas as pd
import json
import os
from fuzzywuzzy import fuzz, process

# Define file paths
SEC_SCHEDULE_FILE = os.path.join("..", "..", "sec_football_schedule.csv")
SCHEDULE_WITH_ODDS_FILE = os.path.join("..", "..", "schedule_with_odds_week_2.csv")
COLLEGE_FOOTBALL_SCHEDULE_FILE = os.path.join("..", "..", "college_football_schedule_2024.csv")

# Load data from CSV files
def load_data():
    sec_schedule = pd.read_csv(SEC_SCHEDULE_FILE)
    schedule_with_odds = pd.read_csv(SCHEDULE_WITH_ODDS_FILE)
    college_football_schedule = pd.read_csv(COLLEGE_FOOTBALL_SCHEDULE_FILE)
    return sec_schedule, schedule_with_odds, college_football_schedule

# Automatically match team names across DataFrames
def match_team_names(reference_teams, target_teams):
    team_map = {}
    for team in target_teams:
        # Find the best match with a minimum similarity score of 80
        match, score = process.extractOne(team, reference_teams, scorer=fuzz.token_sort_ratio)
        if score >= 80:
            team_map[team] = match
        else:
            print(f"No close match found for: {team}")
    return team_map

# Apply team name mapping to DataFrame
def apply_team_name_mapping(df, team_column, team_map):
    df[team_column] = df[team_column].replace(team_map)
    return df

# Aggregate odds data for SEC teams
def aggregate_odds_data():
    sec_schedule, schedule_with_odds, college_football_schedule = load_data()
    
    # Get unique team names from SEC and odds DataFrames
    sec_teams = pd.concat([sec_schedule['team1'], sec_schedule['team2']]).unique()
    odds_teams = pd.concat([schedule_with_odds['team1'], schedule_with_odds['team2']]).unique()
    college_teams = pd.concat([college_football_schedule['team1'], college_football_schedule['team2']]).unique()
    
    # Create a mapping for team names based on fuzzy matching
    odds_team_map = match_team_names(sec_teams, odds_teams)
    college_team_map = match_team_names(sec_teams, college_teams)
    
    # Apply the mappings to standardize team names
    schedule_with_odds = apply_team_name_mapping(schedule_with_odds, 'team1', odds_team_map)
    schedule_with_odds = apply_team_name_mapping(schedule_with_odds, 'team2', odds_team_map)
    college_football_schedule = apply_team_name_mapping(college_football_schedule, 'team1', college_team_map)
    college_football_schedule = apply_team_name_mapping(college_football_schedule, 'team2', college_team_map)
    
    # Merge data on week and team names
    merged_data = pd.merge(sec_schedule, schedule_with_odds, on=['week', 'team1', 'team2'], how='outer', suffixes=('_sec', '_odds'))
    merged_data = pd.merge(merged_data, college_football_schedule, on=['week', 'team1', 'team2'], how='outer')
    
    # Extract only SEC team odds data
    sec_data = merged_data[merged_data['team1'].isin(sec_teams) | merged_data['team2'].isin(sec_teams)]
    return sec_data

# Save SEC team data to JSON
def save_to_json(data):
    output_path = os.path.join("..", "..", "sec_team_odds_data.json")
    data.to_json(output_path, orient='records')
    print(f"Data saved to {output_path}")

if __name__ == "__main__":
    sec_team_odds_data = aggregate_odds_data()
    save_to_json(sec_team_odds_data)
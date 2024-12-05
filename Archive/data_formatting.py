import pandas as pd

#Retrieve and format available lines
betting_data = pd.read_csv('./Data/2023/stanford_2023_lines.csv')

#Only include Bovada lines
betting_data = betting_data[betting_data['LineProvider'].str.contains('Bovada', case=False, na=False)]

#Sort chronologically
betting_data = betting_data.sort_values(by=betting_data.columns[0], ascending=True)

betting_data = betting_data.reset_index(drop=True)

betting_data.to_csv('./Data/2023/stanford_2023_lines_altered.csv', index=False)

betting_data.head(20)

num_rows, num_columns = betting_data.shape

print("Size of Betting Data")
print("")
print(f"Number of rows: {num_rows}")
print(f"Number of columns: {num_columns}")

#Retrieve game stats
game_stats = pd.read_csv('./Data/2023/stanford_2023_gamestats.csv')

#Get rid of unnecessary columns and Sacramento State game since we don't have betting lines
game_stats = game_stats.drop(columns=['Season Type', 'Start Date', 
                                     'Start Time Tbd', 'Completed',
                                     'Neutral Site', 'Conference Game',
                                     'Attendance', 'Venue Id', 'Venue',
                                     'Home Id', 'Home Conference',
                                     'Home Division', 'Home Line Scores[0]',
                                     'Home Line Scores[1]', 'Home Line Scores[2]',
                                     'Home Line Scores[3]', 'Away Id',
                                     'Away Line Scores[0]', 'Away Line Scores[1]',
                                     'Away Line Scores[2]', 'Away Line Scores[3]',
                                     'Away Conference', 'Away Division', 'Highlights',
                                     'Notes'], index=2)

game_stats.to_csv('./Data/2023/stanford_2023_gamestats_altered.csv', index=False)

game_stats.head(12)

num_rows, num_columns = game_stats.shape

print("Size of Game Stats Data")
print("")
print(f"Number of rows: {num_rows}")
print(f"Number of columns: {num_columns}")

adv_metrics = pd.read_csv('./Data/2023/stanford_2023_advancedmetrics.csv')

adv_metrics = adv_metrics.drop(index=2)

adv_metrics.to_csv('./Data/2023/stanford_2023_advancedmetrics_altered.csv', index=False)

adv_metrics.head(12)

num_rows, num_columns = adv_metrics.shape

print("Size of Advanced Metrics Data")
print("")
print(f"Number of rows: {num_rows}")
print(f"Number of columns: {num_columns}")

team_stats = pd.read_csv('./Data/2023/stanford_2023_teamstats.csv')

team_stats = team_stats[team_stats['School'] == 'Stanford']

# Initialize a dictionary to collect data by game ID
data = []

# Iterate over each unique game ID
for game_id in team_stats['Game Id'].unique():
    # Filter rows for the current game ID
    game_data = team_stats[team_stats['Game Id'] == game_id]
    
    # Create a dictionary to store all stats for this game
    row = {'Game Id': game_id, 'School': 'Stanford'}
    
    # Loop through each row in this subset to add stats to the dictionary
    for _, stat_row in game_data.iterrows():
        # Use the stat category as the column name and assign the stat value
        stat_category = stat_row['Stat Category']
        stat_value = stat_row['Stat']
        row[stat_category] = stat_value
    
    # Append the constructed row to our data list
    data.append(row)

# Convert the list of dictionaries to a DataFrame
team_stats = pd.DataFrame(data)

team_stats = team_stats.sort_values(by=team_stats.columns[0], ascending=True)

team_stats = team_stats.fillna(0)

team_stats = team_stats.drop(index=8)

team_stats = team_stats.reset_index(drop=True)

team_stats.to_csv('./Data/2023/stanford_2023_teamstats_altered.csv', index=False)

team_stats.head(40)

num_rows, num_columns = team_stats.shape

print("Size of Team Stats Data")
print("")
print(f"Number of rows: {num_rows}")
print(f"Number of columns: {num_columns}")
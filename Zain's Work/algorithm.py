import pandas as pd
import numpy as np

# Load the data
metrics_df = pd.read_csv('./Data/2023/stanford_2023_advancedmetrics_altered.csv')
gamestats_df = pd.read_csv('./Data/2023/stanford_2023_gamestats_altered.csv')
lines_df = pd.read_csv('./Data/2023/stanford_2023_lines_altered.csv')

# Combine relevant data into a single DataFrame, aligned by week
data_df = pd.concat([metrics_df, gamestats_df, lines_df], axis=1)

#Save concatanated data
#data_df.to_csv('concat_stanford_2023.csv',index=False)

# MDP parameters
actions = ['bet', 'no_bet']
bet_amount = 100  # Fixed amount to bet each week
expected_value_threshold = 5  # Expected value threshold for betting (adjustable)

# Initialize variables
total_reward = 0  # Track total profit or loss
rewards = []      # Record cumulative reward outcomes for each week

# Define the reward function based on the bet outcome and odds
def reward(action, odds, outcome):
    if action == 'bet':
        if outcome > 0:  # Win scenario
            if odds > 0:
                return bet_amount * (odds / 100)  # Positive odds (e.g., +150)
            else:
                return bet_amount * (100 / abs(odds))  # Negative odds (e.g., -150)
        else:
            return -bet_amount  # Loss scenario, lose full $100
    return 0  # No reward if no bet

# Function to extract Stanford's moneyline odds and determine game outcome
def get_stanford_moneyline_and_outcome(row):
    if row['HomeTeam'] == 'Stanford':
        odds = row['HomeMoneyline']
        outcome = 1 if row['HomeScore'] > row['AwayScore'] else -1  # 1 if win, -1 if loss
        stanford_elo = row['Home Pregame Elo']
        opponent_elo = row['Away Pregame Elo']
    elif row['AwayTeam'] == 'Stanford':
        odds = row['AwayMoneyline']
        outcome = 1 if row['AwayScore'] > row['HomeScore'] else -1  # 1 if win, -1 if loss
        stanford_elo = row['Away Pregame Elo']
        opponent_elo = row['Home Pregame Elo']
    else:
        odds, outcome, stanford_elo, opponent_elo = None, None, None, None  # This case shouldn't happen based on your dataset
    return odds, outcome, stanford_elo, opponent_elo

# Expected value calculation
def calculate_expected_value(odds, win_prob):
    if odds > 0:
        return bet_amount * (win_prob * (odds / 100) - (1 - win_prob))
    else:
        return bet_amount * (win_prob * (100 / abs(odds)) - (1 - win_prob))

# Simple policy to decide action based on Elo ratings comparison and expected value
def decide_action(row):
    odds, outcome, stanford_elo, opponent_elo = get_stanford_moneyline_and_outcome(row)
    if odds is None:
        return 'no_bet', 0  # Skip if Stanford did not play
    
    # Calculate win probability based on the Elo rating difference
    elo_diff = stanford_elo - opponent_elo
    win_prob = 1 / (1 + 10 ** (-elo_diff / 400))  # Win probability from Elo difference
    
    # Calculate expected value
    ev = calculate_expected_value(odds, win_prob)
    
    # Decision based on expected value
    if ev >= expected_value_threshold:
        return 'bet', odds
    else:
        return 'no_bet', odds

# Simulate sequential decision-making through the season
for week in range(1, len(data_df)):
    current_state = data_df.iloc[:week]  # Include data up to the current week
    next_state = data_df.iloc[week]
    
    # Decide action based on the policy
    action, odds = decide_action(next_state)
    
    # Calculate the reward for this week's action
    odds, outcome, _, _ = get_stanford_moneyline_and_outcome(next_state)
    week_reward = reward(action, odds, outcome)
    total_reward += week_reward
    rewards.append(total_reward)  # Track cumulative reward
    
    # Log action and reward for analysis
    print(f"Week {week}: Action: {action}, Odds: {odds}, Outcome: {outcome}, Cumulative Reward: {total_reward}")

print("Total Cumulative Reward:", total_reward)

import matplotlib.pyplot as plt

# Plotting cumulative reward over weeks
weeks = list(range(1, len(rewards) + 1))
plt.figure(figsize=(10, 5))
plt.plot(weeks, rewards, marker='o', linestyle='-', color='g')
plt.title("Cumulative Reward Over the Season for Stanford Betting (Policy-Based)")
plt.xlabel("Week")
plt.ylabel("Cumulative Reward ($)")
plt.grid(True)
plt.show()
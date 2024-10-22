import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from generate_schedules import generate_schedules

def plot_schedule(schedule_df, title):
    G = nx.DiGraph()

    for _, row in schedule_df.iterrows():
        team1 = row['team1']
        team2 = row['team2']
        G.add_edge(team1, team2)

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=500, font_size=8, font_weight="bold", edge_color="gray", arrows=True)

    # Add title as a text box
    plt.text(0.5, 1.05, title, fontsize=16, ha='center', transform=plt.gca().transAxes)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    schedule_df = generate_schedules()

    # Plot the full season
    plot_schedule(schedule_df, "Full Season Schedule")

    # Plot the schedule up to a specified week
    current_week = 8
    schedule_up_to_week = schedule_df[schedule_df['week'] <= current_week]
    plot_schedule(schedule_up_to_week, f"Schedule up to Week {current_week}")

    # Plot the schedule for a specific week
    schedule_for_week = schedule_df[schedule_df['week'] == current_week]
    plot_schedule(schedule_for_week, f"Schedule for Week {current_week}")
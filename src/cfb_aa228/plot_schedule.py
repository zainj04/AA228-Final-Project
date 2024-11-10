import networkx as nx
import matplotlib.pyplot as plt

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
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from generate_schedules import generate_schedules
from plot_schedule import plot_schedule

def project_proposal():
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
# generates 64 teams with random attributes and predicts outcomes of matches between
# each team based on different attributes. 


import matplotlib.pyplot as plt
import numpy as np
import random

# Define the Team class
class Team:
    def __init__(self, seed, trpt_pct, fg_pct, bpm):
        self.seed = seed  # team seed
        self.trpt_pct = trpt_pct  # turnover percentage
        self.fg_pct = fg_pct  # field goal percentage
        self.bpm = bpm  # box plus minus

    def __repr__(self):
        return (f"Team(seed={self.seed}, "
                f"trpt_pct={self.trpt_pct}, "
                f"fg_pct={self.fg_pct}, "
                f"bpm={self.bpm})")
# generate any number of teams with random attributes and assign them seeds based on BPM
def generate_teams(num_teams):
    teams = []
    for _ in range(num_teams):
        trpt_pct = np.random.uniform(10, 20)
        fg_pct = np.random.uniform(40, 60)
        bpm = np.random.uniform(-5, 10)
        # seeds based on ranking, placeholder for simplicity
        seed = 0
        team = Team(seed, trpt_pct, fg_pct, bpm)
        teams.append(team)
    # Sort teams by bpm in descending order and assign seeds
    teams.sort(key=lambda team: team.bpm, reverse=True)
    for i, team in enumerate(teams):
        team.seed = i // 4 + 1  # Assign seeds based on ranking
    return teams
# plot the teams based on seed and BPM, a higher BPM should correlate with a higher seed
def plot_teams(teams):
    x_values = [team.seed for team in teams]
    y_values = [team.bpm for team in teams]
    
    plt.scatter(x_values, y_values)
    plt.xlabel('Team Seed')
    plt.ylabel('Box Plus Minus (BPM)')
    plt.title('Teams Plot')
    plt.show()




# Define comparison functions based on different metrics
def bySeed(team1, team2):
    r1 = team1.seed * np.random.uniform(0,1)
    r2 = team2.seed * np.random.uniform(0,1)
    if r1 > r2:
        return False
    else:
        return True
    
def byTrptPct(team1, team2):
    r1 = team1.trpt_pct * np.random.uniform(0,1)
    r2 = team2.trpt_pct * np.random.uniform(0,1)   
    if r1 > r2:
        return True
    else:
        return False
    
def byFgPct(team1, team2):
    r1 = team1.fg_pct * np.random.uniform(0,1)
    r2 = team2.fg_pct * np.random.uniform(0,1)
    if r1 > r2:
        return True
    else:
        return False
    
def byBPM(team1, team2):
    r1 = team1.bpm * np.random.uniform(0,1)
    r2 = team2.bpm * np.random.uniform(0,1)
    if r1 > r2:
        return True
    else:
        return False
    
# Simulate the tournament
def simulate_tournament(teams, metric):
    winners = []
    for i in range(32):
        team1 = teams[i]
        team2 = teams[64 - i - 1]
        if metric(team1, team2):
            winners.append(team1)
        else:
            winners.append(team2)
    # Round of 32
    for i in range(16):
        team1 = winners[i]
        team2 = winners[32 - i - 1]
        if metric(team1, team2):
            winners[i] = team1
        else:
            winners[i] = team2
    # Sweet 16
    for i in range(8):
        team1 = winners[i]
        team2 = winners[16 -i - 1]
        if metric(team1, team2):
            winners[i] = team1
        else:
            winners[i] = team2
    # Elite 8
    for i in range(4):
        team1 = winners[i]
        team2 = winners[8 - i - 1]
        if metric(team1, team2):
            winners[i] = team1
        else:
            winners[i] = team2
    # Final 4
    for i in range(2):
        team1 = winners[i]
        team2 = winners[4 - i - 1]
        if metric(team1, team2):
            winners[i] = team1
        else:
            winners[i] = team2
    # Championship
    team1 = winners[0]
    team2 = winners[1]
    if metric(team1, team2):
        winners[0] = team1
    else:
        winners[0] = team2
    return winners[0]

# monte carlo simulation to test the simulation
def monte_carlo_simulation(teams, metric, num_simulations):
    winners = []
    for _ in range(num_simulations):
        winner = simulate_tournament(teams, metric)
        winners.append(winner)
    return winners

# Plots the histograms of the winning team based on different metrics
def plot_histogram(winners, x_values, title):
    #x_values = [team.seed for team in winners]
    plt.hist(x_values, bins=range(1, 65), align='left', rwidth=0.8)
    plt.xlabel('Winning Team Seed')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.show()

# Generate 64 teams
seedW = []
trptW = []
fgW = []
bpmW = []
for i in range(10000):
    teams = generate_teams(64)
    # Simulate the tournament based on different metrics
    seedW.append(simulate_tournament(teams, bySeed))
    trptW.append(simulate_tournament(teams, byTrptPct))
    fgW.append(simulate_tournament(teams, byFgPct))
    bpmW.append(simulate_tournament(teams, byBPM))

# Plot the histograms of winning team based on seed metric
# highest seeds should win more often
plot_histogram(seedW, [team.seed for team in seedW], 'Seed Metric')
# highest turnover percentage should have no effect on win percentage for this simulation
plot_histogram(trptW, [team.seed for team in trptW], 'Turnover Percentage Metric')
# highest field goal percentage should have no effect on win percentage for this simulation
plot_histogram(fgW, [team.seed for team in fgW], 'Field Goal Percentage Metric')
# highest BPM should win more often as seed is based on BPM for the team creation simulation
plot_histogram(bpmW, [team.seed for team in bpmW], 'Box Plus Minus Metric')


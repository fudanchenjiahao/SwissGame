import numpy as np
import random

class Team:
    def __init__(self, id):
        self.id = id
        self.wins = 0
        self.losses = 0
        self.eliminated = False
        self.qualified = False
        self.head_to_head = {}  # Record the head to head results against other teams

    def win(self, opponent_id):
        self.wins += 1
        self.head_to_head[opponent_id] = self.head_to_head.get(opponent_id, 0) + 1

    def lose(self, opponent_id):
        self.losses += 1
        self.head_to_head[opponent_id] = self.head_to_head.get(opponent_id, 0) - 1

def win_probability(team1, team2):
    return 1 / (1 + np.exp(-(team2.id - team1.id) * 0.1))

def simulate_match(team1, team2):
    if random.random() < win_probability(team1, team2):
        team1.win(team2.id)
        team2.lose(team1.id)
    else:
        team2.win(team1.id)
        team1.lose(team2.id)

def group_phase(group):
    for _ in range(2):  # Double round robin
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                simulate_match(group[i], group[j])
                simulate_match(group[j], group[i])

def decide_qualifiers(group):
    group = sorted(group, key=lambda team: (team.wins, sum(team.head_to_head.values())), reverse=True)
    group[0].qualified = True
    group[1].qualified = True
    group[2].eliminated = True
    group[3].eliminated = True

def group_stage_simulation():
    teams = [Team(i+1) for i in range(16)]
    random.shuffle(teams)
    groups = [teams[i:i+4] for i in range(0, len(teams), 4)]
    for group in groups:
        group_phase(group)
        decide_qualifiers(group)

    qualified_teams = [team for team in teams if team.qualified]
    eliminated_teams = [team for team in teams if team.eliminated]

    return [team.id for team in qualified_teams], [team.id for team in eliminated_teams]

def simulate_group_stage_multiple_times(n=100000):
    count = {i: 0 for i in range(1, 17)}
    for _ in range(n):
        qualified, _ = group_stage_simulation()
        for team_id in qualified:
            count[team_id] += 1

    probabilities = {team_id: count_val/n for team_id, count_val in count.items()}
    return probabilities

probabilities = simulate_group_stage_multiple_times()
print(probabilities)













import numpy as np
import random
def win_probability(team1, team2):
    return 1 / (1 + np.exp(-(team2.id - team1.id) * 0.1))

class Team:
    def __init__(self, id):
        self.id = id
        self.wins = 0
        self.losses = 0
        self.eliminated = False
        self.qualified = False

    def win(self):
        self.wins += 1
        if self.wins == 3:
            self.qualified = True

    def lose(self):
        self.losses += 1
        if self.losses == 3:
            self.eliminated = True





def simulate_match(team1, team2, best_of_three=False):
    if best_of_three:
        team1_wins = 0
        team2_wins = 0
        for _ in range(3):
            if random.random() < win_probability(team1, team2):
                team1_wins += 1
            else:
                team2_wins += 1
            if team1_wins == 2:
                team1.win()
                team2.lose()
                return
            if team2_wins == 2:
                team2.win()
                team1.lose()
                return
    else:
        if random.random() < win_probability(team1, team2):
            team1.win()
            team2.lose()
        else:
            team2.win()
            team1.lose()


def simulate_round(teams):
    teams = sorted(teams, key=lambda x: x.wins, reverse=True)
    grouped_teams = []
    buffer_group = []
    current_wins = teams[0].wins
    for team in teams:
        if team.wins == current_wins:
            buffer_group.append(team)
        else:
            random.shuffle(buffer_group)
            grouped_teams.extend(buffer_group)
            buffer_group = [team]
            current_wins = team.wins
    if buffer_group:
        random.shuffle(buffer_group)
        grouped_teams.extend(buffer_group)

    for i in range(0, len(grouped_teams), 2):
        team1 = grouped_teams[i]
        team2 = grouped_teams[i + 1]
        best_of_three = team1.wins >= 2 or team1.losses >= 2 or team2.wins >= 2 or team2.losses >= 2
        simulate_match(team1, team2, best_of_three)


def swiss_simulation():
    teams = [Team(i + 1) for i in range(16)]
    qualified_teams = []
    eliminated_teams = []

    for round_num in range(5):
        if len(qualified_teams) == 8:
            break
        playing_teams = [team for team in teams if not team.qualified and not team.eliminated]
        simulate_round(playing_teams)
        qualified_teams = [team for team in teams if team.qualified]
        eliminated_teams = [team for team in teams if team.eliminated]

    return [team.id for team in qualified_teams], [team.id for team in eliminated_teams]


# Integrating all the code together including the simulate_many_times function

def simulate_many_times(n=100000):
    counts = {i + 1: 0 for i in range(16)}  # Initialize counts for each team

    for _ in range(n):
        qualified, _ = swiss_simulation()
        for team_id in qualified:
            counts[team_id] += 1

    probabilities = {team_id: count / n for team_id, count in counts.items()}
    return probabilities


# Now running the simulation 1000 times
probabilities = simulate_many_times()


# Simulate 1000 times
probabilities = simulate_many_times()

print(probabilities)

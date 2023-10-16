# Merging all the code together

import numpy as np
import random


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


def win_probability(team1, team2):
    # Calculate the win probability for team1 using the sigmoid function
    return 1 / (1 + np.exp(-(team2.id - team1.id) * 0.15))


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


def modified_swiss_simulation():
    teams = [Team(i + 1) for i in range(16)]
    random.shuffle(teams)  # Shuffle teams for the first round

    # Find opponent of team 6 in the first round
    opponent_of_6 = None
    for i in range(0, 16, 2):
        if teams[i].id == 6:
            opponent_of_6 = teams[i + 1].id
        elif teams[i + 1].id == 6:
            opponent_of_6 = teams[i].id

    qualified_teams = []
    eliminated_teams = []

    for round_num in range(5):
        if len(qualified_teams) == 8:
            break
        playing_teams = [team for team in teams if not team.qualified and not team.eliminated]
        simulate_round(playing_teams)
        qualified_teams = [team for team in teams if team.qualified]
        eliminated_teams = [team for team in teams if team.eliminated]

    is_team_6_qualified = 6 in [team.id for team in qualified_teams]

    return opponent_of_6, is_team_6_qualified


def simulate_with_opponent(n=300000):
    opponent_counts = {i + 1: 0 for i in range(16) if i + 1 != 6}  # Excluding team 6
    qualified_counts = {i + 1: 0 for i in range(16) if i + 1 != 6}

    for _ in range(n):
        opponent, is_qualified = modified_swiss_simulation()
        opponent_counts[opponent] += 1
        if is_qualified:
            qualified_counts[opponent] += 1

    probabilities_given_opponent = {team_id: qualified_counts[team_id] / opponent_counts[team_id] for team_id in
                                    opponent_counts}

    return opponent_counts, qualified_counts, probabilities_given_opponent


opponent_counts, qualified_counts, probabilities_given_opponent = simulate_with_opponent()

print(opponent_counts, qualified_counts, '\n',probabilities_given_opponent)


#%%

import numpy as np
from tabulate import tabulate

class Game2x2:
    def __init__(self, payoff_matrix_p1, payoff_matrix_p2):
        """
        Initialize a 2x2 game.
        
        Args:
            payoff_matrix_p1: 2x2 numpy array for player 1's payoffs
            payoff_matrix_p2: 2x2 numpy array for player 2's payoffs
        """
        self.payoffs_p1 = np.array(payoff_matrix_p1)
        self.payoffs_p2 = np.array(payoff_matrix_p2)
        self.num_strategies = (2, 2)  # (player1_strategies, player2_strategies)
    
    def __repr__(self):
        return f"2x2 Game:\nPlayer 1 payoffs:\n{self.payoffs_p1}\nPlayer 2 payoffs:\n{self.payoffs_p2}"
    
    def pretty_print(self):
        """Print the game as a nice payoff matrix grid"""
        # Create the payoff cells as (p1_payoff, p2_payoff)
        grid = []
        for i in range(2):
            row = []
            for j in range(2):
                cell = f"({self.payoffs_p1[i,j]}, {self.payoffs_p2[i,j]})"
                row.append(cell)
            grid.append(row)
        
        print("Game Payoff Matrix:")
        print("(Player 1 payoff, Player 2 payoff)")
        print(tabulate(grid, 
                        headers=["P2: Strategy 0", "P2: Strategy 1"], 
                        showindex=["P1: Strategy 0", "P1: Strategy 1"], 
                        tablefmt="grid"))

# Create some classic games
def prisoners_dilemma():
    p1_payoffs = [
        [3, 0], 
        [5, 1]
        ]  # Cooperate, Defect
    p2_payoffs = [
        [3, 5], 
        [0, 1]
        ]
    return Game2x2(p1_payoffs, p2_payoffs)

def battle_of_sexes():
    p1_payoffs = [
        [2, 0], 
        [0, 1]
    ]  # Opera, Football
    p2_payoffs = [
        [1, 0], 
        [0, 2]
    ]
    return Game2x2(p1_payoffs, p2_payoffs)

def rand_strategy_game():
    p1_payoffs = np.random.randint(0, 10, (2, 2))
    p2_payoffs = np.random.randint(0, 10, (2, 2))
    return Game2x2(p1_payoffs, p2_payoffs)

def rand_strategy(Game):
    p1_strat = np.random.rand(Game.num_strategies[0])
    p1_strat /= p1_strat.sum()
    
    p2_strat = np.random.rand(Game.num_strategies[1])
    p2_strat /= p2_strat.sum()

    return p1_strat, p2_strat

def best_response(Game, opponent_strat, player=1):
    if player == 1:
        expected_payoffs = Game.payoffs_p1 @ opponent_strat
    else:
        expected_payoffs = Game.payoffs_p2.T @ opponent_strat
    
    best_response = np.zeros_like(expected_payoffs)
    best_response[np.argmax(expected_payoffs)] = 1
    return best_response


#%%

game = rand_strategy_game()
print("Random Game:")
game.pretty_print()


player1, player2 = rand_strategy(game)
print("Player 2 Strategy:")
print(player2)

previous_states = list()
for i in range(5):
    player1 = best_response(game, player2, player=1)
    print(f"Player 1 best response: {player1} to {player2}" )
    player2 = best_response(game, player1, player=2)
    print(f"Player 2 best response: {player2} to {player1}" )
    state = (tuple(player1), tuple(player2))
    if state in previous_states:
        if previous_states[-1] == state:
            print("Convergence detected.")
          

            p1_strategy = np.argmax(player1)
            p2_strategy = np.argmax(player2)

            print(f"Converged to P1: {p1_strategy}, P2: {p2_strategy}")
            # Create a visual grid
            grid = [[".", "."], [".", "."]]
            grid[p1_strategy][p2_strategy] = "X"
            
            print("Converged to position:")
            print(tabulate(grid, headers=["P2 Strat 0", "P2 Strat 1"], 
                          showindex=["P1 Strat 0", "P1 Strat 1"], tablefmt="grid"))
        else:
            print("Cycle detected.")
            print(f"Cycled through: \n{previous_states}")
        break
    previous_states.append(state)

# Best Response Runner



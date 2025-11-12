import os
import statistics

from tqdm import tqdm

from lab_2a import create_random_agent
from lab_2b import create_fixed_agent
from libs.agent import Agent
from libs.hand_evaluation import analyse_hand
from libs.poker_game import PokerGame
from plotting_utils import generate_all_plots


def create_reflex_agent(name: str) -> Agent:

    class ReflexAgent(Agent):
        """
        Bidding strategy:
        - Maps hand score (1-39) to bid amount (0-50)
        - Uses linear scaling: bid = (hand_score / 39) * 50
        """

        def make_bid(self, phase, own_bids, opponent_bids):
            """
            Make a bid decision based on hand strength.
            """
            if self.hand is None:
                return 0
            hand_score = analyse_hand(self.hand)
            return max(0, min(50, int((hand_score / 39.0) * 50)))

    return ReflexAgent(name)


def run_experiment(agent1_factory, agent2_factory, agent1_name, agent2_name,
                   num_games=100, num_hands=50):
    """
    Run multiple games between two agents.
    """
    differences = []
    agent1_winnings = []
    agent2_winnings = []

    print(f"Running {num_games} games ({num_hands} hands per game)...")
    print(f"  {agent1_name} vs {agent2_name}")
    print("-" * 70)

    for _ in tqdm(
        range(num_games),
        desc=f"Games ({agent1_name} vs {agent2_name})",
        unit="game"
    ):
        # Create a new game with fresh agents
        game = PokerGame(
            agent1_factory=agent1_factory,
            agent2_factory=agent2_factory,
            num_hands=num_hands
        )

        # Play the game
        game_result = game.play_game()

        # Calculate difference (Agent1 - Agent2)
        diff = game_result['difference']
        differences.append(diff)
        agent1_winnings.append(game_result['agent1_winnings'])
        agent2_winnings.append(game_result['agent2_winnings'])

    # Calculate statistics
    mean_diff = statistics.mean(differences)
    std_diff = statistics.stdev(differences) if len(differences) > 1 else 0
    mean_agent1 = statistics.mean(agent1_winnings)
    mean_agent2 = statistics.mean(agent2_winnings)

    return {
        'differences': differences,
        'agent1_winnings': agent1_winnings,
        'agent2_winnings': agent2_winnings,
        'mean_difference': mean_diff,
        'std_difference': std_diff,
        'mean_agent1_winnings': mean_agent1,
        'mean_agent2_winnings': mean_agent2,
        'num_games': num_games,
        'num_hands': num_hands,
        'agent1_name': agent1_name,
        'agent2_name': agent2_name
    }


if __name__ == "__main__":
    print("-" * 70)
    print("Lab 2e: Reflex Agent Implementation and Comparison")
    print("-" * 70)

    # Experiment 1: Reflex Agent vs Random Agent
    print("\n" + "-" * 70)
    print("EXPERIMENT 1: Reflex Agent vs Random Agent")
    print("-" * 70)

    results1 = run_experiment(
        agent1_factory=lambda: create_reflex_agent("Reflex Agent"),
        agent2_factory=lambda: create_random_agent("Random Agent"),
        agent1_name="Reflex Agent",
        agent2_name="Random Agent",
        num_games=100,
        num_hands=50)

    # Generate plots for Experiment 1
    plots_dir = os.path.join(os.path.dirname(__file__), '..', 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    generate_all_plots(results1, plots_dir, 'lab_2e')

    # Experiment 2: Reflex Agent vs Fixed Agent
    print("\n\n" + "-" * 70)
    print("EXPERIMENT 2: Reflex Agent vs Fixed Agent")
    print("-" * 70)

    results2 = run_experiment(
        agent1_factory=lambda: create_reflex_agent("Reflex Agent"),
        agent2_factory=lambda: create_fixed_agent("Fixed Agent"),
        agent1_name="Reflex Agent",
        agent2_name="Fixed Agent",
        num_games=100,
        num_hands=50)

    # Generate plots for Experiment 2
    generate_all_plots(results2, plots_dir, 'lab_2e_e2')

    # Summary
    print("-" * 70)
    print("Experiment complete!")
    print("-" * 70)

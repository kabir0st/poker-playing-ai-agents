import os
import statistics

from tqdm import tqdm

from lab_2a import create_random_agent  # noqa: E402
from lab_2b import create_fixed_agent  # noqa: E402
from libs.poker_game import PokerGame  # noqa: E402
from plotting_utils import generate_all_plots  # noqa: E402


def run_experiment(num_games: int = 100,
                   num_hands: int = 50,
                   fixed_bid_amount: int = 25) -> dict:
    """
    Run multiple games between random and fixed agents.
    """
    differences = []
    random_winnings = []
    fixed_winnings = []

    print(f"Running {num_games} games ({num_hands} hands per game)...")
    print("-" * 70)

    for _ in tqdm(range(num_games), desc="Playing games", unit="game"):
        # Create a new game with fresh agents
        game = PokerGame(
            agent1_factory=lambda: create_random_agent("Random Agent"),
            agent2_factory=lambda: create_fixed_agent("Fixed Agent",
                                                      fixed_bid_amount),
            num_hands=num_hands)

        # Play the game
        game_result = game.play_game()

        # Calculate difference (Random Agent - Fixed Agent)
        diff = game_result['difference']
        differences.append(diff)
        random_winnings.append(game_result['agent1_winnings'])
        fixed_winnings.append(game_result['agent2_winnings'])

    # Calculate statistics
    mean_diff = statistics.mean(differences)
    std_diff = statistics.stdev(differences) if len(differences) > 1 else 0
    mean_random = statistics.mean(random_winnings)
    mean_fixed = statistics.mean(fixed_winnings)

    return {
        'differences': differences,
        'agent1_winnings': random_winnings,
        'agent2_winnings': fixed_winnings,
        'mean_difference': mean_diff,
        'std_difference': std_diff,
        'mean_agent1_winnings': mean_random,
        'mean_agent2_winnings': mean_fixed,
        'num_games': num_games,
        'num_hands': num_hands,
        'agent1_name': 'Random Agent',
        'agent2_name': 'Fixed Agent',
        'fixed_bid_amount': fixed_bid_amount
    }


if __name__ == "__main__":
    print("-" * 70)
    print("Lab 2d: Random Agent vs Fixed Agent Analysis")
    print("-" * 70)

    # Run experiment: 100 games, 50 hands per game
    print("\nRunning experiment with 100 games...")
    results = run_experiment(num_games=10000, fixed_bid_amount=17)

    # Generate plots
    plots_dir = os.path.join(os.path.dirname(__file__), '..', 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    generate_all_plots(results, plots_dir, 'lab_2d_random_vs_fixed')

    print("\n" + "-" * 70)
    print("Experiment complete!")
    print(f"Plots saved to: {plots_dir}")
    print("-" * 70)

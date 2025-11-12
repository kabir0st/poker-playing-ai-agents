"""Lab 2d: Analyze random agent vs fixed agent performance."""

import os
import random
import statistics
import sys

# Add parent directory to path to import libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lab_2a import create_random_agent  # noqa: E402
from lab_2b import create_fixed_agent  # noqa: E402
from libs.poker_game import PokerGame  # noqa: E402


def run_experiment(num_games=100, num_hands=50, fixed_bid_amount=25):
    """
    Run multiple games between random and fixed agents.

    Parameters
    ----------
    num_games : int
        Number of games to play (default: 100)
    num_hands : int
        Number of hands per game (default: 50)
    fixed_bid_amount : int
        Fixed bid amount for the fixed agent (default: 25)

    Returns
    -------
    dict
        Dictionary containing statistics and results
    """
    differences = []
    random_winnings = []
    fixed_winnings = []

    print(f"Running {num_games} games ({num_hands} hands per game)...")
    print("=" * 70)

    for game_num in range(1, num_games + 1):
        # Create a new game with fresh agents
        game = PokerGame(
            agent1_factory=lambda: create_random_agent("Random Agent"),
            agent2_factory=lambda: create_fixed_agent("Fixed Agent", fixed_bid_amount),
            num_hands=num_hands
        )

        # Play the game
        game_result = game.play_game()

        # Calculate difference (Random Agent - Fixed Agent)
        diff = game_result['difference']
        differences.append(diff)
        random_winnings.append(game_result['agent1_winnings'])
        fixed_winnings.append(game_result['agent2_winnings'])

        # Progress indicator
        if game_num % 10 == 0:
            print(f"Completed {game_num}/{num_games} games...")

    # Calculate statistics
    mean_diff = statistics.mean(differences)
    std_diff = statistics.stdev(differences) if len(differences) > 1 else 0
    mean_random = statistics.mean(random_winnings)
    mean_fixed = statistics.mean(fixed_winnings)

    return {
        'differences': differences,
        'random_winnings': random_winnings,
        'fixed_winnings': fixed_winnings,
        'mean_difference': mean_diff,
        'std_difference': std_diff,
        'mean_random_winnings': mean_random,
        'mean_fixed_winnings': mean_fixed,
        'num_games': num_games,
        'num_hands': num_hands,
        'fixed_bid_amount': fixed_bid_amount
    }


def analyze_results(results):
    """
    Analyze and print the results of the experiment.

    Parameters
    ----------
    results : dict
        Results dictionary from run_experiment
    """
    print("\n" + "=" * 70)
    print("EXPERIMENTAL RESULTS")
    print("=" * 70)

    print(f"\nConfiguration:")
    print(f"  Number of games: {results['num_games']}")
    print(f"  Hands per game: {results['num_hands']}")
    print(f"  Total hands played: {results['num_games'] * results['num_hands']}")

    print(f"\nBankroll Difference Statistics (Random Agent - Fixed Agent):")
    print(f"  Mean difference: ${results['mean_difference']:.2f}")
    print(f"  Standard deviation: ${results['std_difference']:.2f}")

    print(f"\nAverage Winnings per Game:")
    print(f"  Random Agent: ${results['mean_random_winnings']:.2f}")
    print(f"  Fixed Agent: ${results['mean_fixed_winnings']:.2f}")

    # Determine which agent is better
    mean_diff = results['mean_difference']
    std_diff = results['std_difference']

    print(f"\n" + "=" * 70)
    print("ANALYSIS")
    print("=" * 70)

    if mean_diff > 0:
        better_agent = "Random Agent"
        worse_agent = "Fixed Agent"
    elif mean_diff < 0:
        better_agent = "Fixed Agent"
        worse_agent = "Random Agent"
    else:
        print("\nThe agents perform equally well on average.")
        return

    print(f"\nWhich agent is better?")
    print(f"  {better_agent} is better on average.")
    print(f"  Average advantage: ${abs(mean_diff):.2f} per game")

    print(f"\nWhy?")
    print(f"  The mean bankroll difference is ${mean_diff:.2f}, meaning {better_agent}")
    print(f"  wins ${abs(mean_diff):.2f} more per game on average than {worse_agent}.")

    # Additional insights
    print(f"\nAdditional Insights:")
    print(f"  1. Standard deviation of ${std_diff:.2f} indicates the variability")
    print(f"     in outcomes across games.")

    if abs(mean_diff) > 2 * std_diff:
        print(f"  2. The difference is statistically significant (mean > 2*std),")
        print(f"     suggesting a consistent advantage for {better_agent}.")
    else:
        print(f"  2. The difference is relatively small compared to variability,")
        print(f"     suggesting the advantage may not be consistent.")

    # Strategy analysis
    print(f"\nStrategy Analysis:")
    print(f"  Random Agent Strategy:")
    print(f"    - Bids randomly between $0-$50 each phase")
    print(f"    - Average bid per phase: ~$25 (uniform distribution)")
    print(f"    - Total average bid per hand: ~$75 (3 phases)")

    print(f"  Fixed Agent Strategy:")
    fixed_bid = results.get('fixed_bid_amount', 25)
    print(f"    - Always bids ${fixed_bid} each phase")
    print(f"    - Total bid per hand: ${fixed_bid * 3} (3 phases)")

    print(f"\n  Key Difference:")
    if mean_diff > 0:
        print(f"    Random agent's variable bidding may allow it to:")
        print(f"    - Bid higher when it has strong hands (though it doesn't know)")
        print(f"    - Bid lower when it has weak hands (by chance)")
        print(f"    However, since random agent doesn't use hand information,")
        print(f"    this advantage is purely coincidental.")
    else:
        print(f"    Fixed agent's consistent strategy provides:")
        print(f"    - Predictable pot sizes")
        print(f"    - No risk of over-bidding on weak hands")
        print(f"    - No risk of under-bidding on strong hands")
        print(f"    Since both agents are equally likely to get good/bad hands,")
        print(f"    the fixed strategy may be more stable.")


if __name__ == "__main__":
    # Set random seed for reproducibility (optional)
    # random.seed(42)

    # Run experiment: 100 games, 50 hands per game
    results = run_experiment(num_games=100, num_hands=50, fixed_bid_amount=25)

    # Analyze and print results
    analyze_results(results)

    print("\n" + "=" * 70)
    print("Experiment complete!")
    print("=" * 70)


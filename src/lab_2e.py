"""Lab 2e: Implement a simple reflex agent and compare it with random and fixed agents."""

import os
import statistics
import sys

# Add parent directory to path to import libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lab_2a import create_random_agent  # noqa: E402
from lab_2b import create_fixed_agent  # noqa: E402
from libs.agent import Agent  # noqa: E402
from libs.hand_evaluation import analyse_hand  # noqa: E402
from libs.poker_game import PokerGame  # noqa: E402
from plotting_utils import generate_all_plots  # noqa: E402


def create_reflex_agent(name):
    """
    Create a reflex agent that makes betting decisions based on hand strength.

    Task 2e: Implement a simple reflex agent.

    The reflex agent evaluates its hand strength and bids proportionally:
    - Strong hands (high score) -> higher bids
    - Weak hands (low score) -> lower bids

    Parameters
    ----------
    name : str
        Name of the agent

    Returns
    -------
    Agent
        A ReflexAgent instance
    """
    class ReflexAgent(Agent):
        """
        A reflex agent that bids based on hand strength.

        Hand scores range from 1-39:
        - High cards: 1-13
        - Pairs: 14-26
        - Three of a kind: 27-39

        Bidding strategy:
        - Maps hand score (1-39) to bid amount (0-50)
        - Uses linear scaling: bid = (hand_score / 39) * 50
        """

        def make_bid(self, phase, own_bids, opponent_bids):
            """
            Make a bid decision based on hand strength.

            Parameters
            ----------
            phase : int
                Current bidding phase (1, 2, or 3)
            own_bids : list
                List of own previous bids
            opponent_bids : list
                List of opponent's previous bids

            Returns
            -------
            int : bid amount ($0-50)
            """
            if self.hand is None:
                # If no hand received yet, bid minimum
                return 0

            # Evaluate hand strength (score ranges from 1-39)
            hand_score = analyse_hand(self.hand)

            # Map hand score (1-39) to bid amount (0-50)
            # Linear scaling: stronger hands bid more
            # Formula: bid = (hand_score / 39) * 50
            bid = int((hand_score / 39.0) * 50)

            # Ensure bid is within valid range [0, 50]
            bid = max(0, min(50, bid))

            return bid

        def observe_showdown(self, opponent_hand):
            """
            Observe opponent's hand during showdown phase.

            The reflex agent could use this information to learn,
            but for now we'll keep it simple and not use it.
            """
            pass  # Simple reflex agent doesn't learn from past games

    return ReflexAgent(name)


def run_experiment(agent1_factory, agent2_factory, agent1_name, agent2_name,
                   num_games=100, num_hands=50):
    """
    Run multiple games between two agents.

    Parameters
    ----------
    agent1_factory : callable
        Function that returns an Agent instance for player 1
    agent2_factory : callable
        Function that returns an Agent instance for player 2
    agent1_name : str
        Name of agent 1
    agent2_name : str
        Name of agent 2
    num_games : int
        Number of games to play (default: 100)
    num_hands : int
        Number of hands per game (default: 50)

    Returns
    -------
    dict
        Dictionary containing statistics and results
    """
    differences = []
    agent1_winnings = []
    agent2_winnings = []

    print(f"Running {num_games} games ({num_hands} hands per game)...")
    print(f"  {agent1_name} vs {agent2_name}")
    print("=" * 70)

    for game_num in range(1, num_games + 1):
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

        # Progress indicator
        if game_num % 10 == 0:
            print(f"Completed {game_num}/{num_games} games...")

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

    agent1_name = results['agent1_name']
    agent2_name = results['agent2_name']

    print(f"\nBankroll Difference Statistics ({agent1_name} - {agent2_name}):")
    print(f"  Mean difference: ${results['mean_difference']:.2f}")
    print(f"  Standard deviation: ${results['std_difference']:.2f}")

    print(f"\nAverage Winnings per Game:")
    print(f"  {agent1_name}: ${results['mean_agent1_winnings']:.2f}")
    print(f"  {agent2_name}: ${results['mean_agent2_winnings']:.2f}")

    # Determine which agent is better
    mean_diff = results['mean_difference']
    std_diff = results['std_difference']

    print(f"\n" + "=" * 70)
    print("ANALYSIS")
    print("=" * 70)

    if mean_diff > 0:
        better_agent = agent1_name
        worse_agent = agent2_name
    elif mean_diff < 0:
        better_agent = agent2_name
        worse_agent = agent1_name
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
    if "Reflex" in agent1_name:
        print(f"  {agent1_name} Strategy:")
        print(f"    - Evaluates hand strength (score 1-39)")
        print(f"    - Bids proportionally: bid = (hand_score / 39) * 50")
        print(f"    - Strong hands (27-39) bid high ($35-$50)")
        print(f"    - Medium hands (14-26) bid medium ($18-$33)")
        print(f"    - Weak hands (1-13) bid low ($1-$16)")
    elif "Random" in agent1_name:
        print(f"  {agent1_name} Strategy:")
        print(f"    - Bids randomly between $0-$50 each phase")
        print(f"    - Average bid per phase: ~$25 (uniform distribution)")
    elif "Fixed" in agent1_name:
        print(f"  {agent1_name} Strategy:")
        print(f"    - Always bids a fixed amount each phase")

    if "Reflex" in agent2_name:
        print(f"  {agent2_name} Strategy:")
        print(f"    - Evaluates hand strength (score 1-39)")
        print(f"    - Bids proportionally: bid = (hand_score / 39) * 50")
        print(f"    - Strong hands (27-39) bid high ($35-$50)")
        print(f"    - Medium hands (14-26) bid medium ($18-$33)")
        print(f"    - Weak hands (1-13) bid low ($1-$16)")
    elif "Random" in agent2_name:
        print(f"  {agent2_name} Strategy:")
        print(f"    - Bids randomly between $0-$50 each phase")
        print(f"    - Average bid per phase: ~$25 (uniform distribution)")
    elif "Fixed" in agent2_name:
        print(f"  {agent2_name} Strategy:")
        print(f"    - Always bids a fixed amount each phase")


def demonstrate_reflex_agent():
    """Demonstrate how the reflex agent bids based on hand strength."""
    print("=" * 70)
    print("Reflex Agent Demonstration")
    print("=" * 70)

    reflex_agent = create_reflex_agent("Reflex Agent")

    # Test with different hand types
    test_hands = [
        (["2s", "3h", "4c"], "Weak high card"),
        (["Ks", "Qh", "Jc"], "Strong high card"),
        (["5s", "5h", "2c"], "Weak pair"),
        (["As", "Ah", "2c"], "Strong pair"),
        (["7s", "7h", "7c"], "Three of a kind"),
        (["As", "Ah", "Ac"], "Strongest hand"),
    ]

    print("\nBidding behavior for different hand strengths:")
    print("-" * 70)

    for hand, description in test_hands:
        reflex_agent.receive_hand(hand)
        hand_score = analyse_hand(hand)
        bid = reflex_agent.make_bid(1, [], [])
        print(f"{description:20s} | Hand: {hand} | Score: {hand_score:2d} | Bid: ${bid:2d}")

    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    print("=" * 70)
    print("Lab 2e: Reflex Agent Implementation and Comparison")
    print("=" * 70)

    # Demonstrate reflex agent behavior
    demonstrate_reflex_agent()

    # Experiment 1: Reflex Agent vs Random Agent
    print("\n" + "=" * 70)
    print("EXPERIMENT 1: Reflex Agent vs Random Agent")
    print("=" * 70)

    results1 = run_experiment(
        agent1_factory=lambda: create_reflex_agent("Reflex Agent"),
        agent2_factory=lambda: create_random_agent("Random Agent"),
        agent1_name="Reflex Agent",
        agent2_name="Random Agent",
        num_games=100,
        num_hands=50
    )

    analyze_results(results1)

    # Generate plots for Experiment 1
    plots_dir = os.path.join(os.path.dirname(__file__), '..', 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    generate_all_plots(results1, plots_dir, 'lab_2e_experiment1_reflex_vs_random')

    # Experiment 2: Reflex Agent vs Fixed Agent
    print("\n\n" + "=" * 70)
    print("EXPERIMENT 2: Reflex Agent vs Fixed Agent")
    print("=" * 70)

    results2 = run_experiment(
        agent1_factory=lambda: create_reflex_agent("Reflex Agent"),
        agent2_factory=lambda: create_fixed_agent("Fixed Agent", fixed_bid_amount=25),
        agent1_name="Reflex Agent",
        agent2_name="Fixed Agent",
        num_games=100,
        num_hands=50
    )

    analyze_results(results2)

    # Generate plots for Experiment 2
    generate_all_plots(results2, plots_dir, 'lab_2e_experiment2_reflex_vs_fixed')

    # Summary
    print("\n\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("\nReflex Agent Performance:")
    print(f"  vs Random Agent: ${results1['mean_difference']:.2f} advantage")
    print(f"  vs Fixed Agent: ${results2['mean_difference']:.2f} advantage")

    if results1['mean_difference'] > 0 and results2['mean_difference'] > 0:
        print("\n✓ Reflex Agent performs better than both Random and Fixed agents!")
        print("  This demonstrates that using hand strength information improves")
        print("  betting decisions compared to random or fixed strategies.")
    elif results1['mean_difference'] > 0 or results2['mean_difference'] > 0:
        print("\n✓ Reflex Agent shows improvement in at least one comparison.")
    else:
        print("\n⚠ Reflex Agent did not outperform both opponents.")
        print("  This may indicate the need for strategy refinement.")

    print("\n" + "=" * 70)
    print("Experiment complete!")
    print("=" * 70)


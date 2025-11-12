"""Lab 2f: Implement a reflex agent with memory and compare with reflex agent without memory."""

import os
import statistics
import sys

# Add parent directory to path to import libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lab_2e import create_reflex_agent  # noqa: E402
from libs.agent import Agent  # noqa: E402
from libs.hand_evaluation import analyse_hand  # noqa: E402
from libs.poker_game import PokerGame  # noqa: E402
from plotting_utils import generate_all_plots  # noqa: E402


def create_reflex_agent_with_memory(name):
    """
    Create a reflex agent with memory that considers opponent bidding history.

    The agent makes betting decisions based on:
    1. Current hand strength
    2. Opponent's last bid amount

    Strategy:
    - Base bid from hand strength (like reflex agent)
    - Adjust based on opponent's last bid:
      * High opponent bid -> opponent might have strong hand -> be cautious
      * Low opponent bid -> opponent might have weak hand -> be more aggressive

    Parameters
    ----------
    name : str
        Name of the agent

    Returns
    -------
    Agent
        A ReflexAgentWithMemory instance
    """
    class ReflexAgentWithMemory(Agent):
        """
        A reflex agent with memory that uses opponent bidding information.

        Hand scores range from 1-39:
        - High cards: 1-13
        - Pairs: 14-26
        - Three of a kind: 27-39

        Bidding strategy:
        - Base bid from hand strength: bid = (hand_score / 39) * 50
        - Adjust based on opponent's last bid:
          * If opponent bid high (>30), reduce bid (they might be strong)
          * If opponent bid low (<20), increase bid (they might be weak)
        """

        def make_bid(self, phase, own_bids, opponent_bids):
            """
            Make a bid decision based on hand strength and opponent's last bid.

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

            # Base bid from hand strength
            # Linear scaling: stronger hands bid more
            base_bid = (hand_score / 39.0) * 50

            # Adjust based on opponent's last bid (if available)
            adjustment = 0
            if opponent_bids:  # If opponent has bid in previous phases
                last_opponent_bid = opponent_bids[-1]

                # Analyze opponent's bidding pattern
                # High bid (>30) suggests strong hand -> be cautious
                # Low bid (<20) suggests weak hand -> be more aggressive

                if last_opponent_bid > 30:
                    # Opponent bid high - they might have a strong hand
                    # Reduce our bid slightly to avoid overcommitting
                    adjustment = -5
                elif last_opponent_bid < 20:
                    # Opponent bid low - they might have a weak hand
                    # Increase our bid to capitalize on their weakness
                    adjustment = +5
                # If opponent bid between 20-30, no adjustment (neutral)

            # Apply adjustment
            bid = base_bid + adjustment

            # Ensure bid is within valid range [0, 50]
            bid = max(0, min(50, int(bid)))

            return bid

        def observe_showdown(self, opponent_hand):
            """
            Observe opponent's hand during showdown phase.

            Could potentially learn from this, but for now we'll keep it simple.
            """
            pass

    return ReflexAgentWithMemory(name)


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
        advantage = mean_diff
    elif mean_diff < 0:
        better_agent = agent2_name
        worse_agent = agent1_name
        advantage = abs(mean_diff)
    else:
        print("\nThe agents perform equally well on average.")
        return

    print(f"\nWhich agent is better?")
    print(f"  {better_agent} is better on average.")
    print(f"  Average advantage: ${advantage:.2f} per game")

    print(f"\nWhy?")
    print(f"  The mean bankroll difference is ${results['mean_difference']:.2f}, meaning {better_agent}")
    print(f"  wins ${advantage:.2f} more per game on average than {worse_agent}.")

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
    print(f"\nStrategy Comparison:")

    # Agent 1 strategy
    print(f"  {agent1_name} Strategy:")
    if "(Memory)" in agent1_name or ("Memory" in agent1_name and "No Memory" not in agent1_name):
        print(f"    - Base bid from hand strength (like reflex agent)")
        print(f"    - Adjusts bid based on opponent's last bid:")
        print(f"      * Opponent bid > $30: reduce bid by $5 (cautious)")
        print(f"      * Opponent bid < $20: increase bid by $5 (aggressive)")
        print(f"      * Opponent bid $20-$30: no adjustment")
    else:
        print(f"    - Bids based solely on hand strength")
        print(f"    - Formula: bid = (hand_score / 39) * 50")
        print(f"    - Does not consider opponent bidding")

    # Agent 2 strategy
    print(f"\n  {agent2_name} Strategy:")
    if "(Memory)" in agent2_name or ("Memory" in agent2_name and "No Memory" not in agent2_name):
        print(f"    - Base bid from hand strength (like reflex agent)")
        print(f"    - Adjusts bid based on opponent's last bid:")
        print(f"      * Opponent bid > $30: reduce bid by $5 (cautious)")
        print(f"      * Opponent bid < $20: increase bid by $5 (aggressive)")
        print(f"      * Opponent bid $20-$30: no adjustment")
    else:
        print(f"    - Bids based solely on hand strength")
        print(f"    - Formula: bid = (hand_score / 39) * 50")
        print(f"    - Does not consider opponent bidding")


def analyze_memory_effectiveness(results):
    """
    Analyze why memory agent performs better or worse.

    Parameters
    ----------
    results : dict
        Results dictionary from run_experiment
    """
    mean_diff = results['mean_difference']
    memory_agent_name = results['agent1_name'] if "Memory" in results['agent1_name'] else results['agent2_name']
    reflex_agent_name = results['agent2_name'] if "Memory" in results['agent1_name'] else results['agent1_name']

    print(f"\n" + "=" * 70)
    print("MEMORY AGENT ANALYSIS")
    print("=" * 70)

    if mean_diff > 0 and "Memory" in results['agent1_name']:
        print(f"\n✓ Memory agent performs BETTER than reflex agent without memory.")
        print(f"\nWhy memory helps:")
        print(f"  1. Opponent bidding provides information about their hand strength")
        print(f"  2. Adjusting bids based on opponent behavior allows:")
        print(f"     - Avoiding overcommitting when opponent is strong")
        print(f"     - Capitalizing when opponent is weak")
        print(f"  3. This creates a more adaptive strategy")
    elif mean_diff < 0 and "Memory" in results['agent1_name']:
        print(f"\n✗ Memory agent performs WORSE than reflex agent without memory.")
        print(f"\nWhy memory might hurt:")
        print(f"  1. The adjustment strategy might be too simplistic")
        print(f"  2. Opponent bidding may not reliably indicate hand strength")
        print(f"     (especially against a reflex agent that also bids based on hand)")
        print(f"  3. The fixed adjustment amounts (+$5/-$5) might not be optimal")
        print(f"  4. Both agents bid based on hand strength, so bids correlate")
        print(f"     with actual hand strength, making opponent bids informative")
        print(f"     but our adjustments might be counterproductive")
    elif mean_diff > 0 and "Memory" in results['agent2_name']:
        print(f"\n✗ Memory agent performs WORSE than reflex agent without memory.")
        print(f"\nWhy memory might hurt:")
        print(f"  1. The adjustment strategy might be too simplistic")
        print(f"  2. Opponent bidding may not reliably indicate hand strength")
        print(f"  3. The fixed adjustment amounts (+$5/-$5) might not be optimal")
    else:
        print(f"\n✓ Memory agent performs BETTER than reflex agent without memory.")
        print(f"\nWhy memory helps:")
        print(f"  1. Opponent bidding provides information about their hand strength")
        print(f"  2. Adjusting bids based on opponent behavior allows:")
        print(f"     - Avoiding overcommitting when opponent is strong")
        print(f"     - Capitalizing when opponent is weak")

    print(f"\n" + "=" * 70)
    print("POTENTIAL IMPROVEMENTS")
    print("=" * 70)
    print(f"\nTo improve the memory agent, consider:")
    print(f"\n1. More sophisticated adjustment strategy:")
    print(f"   - Use proportional adjustments based on opponent bid amount")
    print(f"   - Consider the difference between opponent bid and expected bid")
    print(f"   - Adjust more aggressively when confidence is high")
    print(f"\n2. Multi-phase memory:")
    print(f"   - Track opponent bidding pattern across all phases")
    print(f"   - Detect if opponent is increasing/decreasing bids")
    print(f"   - Use trend analysis to predict opponent strength")
    print(f"\n3. Hand strength comparison:")
    print(f"   - Compare own hand strength with inferred opponent strength")
    print(f"   - Only adjust when there's a significant difference")
    print(f"   - Be more aggressive when own hand is clearly stronger")
    print(f"\n4. Learning from showdown:")
    print(f"   - Use observe_showdown() to learn opponent patterns")
    print(f"   - Build a model of opponent bidding behavior")
    print(f"   - Calibrate adjustments based on historical accuracy")
    print(f"\n5. Pot odds consideration:")
    print(f"   - Consider current pot size when making adjustments")
    print(f"   - Calculate expected value based on hand strength and pot")
    print(f"   - Make adjustments that maximize expected value")
    print(f"\n6. Adaptive thresholds:")
    print(f"   - Instead of fixed thresholds ($20, $30), use dynamic ones")
    print(f"   - Base thresholds on opponent's average bidding pattern")
    print(f"   - Adjust thresholds based on game history")


if __name__ == "__main__":
    print("=" * 70)
    print("Lab 2f: Reflex Agent with Memory vs Reflex Agent without Memory")
    print("=" * 70)

    # Experiment: Reflex Agent with Memory vs Reflex Agent without Memory
    print("\n" + "=" * 70)
    print("EXPERIMENT: Reflex Agent with Memory vs Reflex Agent without Memory")
    print("=" * 70)

    results = run_experiment(
        agent1_factory=lambda: create_reflex_agent_with_memory("Reflex Agent (Memory)"),
        agent2_factory=lambda: create_reflex_agent("Reflex Agent (No Memory)"),
        agent1_name="Reflex Agent (Memory)",
        agent2_name="Reflex Agent (No Memory)",
        num_games=100,
        num_hands=50
    )

    analyze_results(results)
    analyze_memory_effectiveness(results)

    # Generate plots
    plots_dir = os.path.join(os.path.dirname(__file__), '..', 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    generate_all_plots(results, plots_dir, 'lab_2f_reflex_memory_vs_no_memory')

    print("\n" + "=" * 70)
    print("Experiment complete!")
    print("=" * 70)


"""Lab 2c: Build the environment of the game and have agents play."""

import os
import random
import sys

# Add parent directory to path to import libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.agent import Agent  # noqa: E402
from libs.hand_evaluation import analyse_hand  # noqa: E402
from libs.poker_game import PokerGame  # noqa: E402

# Example poker hands for testing
example_hand1 = ["Ad", "2s", "2c"]
example_hand2 = ["5s", "5c", "5d"]


# Agent factory functions
def create_random_agent(name):
    """Create a random agent that bids randomly."""
    class RandomAgent(Agent):
        """A simple agent that bids randomly between $0 and $50."""

        def make_bid(self, phase, own_bids, opponent_bids):
            """Make a bid decision."""
            return random.randint(0, 50)

        def observe_showdown(self, opponent_hand):
            """Observe opponent's hand during showdown phase."""
            pass

    return RandomAgent(name)


def create_fixed_agent(name, fixed_bid_amount=25):
    """Create a fixed agent that always bids the same amount."""
    class FixedAgent(Agent):
        """An agent that always bids a fixed amount."""

        def __init__(self, name, fixed_bid):
            """Initialize fixed agent with a fixed bid amount."""
            super().__init__(name)
            self.fixed_bid = max(0, min(50, fixed_bid))

        def make_bid(self, phase, own_bids, opponent_bids):
            """Make a bid decision."""
            return self.fixed_bid

        def observe_showdown(self, opponent_hand):
            """Observe opponent's hand during showdown phase."""
            pass

    return FixedAgent(name, fixed_bid_amount)


# Test code
if __name__ == "__main__":
    print("=" * 60)
    print("Lab 2c: Poker Game Environment")
    print("=" * 60)

    # Test hand analysis (part 2c.b)
    print("\n2c(b) Testing hand identification and strength evaluation:")
    print(f"Hand 1 {example_hand1}: score = {analyse_hand(example_hand1)}")
    print(f"Hand 2 {example_hand2}: score = {analyse_hand(example_hand2)}")
    print()

    # Create game with agent factories (part 2c.a - game flow)
    print("2c(a) Starting poker game with game flow...")
    print("2c(c) Sensor inputs:")
    print("  - Agent's own hand (during card dealing phase)")
    print("  - Hand of opponent (during showdown phase)")
    print("  - Amount of money both agents bid (during betting phase)")
    print()

    # Play game with random vs fixed agent
    game = PokerGame(
        agent1_factory=lambda: create_random_agent("Random Agent"),
        agent2_factory=lambda: create_fixed_agent("Fixed Agent", 30),
        num_hands=50
    )
    game_result = game.play_game()

    # Print results (part 2c.d - recording results)
    print("\n2c(d) Game Results:")
    print("-" * 60)
    w1 = game_result['agent1_winnings']
    w2 = game_result['agent2_winnings']
    print(f"{game.agent1.name} total winnings: ${w1}")
    print(f"{game.agent2.name} total winnings: ${w2}")
    diff = game_result['difference']
    print(f"Difference ({game.agent1.name} - {game.agent2.name}): ${diff}")
    print()

    # Show first few hands as examples
    print("Sample hands (first 3):")
    print("-" * 60)
    for result in game_result['results'][:3]:
        print(f"\nHand {result['hand_num']}:")
        print(f"  Card Dealing Phase:")
        h1 = result['hand1']
        s1 = result['score1']
        print(f"    {game.agent1.name}: {h1} (score: {s1})")
        h2 = result['hand2']
        s2 = result['score2']
        print(f"    {game.agent2.name}: {h2} (score: {s2})")
        print(f"  Bidding Phases:")
        b1 = result['bids1']
        b2 = result['bids2']
        for i, (bid1, bid2) in enumerate(zip(b1, b2), 1):
            print(f"    Phase {i}: {game.agent1.name} bids ${bid1}, "
                  f"{game.agent2.name} bids ${bid2}")
        print(f"  Showdown Phase:")
        pot = result['pot']
        winner = result['winner']
        print(f"    Pot: ${pot}, Winner: {winner}")

    print("\n" + "=" * 60)
    print("Lab 2c implementation complete!")
    print("=" * 60)


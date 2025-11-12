"""Lab 2a: Implement a random agent that bids randomly."""

import os
import random
import sys

# Add parent directory to path to import libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.agent import Agent  # noqa: E402


def create_random_agent(name):
    """
    Create a random agent that bids randomly.

    Task 2a: Implement a random agent that bids randomly.

    Parameters
    ----------
    name : str
        Name of the agent

    Returns
    -------
    Agent
        A RandomAgent instance
    """
    class RandomAgent(Agent):
        """A simple agent that bids randomly between $0 and $50."""

        def make_bid(self, phase, own_bids, opponent_bids):
            """
            Make a bid decision by randomly choosing between $0 and $50.

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
            return random.randint(0, 50)

        def observe_showdown(self, opponent_hand):
            """Observe opponent's hand during showdown phase."""
            pass  # Random agent doesn't use this information

    return RandomAgent(name)


# Test code
if __name__ == "__main__":
    # Create a random agent
    agent = create_random_agent("Random Agent")

    # Test receiving a hand
    test_hand = ["Ad", "2s", "2c"]
    agent.receive_hand(test_hand)
    print(f"Agent received hand: {agent.hand}")

    # Test making bids
    print("\nTesting random bids:")
    for phase in range(1, 4):
        bid = agent.make_bid(phase, [], [])
        print(f"Phase {phase}: Bid ${bid}")

    print("\nRandom agent implementation complete!")

"""Lab 2b: Implement a fixed agent."""

import os
import sys

# Add parent directory to path to import libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.agent import Agent  # noqa: E402


def create_fixed_agent(name, fixed_bid_amount=25):
    """
    Create a fixed agent that always bids the same amount.

    Task 2b: Implement a fixed agent.

    Parameters
    ----------
    name : str
        Name of the agent
    fixed_bid_amount : int
        Fixed bid amount for all phases (default: 25, range: 0-50)

    Returns
    -------
    Agent
        A FixedAgent instance
    """
    class FixedAgent(Agent):
        """An agent that always bids a fixed amount."""

        def __init__(self, name, fixed_bid):
            """Initialize fixed agent with a fixed bid amount."""
            super().__init__(name)
            self.fixed_bid = max(0, min(50, fixed_bid))  # Clamp to 0-50

        def make_bid(self, phase, own_bids, opponent_bids):
            """
            Make a bid decision by always bidding the fixed amount.

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
            int : bid amount (fixed amount)
            """
            return self.fixed_bid

        def observe_showdown(self, opponent_hand):
            """Observe opponent's hand during showdown phase."""
            pass  # Fixed agent doesn't use this information

    return FixedAgent(name, fixed_bid_amount)


# Test code
if __name__ == "__main__":
    # Create a fixed agent with fixed bid of $25
    agent = create_fixed_agent("Fixed Agent", fixed_bid_amount=25)

    # Test receiving a hand
    test_hand = ["5s", "5c", "5d"]
    agent.receive_hand(test_hand)
    print(f"Agent received hand: {agent.hand}")

    # Test making bids (should always be the same)
    print("\nTesting fixed bids:")
    for phase in range(1, 4):
        bid = agent.make_bid(phase, [], [])
        print(f"Phase {phase}: Bid ${bid}")

    print("\nFixed agent implementation complete!")


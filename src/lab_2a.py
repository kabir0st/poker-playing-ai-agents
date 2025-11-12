import random
from libs.agent import Agent


def create_random_agent(name: str) -> Agent:

    class RandomAgent(Agent):
        """A simple agent that bids randomly between $0 and $50."""

        def make_bid(self, phase, own_bids, opponent_bids):
            return random.randint(0, 50)

    return RandomAgent(name)


if __name__ == "__main__":
    agent = create_random_agent("Random Agent")
    test_hand = ["Ad", "2s", "2c"]
    agent.receive_hand(test_hand)
    print(f"Agent received hand: {agent.hand}")
    print("\nTesting random bids:")
    for phase in range(1, 4):
        bid = agent.make_bid(phase, [], [])
        print(f"Phase {phase}: Bid ${bid}")

    print("\nRandom agent implementation complete!")

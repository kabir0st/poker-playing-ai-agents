from libs.agent import Agent


def create_fixed_agent(name: str, fixed_bid_amount: int = 17) -> Agent:
    class FixedAgent(Agent):
        """An agent that always bids a fixed amount."""

        def __init__(self, name: str, fixed_bid: int) -> None:
            super().__init__(name)
            self.fixed_bid = max(0, min(50, fixed_bid))  # Clamp to 0-50

        def make_bid(self, phase, own_bids, opponent_bids):
            return self.fixed_bid

    return FixedAgent(name, fixed_bid_amount)


if __name__ == "__main__":
    agent = create_fixed_agent("Fixed Agent")
    test_hand = ["5s", "5c", "5d"]
    agent.receive_hand(test_hand)
    print(f"Agent received hand: {agent.hand}")
    print("\nTesting fixed bids:")
    for phase in range(1, 4):
        bid = agent.make_bid(phase, [], [])
        print(f"Phase {phase}: Bid ${bid}")
    print("\nFixed agent implementation complete!")

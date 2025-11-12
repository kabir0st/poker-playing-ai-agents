class Agent:
    """Base class for poker agents."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.hand = None
        self.total_winnings = 0

    def receive_hand(self, hand: list[str]) -> None:
        self.hand = hand

    def make_bid(self, phase: int, own_bids: list[int],
                 opponent_bids: list[int]) -> int:
        raise NotImplementedError(
            "Subclasses must implement make_bid method"
        )

    def observe_showdown(self, opponent_hand: list[str]) -> None:
        pass

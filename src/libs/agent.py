"""Base Agent class for poker players."""


class Agent:
    """Base class for poker agents."""

    def __init__(self, name):
        """Initialize an agent with a name."""
        self.name = name
        self.hand = None
        self.total_winnings = 0

    def receive_hand(self, hand):
        """
        Receive hand during card dealing phase.

        Parameters
        ----------
        hand : list of strings
            The hand of cards assigned to this agent
        """
        self.hand = hand

    def make_bid(self, phase, own_bids, opponent_bids):
        """
        Make a bid decision.

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
        raise NotImplementedError(
            "Subclasses must implement make_bid method"
        )

    def observe_showdown(self, opponent_hand):
        """
        Observe opponent's hand during showdown phase.

        Parameters
        ----------
        opponent_hand : list of strings
            The opponent's hand revealed during showdown
        """
        pass  # Default implementation does nothing


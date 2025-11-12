"""Poker game logic."""

from libs.cards import generate_2hands
from libs.hand_evaluation import analyse_hand


class PokerGame:
    """Simple poker game with two agents."""

    def __init__(self, agent1_factory, agent2_factory, num_hands=50):
        """
        Initialize a poker game.

        Parameters
        ----------
        agent1_factory : callable
            Function that returns an Agent instance for player 1
        agent2_factory : callable
            Function that returns an Agent instance for player 2
        num_hands : int
            Number of hands to play (default: 50)
        """
        self.agent1 = agent1_factory()
        self.agent2 = agent2_factory()
        self.num_hands = num_hands
        self.agent1_winnings = 0
        self.agent2_winnings = 0

    def play_hand(self, hand_num):
        """Play a single hand."""
        # Phase 1: Card Dealing
        hand1, hand2 = generate_2hands(3)
        self.agent1.receive_hand(hand1)
        self.agent2.receive_hand(hand2)

        # Phase 2: Bidding (3 phases)
        agent1_bids = []
        agent2_bids = []
        pot = 0

        for phase in range(1, 4):
            bid1 = self.agent1.make_bid(phase, agent1_bids, agent2_bids)
            bid2 = self.agent2.make_bid(phase, agent2_bids, agent1_bids)

            agent1_bids.append(bid1)
            agent2_bids.append(bid2)
            pot += bid1 + bid2

        # Phase 3: Showdown
        score1 = analyse_hand(hand1)
        score2 = analyse_hand(hand2)

        self.agent1.observe_showdown(hand2)
        self.agent2.observe_showdown(hand1)

        # Determine winner
        if score1 > score2:
            self.agent1_winnings += pot
            winner = self.agent1.name
        elif score2 > score1:
            self.agent2_winnings += pot
            winner = self.agent2.name
        else:
            # Tie - split pot
            self.agent1_winnings += pot // 2
            self.agent2_winnings += pot // 2
            winner = "Tie"

        return {
            'hand_num': hand_num,
            'hand1': hand1,
            'hand2': hand2,
            'score1': score1,
            'score2': score2,
            'bids1': agent1_bids,
            'bids2': agent2_bids,
            'pot': pot,
            'winner': winner
        }

    def play_game(self):
        """Play the full game of 50 hands."""
        results = []

        for hand_num in range(1, self.num_hands + 1):
            result = self.play_hand(hand_num)
            results.append(result)

        # Calculate final difference
        difference = self.agent1_winnings - self.agent2_winnings

        return {
            'results': results,
            'agent1_winnings': self.agent1_winnings,
            'agent2_winnings': self.agent2_winnings,
            'difference': difference
        }


"""Card constants and generation functions."""

import random

# Rank: {2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A}
# Suit: {s, h, d, c}

RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUITS = ['s', 'h', 'd', 'c']
# 2=1, 3=2, ..., A=13
RANK_VALUES = {rank: i+1 for i, rank in enumerate(RANKS)}


def generate_2hands(nn_card=3):
    """
    Return two hands of cards, each hand consists of nn_card number of cards.
    Note that there shall be no duplicates.

    Parameters
    ----------
    nn_card : int
            Number of cards in each hand

    Returns
    -------
    out : lists of strings
        Two lists, each corresponding to one hand
    """
    # Create a deck of all cards
    deck = [rank + suit for rank in RANKS for suit in SUITS]

    # Shuffle and deal
    random.shuffle(deck)
    hand1 = deck[:nn_card]
    hand2 = deck[nn_card:2*nn_card]

    return hand1, hand2


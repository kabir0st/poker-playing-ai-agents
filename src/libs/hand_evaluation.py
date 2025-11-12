"""Hand evaluation functions."""

from libs.cards import RANK_VALUES


def identify_hand(hand_):
    """
    Identify the type and the strength of one hand.

    Notes
    ----------
    We only work with hands with three cards in this exercise, hence, there
    are three types available, i.e. high cards, one pair,
    three of a kind.


    Parameters
    ----------
    Hand_ : list of strings
          Player hands, a list of three strings

    Returns
    -------
    out : tuple (string, int)
        This function should return the type, and the rank value of
        the given hand.
    """
    # Extract ranks
    ranks = [card[0] for card in hand_]
    rank_counts = {}
    for rank in ranks:
        rank_counts[rank] = rank_counts.get(rank, 0) + 1

    # Check for three of a kind
    if 3 in rank_counts.values():
        rank = [r for r, count in rank_counts.items() if count == 3][0]
        return ("three_of_a_kind", RANK_VALUES[rank])

    # Check for pair
    if 2 in rank_counts.values():
        rank = [r for r, count in rank_counts.items() if count == 2][0]
        return ("pair", RANK_VALUES[rank])

    # High card - return the highest rank
    max_rank = max(ranks, key=lambda r: RANK_VALUES[r])
    return ("high_card", RANK_VALUES[max_rank])


def analyse_hand(hand_):
    """
    Evaluates a given hand based on its type and strength,
    and return an integer value.

    Notes
    ----------
    This function should call identify_hand(...)
    and evaluate it based on its type and the strength.
    high cards: 1 - 13
    pairs: 14 - 26
    three-of-a-kind: 27 - 39


    Parameters
    ----------
    Hand_ : list of strings
          Player hands, a list of three strings

    Returns
    -------
    out : int
        A value refecting the overall strength of a hand.
    """
    hand_type, rank_value = identify_hand(hand_)

    if hand_type == "three_of_a_kind":
        score = 27 + rank_value - 1  # 27-39
    elif hand_type == "pair":
        score = 14 + rank_value - 1  # 14-26
    else:  # high_card
        score = rank_value  # 1-13

    return score

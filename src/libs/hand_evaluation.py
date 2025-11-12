"""Hand evaluation functions."""

from libs.cards import RANK_VALUES


def identify_hand(hand_: list[str]) -> tuple[str, int]:
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


def analyse_hand(hand_: list[str]) -> int:
    """Analyse a hand and return a score."""
    hand_type, rank_value = identify_hand(hand_)
    if hand_type == "three_of_a_kind":
        score = 26 + rank_value  # 27-39
    elif hand_type == "pair":
        score = 13 + rank_value  # 14-26
    else:  # high_card
        score = rank_value  # 1-13
    return score

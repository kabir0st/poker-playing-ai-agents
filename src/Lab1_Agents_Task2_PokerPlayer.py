# Please feel free to work with your own code structure

# Rank: {2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A}
# Suit: {s, h, d, c}

# 2 example poker hands
example_hand1 = ["Ad", "2s", "2c"]
example_hand2 = ["5s", "5c", "5d"]


# Randomly generate two hands of n cards
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
    pass


# identify hand category using IF-THEN rule
def identify_hand(hand_):
    """
    Identify the type and the strength of one hand.

    Notes
    ----------
    We only work with hands with three cards in this exercise, hence, there are three types available, i.e. high cards, one pair,       three of a kind.


    Parameters
    ----------
    Hand_ : list of strings
          Player hands, a list of three strings

    Returns
    -------
    out : string, int
        This function should return the type, and the strength of the given hand.
    """
    for c1 in hand_:
        for c2 in hand_:
            if (c1[0] == c2[0]) and (c1[1] < c2[1]):
                yield dict(name="pair", rank=c1[0], suit1=c1[1], suit2=c2[1])


# Print out the result
def analyse_hand(hand_):
    """
    Evaluates a given hand based on its type and strength, and return an integer value.

    Notes
    ----------
    This function should call identify_hand(...) and evaluate it based on its type and the strength.
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

    return score


# writing your test code here
print(analyse_hand(example_hand1))

#########################
#      Game flow        #
#########################


#########################
# phase 1: Card Dealing #
#########################


#########################
# phase 2:   Bidding    #
#########################

# Sensing, resoning & decision making, and acting


#########################
# phase 2:   Showdown   #
#########################


w

from libs.poker_game import PokerGame
from lab_2a import create_random_agent


if __name__ == "__main__":
    print("-" * 60)
    print("Lab 2c: Testing Poker Game Environment with Random Agents")
    print("-" * 60)
    # Play game with random vs fixed agent
    game = PokerGame(
        agent1_factory=lambda: create_random_agent("James Bond"),
        agent2_factory=lambda: create_random_agent("Le Chiffre"),
        num_hands=50
    )
    game_result = game.play_game()

    print("\n Game Results:")
    print("-" * 60)
    w1 = game_result['agent1_winnings']
    w2 = game_result['agent2_winnings']
    print(f"{game.agent1.name} total winnings: ${w1}")
    print(f"{game.agent2.name} total winnings: ${w2}")
    diff = game_result['difference']
    print(f"Difference ({game.agent1.name} - {game.agent2.name}): ${diff}")
    print()

    print("Sample hands (first 3):")
    print("-" * 60)
    for result in game_result['results'][:3]:
        print(f"\nHand {result['hand_num']}:")
        print("  Card Dealing Phase:")
        h1 = result['hand1']
        s1 = result['score1']
        print(f"    {game.agent1.name}: {h1} (score: {s1})")
        h2 = result['hand2']
        s2 = result['score2']
        print(f"    {game.agent2.name}: {h2} (score: {s2})")
        print("  Bidding Phases:")
        b1 = result['bids1']
        b2 = result['bids2']
        for i, (bid1, bid2) in enumerate(zip(b1, b2), 1):
            print(f"    Phase {i}: {game.agent1.name} bids ${bid1}, "
                  f"{game.agent2.name} bids ${bid2}")
        print("  Showdown Phase:")
        pot = result['pot']
        winner = result['winner']
        print(f"    Pot: ${pot}, Winner: {winner}")

    print("\n" + "-" * 60)
    print("Lab 2c implementation complete!")
    print("-" * 60)

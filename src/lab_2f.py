import os
import statistics

from lab_2e import create_reflex_agent
from libs.agent import Agent
from libs.hand_evaluation import analyse_hand
from libs.poker_game import PokerGame
from plotting_utils import generate_all_plots
from tqdm import tqdm


def create_reflex_agent_with_memory(name):

    class ReflexAgentWithMemory(Agent):

        def make_bid(self, phase, own_bids, opponent_bids):
            if self.hand is None:
                # If no hand received yet, bid minimum
                return 0

            # Evaluate hand strength (score ranges from 1-39)
            hand_score = analyse_hand(self.hand)
            base_bid = (hand_score / 39.0) * 50

            # Adjust based on opponent's last bid (if available)
            # Note: When bidding second in a phase,
            # opponent_bids includes the opponent's
            # bid from the current phase, allowing real-time
            # reaction to opponent behavior
            adjustment = 0
            if opponent_bids:  # If opponent has bid
                last_opponent_bid = opponent_bids[-1]

                # Calculate expected opponent bid
                # Average hand strength is ~20 (midpoint of 1-39),
                # so expected bid ~25.6
                # We can also use our own base_bid as a reference point
                expected_opponent_bid = 25.0  # Average expected bid
                # Calculate the difference between opponent bid and
                # expected bid
                bid_difference = last_opponent_bid - expected_opponent_bid

                # Calculate confidence based on hand strength
                # Normalize hand strength to [0, 1] range (1-39 -> 0-1)
                # Stronger hands = higher confidence
                confidence = (hand_score) / 39.0

                # Proportional adjustment based on bid difference
                # The adjustment is proportional to how much the opponent
                # deviates from expected
                # Maximum adjustment factor: if opponent bids 0 or 50,
                # difference is ±25
                # We scale this to a reasonable adjustment range
                base_adjustment_factor = bid_difference / 25.0

                # Apply confidence multiplier: higher confidence =
                #  more aggressive adjustment
                # Confidence ranges from 0 (weak hand) to 1 (strong hand)
                # When confidence is high, we trust our hand more
                # and adjust more aggressively
                # When confidence is low, we're more cautious
                confidence_multiplier = 0.5 + confidence

                # Calculate proportional adjustment
                # Negative bid_difference (opponent bid low) ->
                # positive adjustment (we bid more)
                # Positive bid_difference (opponent bid high) ->
                # negative adjustment (we bid less)
                # The adjustment is proportional to the difference
                # and scaled by confidence
                max_adjustment = 15.0  # Maximum adjustment amount
                adjustment = -base_adjustment_factor * max_adjustment * \
                    confidence_multiplier

            # Apply adjustment
            bid = base_bid + adjustment

            # Ensure bid is within valid range [0, 50]
            bid = max(0, min(50, int(bid)))

            return bid

        def observe_showdown(self, opponent_hand):
            pass

    return ReflexAgentWithMemory(name)


def run_experiment(agent1_factory,
                   agent2_factory,
                   agent1_name,
                   agent2_name,
                   num_games=100,
                   num_hands=50):
    differences = []
    agent1_winnings = []
    agent2_winnings = []
    for game_num in tqdm(range(1, num_games + 1),
                         desc="Playing games",
                         unit="game"):
        # Create a new game with fresh agents
        game = PokerGame(agent1_factory=agent1_factory,
                         agent2_factory=agent2_factory,
                         num_hands=num_hands)

        # Play the game
        game_result = game.play_game()

        # Calculate difference (Agent1 - Agent2)
        diff = game_result['difference']
        differences.append(diff)
        agent1_winnings.append(game_result['agent1_winnings'])
        agent2_winnings.append(game_result['agent2_winnings'])

    # Calculate statistics
    mean_diff = statistics.mean(differences)
    std_diff = statistics.stdev(differences) if len(differences) > 1 else 0

    return {
        'differences': differences,
        'agent1_winnings': agent1_winnings,
        'agent2_winnings': agent2_winnings,
        'mean_difference': mean_diff,
        'std_difference': std_diff,
        'num_games': num_games,
        'num_hands': num_hands,
        'agent1_name': agent1_name,
        'agent2_name': agent2_name
    }


if __name__ == "__main__":
    print("Lab 2f: Reflex Agent with Memory vs Reflex Agent without Memory")

    results = run_experiment(
        agent1_factory=lambda: create_reflex_agent_with_memory("Memory"),
        agent2_factory=lambda: create_reflex_agent("No Memory"),
        agent1_name="Reflex Agent (Memory)",
        agent2_name="Reflex Agent (No Memory)",
        num_games=100000,
        num_hands=50)
    print(f"Mean difference: {results['mean_difference']}")
    print(f"Standard deviation of difference: {results['std_difference']}")

    # Generate plots
    plots_dir = os.path.join(os.path.dirname(__file__), '..', 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    generate_all_plots(results, plots_dir, 'lab_2f_reflex_memory_vs_no_memory')

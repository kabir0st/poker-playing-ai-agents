import os
import statistics

from lab_2e import create_reflex_agent
from libs.agent import Agent
from libs.hand_evaluation import analyse_hand
from libs.poker_game import PokerGame
from plotting_utils import generate_all_plots
from tqdm import tqdm

# A game "win" = having more total winnings after 50 hands


def create_reflex_agent_with_memory(name):

    class ReflexAgentWithMemory(Agent):

        def __init__(self, name):
            super().__init__(name)
            self.opponent_ratios = []
            self.current_hand_opponent_bids = []

        def make_bid(self, phase, own_bids, opponent_bids):
            if self.hand is None:
                # If no hand received yet, bid minimum
                return 0

            if opponent_bids:
                self.current_hand_opponent_bids = opponent_bids.copy()
            hand_score = analyse_hand(self.hand)
            base_bid = (hand_score / 39.0) * 50

            # Adjust based on opponent's bidding behavior and predicted hand
            adjustment = 0
            if opponent_bids:  # If opponent has bid
                # Predict opponent's hand strength from their current bids
                # using learned bid-to-hand-strength mapping
                predicted_opponent_hand = self._predict_opponent_hand_strength(
                    opponent_bids)

                # Compare our hand strength to predicted opponent hand strength
                hand_strength_diff = hand_score - predicted_opponent_hand

                # Calculate confidence based on hand strength
                confidence = hand_score / 39.0
                confidence_multiplier = 0.5 + confidence

                # Adjust bid based on hand strength comparison
                # If we have stronger hand (positive diff), bid more
                # If opponent has stronger hand (negative diff), bid less
                # Scale adjustment by hand strength difference and confidence
                # Normalize difference to [-1, 1] range (max diff is ±38)
                normalized_diff = hand_strength_diff / 39.0
                max_adjustment = 20.0  # Maximum adjustment amount
                adjustment = normalized_diff * max_adjustment * \
                    confidence_multiplier

            # Apply adjustment
            bid = base_bid + adjustment

            # Ensure bid is within valid range [0, 50]
            bid = max(0, min(50, int(bid)))

            return bid

        def _predict_opponent_hand_strength(self, opponent_bids):
            if not self.opponent_ratios or not opponent_bids:
                return 25.0
            current_avg_bid = sum(opponent_bids) / len(opponent_bids)
            avg_ratio = sum(self.opponent_ratios) / len(self.opponent_ratios)
            predicted_hand = current_avg_bid * avg_ratio
            predicted_hand = max(1.0, min(39.0, predicted_hand))
            return predicted_hand

        def observe_showdown(self, opponent_hand):
            opponent_hand_strength = analyse_hand(opponent_hand)
            if self.current_hand_opponent_bids:
                opponent_avg_bid = sum(self.current_hand_opponent_bids) / len(
                    self.current_hand_opponent_bids)
            else:
                opponent_avg_bid = 0

            if opponent_avg_bid > 0:
                ratio = opponent_hand_strength / opponent_avg_bid
                self.opponent_ratios.append(ratio)

            self.current_hand_opponent_bids = []

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
    for _ in tqdm(range(1, num_games + 1), desc="Playing games", unit="game"):
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
        num_games=100,
        num_hands=50)
    print(f"Mean difference: {results['mean_difference']}")
    print(f"Standard deviation of difference: {results['std_difference']}")

    # Generate plots
    plots_dir = os.path.join(os.path.dirname(__file__), '..', 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    generate_all_plots(results, plots_dir, 'lab_2f_reflex_memory_vs_no_memory')

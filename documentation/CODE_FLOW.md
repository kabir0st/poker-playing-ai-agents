# Code Flow and Architecture

Detailed explanation of the codebase structure, data flow, and component interactions.

## Project Structure

```
poker-ai/
├── src/
│   ├── libs/                    # Core game library
│   │   ├── __init__.py
│   │   ├── agent.py            # Base Agent class
│   │   ├── cards.py            # Card generation and constants
│   │   ├── hand_evaluation.py  # Hand scoring logic
│   │   └── poker_game.py       # Game engine
│   ├── lab_2a.py              # Random agent implementation
│   ├── lab_2b.py              # Fixed agent implementation
│   ├── lab_2c.py              # Game environment setup
│   ├── lab_2d.py              # Random vs Fixed comparison
│   ├── lab_2e.py              # Reflex agent experiments
│   ├── lab_2f.py              # Memory agent experiment
│   └── plotting_utils.py      # Visualization utilities
├── plots/                      # Generated plots (PNG files)
├── documentation/              # Documentation files
└── README.md                   # Main project README
```

## Core Components

### 1. Agent Base Class (`libs/agent.py`)

**Purpose**: Abstract base class defining the agent interface

**Class Structure**:
```python
class Agent:
    def __init__(self, name)
    def receive_hand(self, hand)
    def make_bid(self, phase, own_bids, opponent_bids)
    def observe_showdown(self, opponent_hand)
```

**Data Flow**:
```
Game Engine → receive_hand() → Agent stores hand
Game Engine → make_bid() → Agent returns bid amount
Game Engine → observe_showdown() → Agent can learn
```

**Key Methods**:
- `receive_hand(hand)`: Stores the agent's hand for the current hand
- `make_bid(...)`: Must be implemented by subclasses, returns bid amount
- `observe_showdown(...)`: Optional, can be used for learning

### 2. Card System (`libs/cards.py`)

**Purpose**: Card generation and deck management

**Key Components**:
- `RANKS`: List of rank symbols ['2', '3', ..., 'A']
- `SUITS`: List of suit symbols ['s', 'h', 'd', 'c']
- `RANK_VALUES`: Dictionary mapping ranks to numeric values
- `generate_2hands(nn_card)`: Creates two non-overlapping hands

**Data Flow**:
```
generate_2hands(3)
  → Create deck of 52 cards
  → Shuffle deck
  → Deal first 3 cards to hand1
  → Deal next 3 cards to hand2
  → Return (hand1, hand2)
```

**Example**:
```python
hand1, hand2 = generate_2hands(3)
# hand1 = ["As", "Kh", "2c"]
# hand2 = ["5s", "5h", "5c"]
```

### 3. Hand Evaluation (`libs/hand_evaluation.py`)

**Purpose**: Evaluate hand strength and assign scores

**Functions**:
- `identify_hand(hand)`: Returns (hand_type, rank_value)
- `analyse_hand(hand)`: Returns integer score (1-39)

**Evaluation Flow**:
```
analyse_hand(hand)
  → identify_hand(hand)
    → Extract ranks from cards
    → Count rank occurrences
    → Determine hand type (three_of_a_kind, pair, high_card)
    → Return (type, rank_value)
  → Calculate score based on type
    → Three of a kind: 27 + rank_value - 1
    → Pair: 14 + rank_value - 1
    → High card: rank_value
  → Return score (1-39)
```

**Example**:
```python
hand = ["Ks", "Kh", "2c"]
score = analyse_hand(hand)  # Returns 25
# Pair of Kings: 14 + (12-1) = 25
```

### 4. Game Engine (`libs/poker_game.py`)

**Purpose**: Orchestrates game flow and manages state

**Class Structure**:
```python
class PokerGame:
    def __init__(agent1_factory, agent2_factory, num_hands)
    def play_hand(hand_num)
    def play_game()
```

**Game Flow**:
```
PokerGame.__init__()
  → Create agent1 from factory
  → Create agent2 from factory
  → Initialize winnings to 0

play_game()
  → Initialize agent1_bids_first (random 50/50 chance)
  → For each hand (1 to num_hands):
      → play_hand(hand_num)
      → Toggle agent1_bids_first (alternates each hand)
  → Calculate final difference
  → Return results dictionary

play_hand(hand_num)
  → Phase 1: Deal cards
    → generate_2hands(3)
    → agent1.receive_hand(hand1)
    → agent2.receive_hand(hand2)

  → Phase 2: Bidding (3 rounds)
    → For phase in [1, 2, 3]:
        → If agent1_bids_first:
            → bid1 = agent1.make_bid(phase, agent1_bids, agent2_bids)
            → agent1_bids.append(bid1)
            → bid2 = agent2.make_bid(phase, agent2_bids, agent1_bids)
            → agent2_bids.append(bid2)
        → Else (agent2_bids_first):
            → bid2 = agent2.make_bid(phase, agent2_bids, agent1_bids)
            → agent2_bids.append(bid2)
            → bid1 = agent1.make_bid(phase, agent1_bids, agent2_bids)
            → agent1_bids.append(bid1)
        → Add bids to pot
        → Toggle agent1_bids_first for next hand

  → Phase 3: Showdown
    → score1 = analyse_hand(hand1)
    → score2 = analyse_hand(hand2)
    → agent1.observe_showdown(hand2)
    → agent2.observe_showdown(hand1)
    → Determine winner
    → Add pot to winner's winnings

  → Return hand result dictionary
```

**State Management**:
- `agent1_winnings`: Cumulative winnings for agent 1
- `agent2_winnings`: Cumulative winnings for agent 2
- `num_hands`: Number of hands to play

## Agent Implementations

### Random Agent (`lab_2a.py`)

**Flow**:
```
make_bid(phase, own_bids, opponent_bids)
  → Generate random number (0-50)
  → Return random bid
```

**No state needed**: Pure function, no memory

### Fixed Agent (`lab_2b.py`)

**Flow**:
```
__init__(name, fixed_bid)
  → Store fixed_bid amount

make_bid(phase, own_bids, opponent_bids)
  → Return fixed_bid
```

**State**: Stores `fixed_bid` value

### Reflex Agent (`lab_2e.py`)

**Flow**:
```
make_bid(phase, own_bids, opponent_bids)
  → Get hand from self.hand
  → hand_score = analyse_hand(self.hand)
  → bid = (hand_score / 39.0) * 50
  → Clamp to [0, 50]
  → Return bid
```

**State**: Stores `hand` (set by `receive_hand()`)

### Reflex Agent with Memory (`lab_2f.py`)

**Flow**:
```
make_bid(phase, own_bids, opponent_bids)
  → Get hand from self.hand
  → Store opponent_bids in self.current_hand_opponent_bids
  → hand_score = analyse_hand(self.hand)
  → base_bid = (hand_score / 39.0) * 50

  → If opponent_bids exists:
      → predicted_opponent_hand = _predict_opponent_hand_strength(opponent_bids)
        → If no learned ratios: return 25.0 (default)
        → Else: current_avg_bid = average(opponent_bids)
        → avg_ratio = average(self.opponent_ratios)
        → predicted_hand = current_avg_bid × avg_ratio

      → hand_strength_diff = hand_score - predicted_opponent_hand
      → confidence = hand_score / 39.0
      → confidence_multiplier = 0.5 + confidence
      → normalized_diff = hand_strength_diff / 39.0
      → adjustment = normalized_diff × 20.0 × confidence_multiplier
  → Else:
      → adjustment = 0

  → bid = base_bid + adjustment
  → Clamp to [0, 50]
  → Return bid

observe_showdown(opponent_hand)
  → opponent_hand_strength = analyse_hand(opponent_hand)
  → opponent_avg_bid = average(self.current_hand_opponent_bids)
  → If opponent_avg_bid > 0:
      → ratio = opponent_hand_strength / opponent_avg_bid
      → self.opponent_ratios.append(ratio)
  → Reset self.current_hand_opponent_bids = []
```

**State**:
- Stores `hand` (set by `receive_hand()`)
- Stores `opponent_ratios` (learned from showdowns)
- Stores `current_hand_opponent_bids` (temporary, for current hand)

## Experiment Flow

### Lab 2d: Random vs Fixed

**Flow**:
```
run_experiment()
  → For game in range(1, 101):
      → Create PokerGame with Random and Fixed agents
      → Play 50 hands
      → Record winnings and difference
  → Calculate statistics (mean, std dev)
  → Return results dictionary

analyze_results(results)
  → Print statistics
  → Determine better agent
  → Explain results
```

### Lab 2e: Reflex Agent Experiments

**Flow**:
```
Experiment 1: Reflex vs Random
  → run_experiment(Reflex, Random)
  → analyze_results()
  → generate_all_plots()

Experiment 2: Reflex vs Fixed
  → run_experiment(Reflex, Fixed)
  → analyze_results()
  → generate_all_plots()
```

### Lab 2f: Memory Agent

**Flow**:
```
run_experiment(Reflex+Memory, Reflex)
  → Play games
  → Calculate statistics
  → analyze_results()
  → analyze_memory_effectiveness()
  → generate_all_plots()
```

## Data Structures

### Hand Result Dictionary
```python
{
    'hand_num': int,
    'hand1': list[str],      # Agent 1's cards
    'hand2': list[str],      # Agent 2's cards
    'score1': int,          # Agent 1's hand score
    'score2': int,          # Agent 2's hand score
    'bids1': list[int],     # Agent 1's bids [phase1, phase2, phase3]
    'bids2': list[int],     # Agent 2's bids [phase1, phase2, phase3]
    'pot': int,             # Total pot size
    'winner': str           # Winner name or "Tie"
}
```

### Game Result Dictionary
```python
{
    'results': list[dict],           # List of hand results
    'agent1_winnings': int,          # Total winnings for agent 1
    'agent2_winnings': int,          # Total winnings for agent 2
    'difference': int               # agent1_winnings - agent2_winnings
}
```

### Experiment Results Dictionary
```python
{
    'differences': list[int],         # Differences for each game
    'agent1_winnings': list[int],     # Winnings for each game
    'agent2_winnings': list[int],     # Winnings for each game
    'mean_difference': float,        # Mean of differences
    'std_difference': float,         # Std dev of differences
    'mean_agent1_winnings': float,    # Mean winnings for agent 1
    'mean_agent2_winnings': float,    # Mean winnings for agent 2
    'num_games': int,                # Number of games
    'num_hands': int,                # Hands per game
    'agent1_name': str,              # Agent 1 name
    'agent2_name': str               # Agent 2 name
}
```

## Visualization Flow

### Plotting Utilities (`plotting_utils.py`)

**Flow**:
```
generate_all_plots(results, output_dir, prefix)
  → plot_win_rate_analysis()
  → plot_winnings_after_x_games()
```

**Each Plot Function**:
```
plot_function(results, output_dir, filename_prefix)
  → Extract data from results dictionary
  → Create matplotlib figure
  → Generate plot
  → Save to PNG file (300 DPI)
  → Close figure
```

## Execution Flow

### Complete Experiment Execution

```
1. Import modules
   → Import agent factories
   → Import game engine
   → Import plotting utilities

2. Create agents
   → agent1 = agent1_factory()
   → agent2 = agent2_factory()

3. Run games
   → For each game:
       → Create PokerGame instance
       → Play 50 hands
       → Record results

4. Calculate statistics
   → Mean difference
   → Standard deviation
   → Win rates

5. Generate visualizations
   → Create plots directory
   → Generate 6 plot types
   → Save PNG files

6. Analyze and report
   → Print statistics
   → Determine better agent
   → Explain results
```

## Key Design Patterns

### Factory Pattern
- Agent factories (`create_random_agent`, `create_reflex_agent`, etc.)
- Allows easy agent creation and swapping
- Enables fresh agent instances for each game

### Strategy Pattern
- Each agent implements `make_bid()` differently
- Same interface, different strategies
- Easy to add new agent types

### Template Method Pattern
- `PokerGame.play_hand()` defines game flow template
- Agents implement specific decision-making methods
- Consistent game flow across all agents

## Extension Points

### Adding a New Agent

1. Create agent class inheriting from `Agent`
2. Implement `make_bid()` method
3. Optionally implement `observe_showdown()` for learning
4. Create factory function
5. Add to experiment script

### Adding New Statistics

1. Calculate new metric in `run_experiment()`
2. Add to results dictionary
3. Update `analyze_results()` to display
4. Optionally create new plot function

### Adding New Plot Types

1. Create new function in `plotting_utils.py`
2. Follow existing plot function pattern
3. Add to `generate_all_plots()`
4. Update documentation

## Performance Considerations

### Computational Complexity
- **Per hand**: O(1) - constant time operations
- **Per game**: O(num_hands) - linear in number of hands
- **Per experiment**: O(num_games × num_hands) - linear overall

### Memory Usage
- **Per game**: Stores results for all hands
- **Per experiment**: Stores results for all games
- **Plots**: Generated and saved, not kept in memory

### Optimization Opportunities
- Batch processing for large experiments
- Parallel game execution
- Incremental statistics calculation
- Plot generation only when needed

## Summary

The codebase follows a clean, modular architecture:
- **Separation of concerns**: Game logic, agents, and visualization are separate
- **Extensibility**: Easy to add new agents or metrics
- **Reproducibility**: Deterministic scoring with random card dealing
- **Maintainability**: Clear structure and documentation

The flow is straightforward: agents make decisions, the game engine orchestrates play, and results are analyzed and visualized.


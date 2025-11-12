# Poker AI Lab - Documentation

## Table of Contents
1. [Game Overview](#game-overview)
2. [Architecture](#architecture)
3. [Agent Implementations](#agent-implementations)
4. [Statistics and Metrics](#statistics-and-metrics)
5. [Running Experiments](#running-experiments)

## Additional Documentation

For more detailed information, see:
- **[Game Structure](GAME_STRUCTURE.md)** - Complete game rules, hand types, scoring, and game flow
- **[Code Flow](CODE_FLOW.md)** - Detailed architecture, data structures, and execution flow
- **[Flow Diagrams](FLOW_DIAGRAMS.md)** - Visual flowcharts for each lab experiment
- **[Quick Reference](QUICK_REFERENCE.md)** - Quick lookup guide for agents and statistics

---

## Game Overview

### Game Rules

This is a simplified poker game designed for AI agent experimentation. The game follows these rules:

- **Players**: Two agents compete against each other
- **Deck**: Standard 52-card deck (4 suits × 13 ranks)
- **Hand Size**: Each agent receives exactly 3 cards
- **Game Length**: 50 hands per game
- **Money System**: Agents have unlimited money from a "central bank"
- **Objective**: Maximize the difference between your winnings and opponent's winnings

### Hand Types and Scoring

With only 3 cards, there are three possible hand types:

1. **High Card** (Score: 1-13)
   - No pairs or three-of-a-kind
   - Score = rank value of highest card (2=1, 3=2, ..., A=13)

2. **Pair** (Score: 14-26)
   - Two cards of the same rank
   - Score = 14 + (rank value - 1)
   - Example: Pair of 5s = 14 + (5-1) = 18

3. **Three of a Kind** (Score: 27-39)
   - All three cards have the same rank
   - Score = 27 + (rank value - 1)
   - Example: Three 7s = 27 + (7-1) = 33

**Note**: Suits are equal in value (no suit hierarchy)

### Game Flow

Each hand consists of three phases:

#### Phase 1: Card Dealing
- Random hands of 3 cards are dealt to each agent
- Agents receive their hands via `receive_hand()`

#### Phase 2: Bidding (3 Rounds)
- Each agent makes a bid between $0-$50 in each of 3 bidding phases
- Agents can see:
  - Their own hand
  - Their own previous bids
  - Opponent's previous bids
- All bids are added to the pot

#### Phase 3: Showdown
- Both agents reveal their hands
- Hand scores are compared
- Winner takes the entire pot
- In case of a tie, pot is split equally
- Agents observe opponent's hand via `observe_showdown()`

### Example Hand

```
Card Dealing:
  Agent 1: ['4h', 'Ks', 'Kc']  (Pair of Kings, score = 26)
  Agent 2: ['5s', '5h', '5c']  (Three 5s, score = 31)

Bidding Phase 1:
  Agent 1 bids $20
  Agent 2 bids $30

Bidding Phase 2:
  Agent 1 bids $30
  Agent 2 bids $25

Bidding Phase 3:
  Agent 1 bids $5
  Agent 2 bids $45

Showdown:
  Pot = $20 + $30 + $30 + $25 + $5 + $45 = $155
  Agent 2 wins (score 31 > 26)
  Agent 2 receives $155
```

---

## Architecture

### Code Structure

```
poker-ai/
├── src/
│   ├── libs/
│   │   ├── agent.py          # Base Agent class
│   │   ├── cards.py          # Card generation and constants
│   │   ├── hand_evaluation.py # Hand scoring logic
│   │   └── poker_game.py     # Game engine
│   ├── lab_2a.py             # Random agent implementation
│   ├── lab_2b.py             # Fixed agent implementation
│   ├── lab_2c.py             # Game environment setup
│   ├── lab_2d.py             # Random vs Fixed comparison
│   ├── lab_2e.py             # Reflex agent implementation
│   ├── lab_2f.py             # Reflex agent with memory
│   └── plotting_utils.py     # Visualization utilities
├── plots/                    # Generated visualization plots
└── documentation/            # This documentation
```

### Core Components

#### 1. Agent Base Class (`libs/agent.py`)
Abstract base class defining the interface for all agents:
- `receive_hand(hand)`: Called during card dealing phase
- `make_bid(phase, own_bids, opponent_bids)`: Called during each bidding phase
- `observe_showdown(opponent_hand)`: Called after showdown

#### 2. Game Engine (`libs/poker_game.py`)
The `PokerGame` class orchestrates gameplay:
- Manages game state (winnings, hands, bids)
- Executes the three-phase hand flow
- Determines winners and distributes pots
- Tracks statistics

#### 3. Hand Evaluation (`libs/hand_evaluation.py`)
Functions for evaluating hand strength:
- `identify_hand(hand)`: Returns hand type and rank value
- `analyse_hand(hand)`: Returns numerical score (1-39)

#### 4. Card System (`libs/cards.py`)
- Card generation and deck management
- Rank and suit constants
- `generate_2hands(n)`: Creates two non-overlapping hands

---

## Agent Implementations

### 1. Random Agent (`lab_2a.py`)

**Strategy**: Pure randomness
- Bids a random amount between $0-$50 in each phase
- Does not consider hand strength or opponent behavior
- Average bid per phase: ~$25 (uniform distribution)

**Use Case**: Baseline for comparison

**Code**:
```python
def make_bid(self, phase, own_bids, opponent_bids):
    return random.randint(0, 50)
```

---

### 2. Fixed Agent (`lab_2b.py`)

**Strategy**: Consistent bidding
- Always bids the same fixed amount (default: $25) in every phase
- Predictable and stable strategy
- Total bid per hand: $75 (3 phases × $25)

**Use Case**: Simple baseline that demonstrates consistency

**Code**:
```python
def make_bid(self, phase, own_bids, opponent_bids):
    return self.fixed_bid  # e.g., 25
```

---

### 3. Reflex Agent (`lab_2e.py`)

**Strategy**: Hand strength-based bidding
- Evaluates own hand strength using `analyse_hand()`
- Bids proportionally to hand strength
- Formula: `bid = (hand_score / 39) * 50`

**Bidding Ranges**:
- Weak hands (score 1-13): Bid $1-$16
- Medium hands (score 14-26): Bid $18-$33
- Strong hands (score 27-39): Bid $35-$50

**Advantages**:
- Uses available information (hand strength)
- Adapts to hand quality
- More strategic than random/fixed agents

**Code**:
```python
def make_bid(self, phase, own_bids, opponent_bids):
    hand_score = analyse_hand(self.hand)
    bid = int((hand_score / 39.0) * 50)
    return max(0, min(50, bid))
```

---

### 4. Reflex Agent with Memory (`lab_2f.py`)

**Strategy**: Hand strength + opponent behavior analysis
- Base bid from hand strength (same as reflex agent)
- Adjusts bid based on opponent's last bid:
  - Opponent bid > $30: Reduce bid by $5 (cautious - opponent might be strong)
  - Opponent bid < $20: Increase bid by $5 (aggressive - opponent might be weak)
  - Opponent bid $20-$30: No adjustment (neutral)

**Advantages**:
- Uses both own hand strength AND opponent signals
- More adaptive than simple reflex agent
- Can avoid overcommitting against strong opponents
- Can capitalize on weak opponents

**Limitations**:
- Simple adjustment strategy (+$5/-$5)
- Only considers last bid, not bidding pattern
- Fixed thresholds may not be optimal

**Code**:
```python
def make_bid(self, phase, own_bids, opponent_bids):
    base_bid = (hand_score / 39.0) * 50

    if opponent_bids:
        last_opponent_bid = opponent_bids[-1]
        if last_opponent_bid > 30:
            adjustment = -5  # Cautious
        elif last_opponent_bid < 20:
            adjustment = +5  # Aggressive
        else:
            adjustment = 0

    return max(0, min(50, int(base_bid + adjustment)))
```

---

## Statistics and Metrics

### Key Metrics

#### 1. Bankroll Difference
**Definition**: `Agent1_winnings - Agent2_winnings`

**Interpretation**:
- Positive value: Agent 1 performed better
- Negative value: Agent 2 performed better
- Zero: Equal performance

**Use**: Primary metric for comparing agent performance

---

#### 2. Mean Difference
**Definition**: Average bankroll difference across all games

**Formula**: `mean_diff = sum(differences) / num_games`

**Interpretation**:
- Shows average advantage of one agent over another
- Larger absolute value = stronger advantage
- Sign indicates which agent is better

**Example**: Mean difference of +$428 means Agent 1 wins $428 more per game on average

---

#### 3. Standard Deviation
**Definition**: Measure of variability in bankroll differences

**Interpretation**:
- Low std dev: Consistent performance
- High std dev: High variability (some games very different outcomes)
- If `|mean| > 2 × std_dev`: Statistically significant advantage

**Use**: Assesses reliability of the mean difference

---

#### 4. Average Winnings per Game
**Definition**: Mean winnings for each agent across all games

**Interpretation**:
- Shows absolute performance level
- Higher is better
- Difference between agents' averages equals mean difference

---

#### 5. Win Rate
**Definition**: Percentage of games won by each agent

**Calculation**:
- Agent 1 wins: `count(differences > 0) / total_games × 100%`
- Agent 2 wins: `count(differences < 0) / total_games × 100%`
- Ties: `count(differences == 0) / total_games × 100%`

**Interpretation**:
- Higher win rate = more consistent winner
- Can differ from mean difference if wins/losses vary in magnitude

---

### Visualization Plots

The experiments generate six types of plots:

#### 1. Bankroll Differences Histogram
- Shows distribution of differences across games
- Includes mean and standard deviation lines
- Helps identify if differences are normally distributed

#### 2. Winnings Comparison Box Plot
- Compares distributions of winnings per game
- Shows median, quartiles, and outliers
- Visual comparison of performance variability

#### 3. Cumulative Differences Line Plot
- Shows how cumulative difference evolves over games
- Helps identify trends and consistency
- Steep upward slope = consistent advantage

#### 4. Winnings Over Games Line Plot
- Plots winnings of both agents for each game
- Shows performance over time
- Helps identify if one agent improves/declines

#### 5. Statistics Summary Bar Chart
- Side-by-side comparison of:
  - Average winnings per game
  - Mean difference
  - Standard deviation
- Quick visual summary of key metrics

#### 6. Win Rate Analysis Bar Chart
- Shows:
  - Number of games won by each agent
  - Win rates as percentages
- Complements mean difference analysis

---

## Running Experiments

### Lab 2d: Random vs Fixed Agent
```bash
python src/lab_2d.py
```
- Runs 100 games (50 hands each)
- Compares Random Agent vs Fixed Agent
- Outputs statistics and analysis

### Lab 2e: Reflex Agent Comparisons
```bash
python src/lab_2e.py
```
- Experiment 1: Reflex Agent vs Random Agent
- Experiment 2: Reflex Agent vs Fixed Agent
- Generates 12 plots in `plots/` directory
- Demonstrates reflex agent behavior

### Lab 2f: Memory Agent Comparison
```bash
python src/lab_2f.py
```
- Compares Reflex Agent with Memory vs without Memory
- Generates 6 plots in `plots/` directory
- Analyzes effectiveness of memory/opponent observation

### Viewing Plots
All plots are saved as PNG files in the `plots/` directory:
- High resolution (300 DPI)
- Descriptive filenames
- See `plots/README.md` for detailed plot descriptions

---

## Key Findings

### Reflex Agent Performance
- **vs Random Agent**: Significant advantage (~$400-600 per game)
- **vs Fixed Agent**: Significant advantage (~$400-600 per game)
- **Conclusion**: Using hand strength information dramatically improves performance

### Memory Agent Performance
- **vs Reflex Agent (No Memory)**: Small but consistent advantage (~$60-100 per game)
- **Conclusion**: Opponent observation provides additional value, but the simple adjustment strategy has limited impact

### Why Memory Helps
1. Opponent bids correlate with their hand strength (since they also use hand-based bidding)
2. Adjusting based on opponent signals allows:
   - Avoiding overcommitting against strong opponents
   - Capitalizing on weak opponents
3. Creates more adaptive, context-aware strategy

### Potential Improvements
1. **Proportional adjustments**: Scale adjustments based on bid amount difference
2. **Multi-phase analysis**: Track bidding trends across all phases
3. **Hand strength comparison**: Compare own hand vs inferred opponent strength
4. **Learning from showdown**: Use `observe_showdown()` to calibrate adjustments
5. **Pot odds**: Consider pot size in decision-making
6. **Adaptive thresholds**: Dynamic thresholds based on opponent patterns

---

## Conclusion

This project demonstrates the progression from simple to sophisticated poker agents:
1. **Random/Fixed**: Baseline strategies with no information use
2. **Reflex**: Uses hand strength information effectively
3. **Reflex with Memory**: Adds opponent observation for incremental improvement

The experiments show that:
- Information (hand strength) is valuable
- Opponent observation provides additional value
- Simple strategies can be effective
- More sophisticated strategies have room for improvement

All code is modular and extensible, making it easy to implement new agent strategies and compare their performance.


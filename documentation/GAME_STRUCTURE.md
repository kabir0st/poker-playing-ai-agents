# Game Structure and Rules

Complete documentation of the simplified poker game mechanics, rules, and structure.

## Game Overview

This is a simplified poker game designed specifically for AI agent experimentation. The game strips down traditional poker to its essential elements while maintaining strategic decision-making opportunities.

## Core Rules

### Players
- **Number**: Exactly 2 agents compete in each game
- **Type**: AI agents (no human players)
- **Objective**: Maximize the difference between your winnings and opponent's winnings

### Deck and Cards
- **Deck**: Standard 52-card deck
- **Suits**: 4 suits (spades ♠, hearts ♥, clubs ♣, diamonds ♦)
- **Ranks**: 13 ranks (2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A)
- **Suit Value**: All suits are equal (no suit hierarchy)
- **Card Format**: String representation (e.g., "As" = Ace of spades, "Kh" = King of hearts)

### Hand Structure
- **Cards per Hand**: Exactly 3 cards per agent
- **Dealing**: Random, non-overlapping hands
- **Visibility**:
  - Agents see only their own hand during bidding
  - Both hands revealed during showdown

### Game Structure
- **Hands per Game**: 50 hands
- **Games per Experiment**: Typically 100 games
- **Total Hands**: 5,000 hands per experiment (100 games × 50 hands)

## Hand Types and Scoring

With only 3 cards, there are exactly 3 possible hand types:

### 1. High Card
- **Description**: No pairs, no three-of-a-kind
- **Score Range**: 1-13
- **Calculation**: Score = rank value of highest card
- **Rank Values**:
  - 2 = 1, 3 = 2, 4 = 3, 5 = 4, 6 = 5, 7 = 6, 8 = 7, 9 = 8
  - T = 9, J = 10, Q = 11, K = 12, A = 13
- **Examples**:
  - ["2s", "5h", "Kc"] → Score = 12 (King is highest)
  - ["7s", "9h", "3c"] → Score = 8 (Nine is highest)

### 2. Pair
- **Description**: Two cards of the same rank
- **Score Range**: 14-26
- **Calculation**: Score = 14 + (rank value - 1)
- **Examples**:
  - Pair of 2s: ["2s", "2h", "Kc"] → Score = 14 + (1-1) = 14
  - Pair of 5s: ["5s", "5h", "2c"] → Score = 14 + (4-1) = 17
  - Pair of Aces: ["As", "Ah", "2c"] → Score = 14 + (13-1) = 26

### 3. Three of a Kind
- **Description**: All three cards have the same rank
- **Score Range**: 27-39
- **Calculation**: Score = 27 + (rank value - 1)
- **Examples**:
  - Three 2s: ["2s", "2h", "2c"] → Score = 27 + (1-1) = 27
  - Three 7s: ["7s", "7h", "7c"] → Score = 27 + (6-1) = 32
  - Three Aces: ["As", "Ah", "Ac"] → Score = 27 + (13-1) = 39

### Scoring Summary Table

| Hand Type | Score Range | Example | Score |
|-----------|-------------|---------|-------|
| High Card (2) | 1-13 | ["2s", "5h", "Kc"] | 12 |
| High Card (A) | 1-13 | ["As", "5h", "2c"] | 13 |
| Pair (2s) | 14-26 | ["2s", "2h", "Kc"] | 14 |
| Pair (Ks) | 14-26 | ["Ks", "Kh", "2c"] | 25 |
| Pair (As) | 14-26 | ["As", "Ah", "2c"] | 26 |
| Three (2s) | 27-39 | ["2s", "2h", "2c"] | 27 |
| Three (7s) | 27-39 | ["7s", "7h", "7c"] | 32 |
| Three (As) | 27-39 | ["As", "Ah", "Ac"] | 39 |

## Game Flow

Each hand consists of exactly 3 phases:

### Phase 1: Card Dealing
**Purpose**: Distribute cards to agents

**Process**:
1. Shuffle the 52-card deck
2. Deal 3 cards to Agent 1
3. Deal 3 cards to Agent 2 (non-overlapping)
4. Agents receive their hands via `receive_hand(hand)`

**Agent Information**:
- Agents see only their own hand
- Agents do not see opponent's hand yet

### Phase 2: Bidding (3 Rounds)
**Purpose**: Agents commit money to the pot

**Structure**: 3 sequential bidding phases

**Each Bidding Phase**:
1. Bidding order alternates each hand (randomly determined at start, then alternates)
   - If Agent 1 bids first: Agent 1 bids, then Agent 2 bids (sees Agent 1's bid)
   - If Agent 2 bids first: Agent 2 bids, then Agent 1 bids (sees Agent 2's bid)
2. Both bids are added to the pot
3. Agents can see:
   - Their own hand
   - Their own previous bids in this hand
   - Opponent's previous bids in this hand (including current phase if opponent bid first)

**Bidding Constraints**:
- Minimum bid: $0
- Maximum bid: $50 per phase
- No restrictions on bid changes between phases
- Agents can bid differently in each phase

**Pot Accumulation**:
- Pot starts at $0
- After Phase 1: pot = bid1_phase1 + bid2_phase1
- After Phase 2: pot = previous + bid1_phase2 + bid2_phase2
- After Phase 3: pot = previous + bid1_phase3 + bid2_phase3

**Example Bidding Sequence**:
```
Phase 1: Agent 1 bids $20, Agent 2 bids $30  → Pot = $50
Phase 2: Agent 1 bids $30, Agent 2 bids $25  → Pot = $105
Phase 3: Agent 1 bids $5,  Agent 2 bids $45 → Pot = $155
```

### Phase 3: Showdown
**Purpose**: Determine winner and distribute pot

**Process**:
1. Both agents reveal their hands
2. Calculate hand scores using `analyse_hand()`
3. Compare scores
4. Agents observe opponent's hand via `observe_showdown(opponent_hand)`

**Winner Determination**:
- Higher score wins
- If scores are equal, pot is split equally

**Pot Distribution**:
- Winner takes entire pot
- In case of tie: each agent receives pot ÷ 2

## Complete Hand Example

### Setup
- **Agent 1**: "Random Agent"
- **Agent 2**: "Fixed Agent"

### Phase 1: Card Dealing
```
Deck shuffled: [..., "4h", "Ks", "Kc", "5s", "5h", "5c", ...]

Agent 1 receives: ["4h", "Ks", "Kc"]
Agent 2 receives: ["5s", "5h", "5c"]
```

### Phase 2: Bidding

**Phase 1**:
- Agent 1 (Random): Bids $20 (random)
- Agent 2 (Fixed): Bids $25 (fixed)
- Pot: $45

**Phase 2**:
- Agent 1 (Random): Bids $30 (random)
- Agent 2 (Fixed): Bids $25 (fixed)
- Pot: $100

**Phase 3**:
- Agent 1 (Random): Bids $5 (random)
- Agent 2 (Fixed): Bids $25 (fixed)
- Pot: $130

### Phase 3: Showdown

**Hand Evaluation**:
- Agent 1: ["4h", "Ks", "Kc"]
  - Type: Pair of Kings
  - Rank value: 12 (K)
  - Score: 14 + (12-1) = 25

- Agent 2: ["5s", "5h", "5c"]
  - Type: Three of a Kind (5s)
  - Rank value: 4 (5)
  - Score: 27 + (4-1) = 30

**Result**:
- Agent 2 wins (score 30 > 25)
- Agent 2 receives $130
- Agent 1 receives $0

## Game Statistics

### Per-Game Metrics
- **Agent 1 Winnings**: Total money won by agent 1
- **Agent 2 Winnings**: Total money won by agent 2
- **Difference**: Agent 1 Winnings - Agent 2 Winnings

### Per-Hand Metrics
- **Pot Size**: Sum of all bids in the hand
- **Winner**: Agent with higher hand score
- **Hand Scores**: Numerical scores for both agents

## Money System

### Unlimited Bank
- Agents have unlimited money from a "central bank"
- No risk of bankruptcy
- Focus is on maximizing winnings difference, not survival

### Implications
- Agents can bid aggressively without fear
- Strategy focuses on optimal bidding, not bankroll management
- Performance measured by relative winnings, not absolute amounts

## Strategic Elements

### Information Available to Agents

**During Bidding**:
- Own hand (3 cards)
- Own previous bids in current hand
- Opponent's previous bids in current hand
- Current bidding phase number (1, 2, or 3)

**After Showdown**:
- Opponent's hand (all 3 cards)
- Opponent's hand score
- Final pot size
- Winner of the hand

### Strategic Considerations

1. **Hand Strength**: Stronger hands justify higher bids
2. **Opponent Behavior**: Opponent bids may indicate their hand strength
3. **Pot Size**: Larger pots increase potential winnings/losses
4. **Bidding Pattern**: Trends across phases may reveal information

### Key Decisions

1. **How much to bid?** Based on hand strength and opponent behavior
2. **When to bid high?** With strong hands or when opponent seems weak
3. **When to bid low?** With weak hands or when opponent seems strong
4. **How to interpret opponent bids?** Infer opponent hand strength

## Implementation Details

### Card Representation
- Format: `"{rank}{suit}"`
- Examples: `"As"`, `"Kh"`, `"2c"`, `"Td"`
- Rank values stored in `RANK_VALUES` dictionary

### Hand Evaluation
- Function: `analyse_hand(hand)` → returns integer score (1-39)
- Function: `identify_hand(hand)` → returns (hand_type, rank_value)

### Game Engine
- Class: `PokerGame`
- Methods:
  - `play_hand(hand_num)`: Play a single hand
  - `play_game()`: Play full game of 50 hands

### Agent Interface
- `receive_hand(hand)`: Called during card dealing
- `make_bid(phase, own_bids, opponent_bids)`: Called during each bidding phase
- `observe_showdown(opponent_hand)`: Called after showdown

## Variations and Extensions

### Possible Extensions
- More cards per hand (4, 5 cards)
- More bidding phases
- Bluffing detection
- Learning from past games
- Multi-agent tournaments
- Different scoring systems

### Current Limitations
- Only 3 cards per hand
- No community cards
- No betting rounds (just bidding phases)
- No folding option
- No bluffing mechanics
- No learning between games (by default)

## Summary

This simplified poker game provides:
- **Clear rules**: Easy to understand and implement
- **Strategic depth**: Hand strength and opponent observation matter
- **Measurable outcomes**: Clear scoring and winner determination
- **Extensibility**: Easy to add new agent strategies
- **Reproducibility**: Deterministic scoring with random card dealing

The game strikes a balance between simplicity (for experimentation) and complexity (for meaningful strategy comparison).


# Poker AI Lab - Agent Comparison Project

A simplified poker game environment for comparing different AI agent strategies, from simple random bidding to sophisticated reflex agents with memory.

## 📋 Overview

This project implements and compares multiple poker-playing agents in a simplified 3-card poker game. The goal is to understand how different information usage strategies affect agent performance.

## 🎯 Key Features

- **Multiple Agent Types**: Random, Fixed, Reflex, and Reflex with Memory
- **Comprehensive Experiments**: Statistical analysis with 100 games × 50 hands
- **Rich Visualizations**: 2 types of plots per experiment showing win rates and cumulative performance
- **Modular Architecture**: Easy to extend with new agent strategies

## 🚀 Quick Start

### Prerequisites
```bash
pip install matplotlib numpy tqdm
```

Or using the project's dependency manager:
```bash
uv sync  # or pip install -e .
```

### Run Experiments

```bash
# Compare Random vs Fixed agents
python src/lab_2d.py

# Compare Reflex agent vs Random and Fixed
python src/lab_2e.py

# Compare Reflex with Memory vs without Memory
python src/lab_2f.py
```

All plots are automatically generated in the `plots/` directory.

## 📁 Project Structure

```
poker-ai/
├── src/
│   ├── libs/              # Core game components
│   │   ├── agent.py       # Base Agent class
│   │   ├── cards.py       # Card generation
│   │   ├── hand_evaluation.py  # Hand scoring
│   │   └── poker_game.py  # Game engine
│   ├── lab_2a.py          # Random agent
│   ├── lab_2b.py          # Fixed agent
│   ├── lab_2c.py          # Game environment
│   ├── lab_2d.py          # Random vs Fixed comparison
│   ├── lab_2e.py          # Reflex agent experiments
│   ├── lab_2f.py          # Memory agent experiment
│   └── plotting_utils.py  # Visualization utilities
├── plots/                 # Generated visualization plots
├── documentation/         # Detailed documentation
│   ├── README.md          # Full documentation
│   ├── AGENTS.md          # Agent architecture guide
│   ├── QUICK_REFERENCE.md # Quick reference guide
│   ├── GAME_STRUCTURE.md  # Game rules and structure
│   ├── CODE_FLOW.md      # Code architecture and flow
│   └── FLOW_DIAGRAMS.md   # Visual flow diagrams
├── pyproject.toml         # Project dependencies
└── README.md              # This file
```

## 📊 Results Summary

| Agent Comparison | Mean Advantage | Win Rate | Key Finding |
|-----------------|----------------|----------|-------------|
| Random vs Fixed | ~$0/game | ~50% | Baseline strategies perform similarly |
| Reflex vs Random | ~$400-600/game | ~85-95% | Hand strength information is highly valuable |
| Reflex vs Fixed | ~$400-600/game | ~85-95% | Adaptive strategy beats fixed strategy |
| Reflex+Memory vs Reflex | ~$60-100/game | ~55-65% | Opponent observation provides incremental value |

**Note**: Win rate indicates the percentage of games (out of 100) where one agent had more total winnings after 50 hands than the other.

## 📚 Documentation

Comprehensive documentation is available in the [`documentation/`](documentation/) directory:

### Main Documentation
- **[Full Documentation](documentation/README.md)** - Complete guide covering game rules, architecture, agents, and statistics
- **[Quick Reference](documentation/QUICK_REFERENCE.md)** - Quick lookup guide for agents and statistics

### Detailed Guides
- **[Agent Architecture](documentation/AGENTS.md)** - Complete guide to all agent types, their creation, decision-making processes, and flow diagrams
- **[Game Structure](documentation/GAME_STRUCTURE.md)** - Complete game rules, hand types, scoring system, and game flow
- **[Code Flow](documentation/CODE_FLOW.md)** - Detailed architecture, data structures, component interactions, and execution flow
- **[Flow Diagrams](documentation/FLOW_DIAGRAMS.md)** - Visual Mermaid flowcharts for each lab experiment (Lab 2d, 2e, 2f)

## 🎮 Game Overview

A simplified poker game where:
- Two agents compete
- Each receives 3 cards
- 3 bidding phases per hand ($0-$50 per phase)
- Winner takes the pot based on hand strength
- 50 hands per game

**Hand Types:**
- High Card (Score: 1-13)
- Pair (Score: 14-26)
- Three of a Kind (Score: 27-39)

## 🤖 Agent Strategies

### 1. Random Agent
- Bids randomly ($0-$50)
- No information usage
- Baseline for comparison

### 2. Fixed Agent
- Always bids fixed amount ($25)
- Predictable strategy
- Baseline for comparison

### 3. Reflex Agent
- Bids based on hand strength
- Formula: `bid = (hand_score / 39) * 50`
- Uses available information effectively

### 4. Reflex Agent with Memory
- Hand strength + opponent observation and learning
- Learns bid-to-hand-strength ratios from showdown observations
- Predicts opponent hand strength from their bids
- Adjusts bid based on predicted hand strength comparison
- More adaptive and sophisticated strategy

## 📈 Visualizations and Findings

Each experiment generates 2 types of plots that provide comprehensive insights into agent performance:

### Plot Types

#### 1. Win Rate Analysis Plot
**File naming**: `{experiment}_win_rate_analysis.png`

This plot shows two side-by-side bar charts:

**Left Chart - Win Counts:**
- Number of games won by each agent
- Shows raw counts (e.g., "Agent 1: 65 wins, Agent 2: 35 wins")
- Includes tie counts if any games ended in a tie

**Right Chart - Win Rates:**
- Percentage of games won by each agent
- Shows win rates as percentages (e.g., "Agent 1: 65%, Agent 2: 35%")
- Includes tie rate percentage

**Important Note**: A "win" in this context means having **more total winnings after 50 hands**, not winning individual hands. Each game consists of 50 hands, and the agent with higher cumulative winnings at the end wins the game.

**What it tells us:**
- **Consistency**: How often one agent outperforms the other
- **Dominance**: Whether one agent consistently wins or if results are close
- **Reliability**: High win rate (>70%) indicates a strong, consistent advantage

#### 2. Cumulative Winnings After X Games Plot
**File naming**: `{experiment}_winnings_after_x_games.png`

This line plot shows:
- **X-axis**: Number of games played (1 to 100)
- **Y-axis**: Cumulative winnings (in dollars)
- **Two lines**: One for each agent showing cumulative winnings across all games

**What it tells us:**
- **Trend**: Whether one agent's advantage increases, decreases, or stays constant over time
- **Consistency**: Steep, steady upward slope indicates consistent advantage
- **Magnitude**: The vertical gap between lines shows the size of the advantage
- **Stability**: Parallel lines indicate stable performance difference

### Key Findings from Experiments

#### Lab 2d: Random vs Fixed Agent
**Plots**: `lab_2d_random_vs_fixed_*.png`

**Findings:**
- **Win Rate**: Approximately 50/50 split (no significant advantage)
- **Cumulative Winnings**: Lines remain close together, showing minimal difference
- **Conclusion**: Both baseline strategies perform similarly. Random bidding and fixed bidding are roughly equivalent when neither uses hand strength information.

#### Lab 2e: Reflex Agent Experiments

**Experiment 1: Reflex vs Random** (`lab_2e_*.png`)
- **Win Rate**: Reflex agent wins ~85-95% of games
- **Cumulative Winnings**: Reflex agent's line shows steep upward trend, diverging significantly from Random
- **Mean Advantage**: ~$400-600 per game
- **Conclusion**: Using hand strength information provides massive advantage. The Reflex agent consistently outperforms Random by bidding appropriately based on hand quality.

**Experiment 2: Reflex vs Fixed** (`lab_2e_e2_*.png`)
- **Win Rate**: Reflex agent wins ~85-95% of games
- **Cumulative Winnings**: Similar pattern to Experiment 1 - Reflex agent's line diverges strongly
- **Mean Advantage**: ~$400-600 per game
- **Conclusion**: Adaptive strategy (bidding based on hand strength) dramatically outperforms fixed strategy. The ability to adjust bids based on hand quality is crucial.

#### Lab 2f: Reflex with Memory vs Reflex without Memory
**Plots**: `lab_2f_reflex_memory_vs_no_memory_*.png`

**Findings:**
- **Win Rate**: Memory agent wins ~55-65% of games
- **Cumulative Winnings**: Memory agent's line shows gradual upward divergence
- **Mean Advantage**: ~$60-100 per game (smaller but consistent)
- **Conclusion**: Learning opponent patterns and predicting hand strength provides incremental but meaningful advantage. The memory agent's ability to learn from showdowns and adjust bids based on predicted opponent strength gives it a consistent edge.

### Interpreting the Plots

**Strong Advantage Indicators:**
- Win rate > 70%
- Cumulative winnings lines diverge significantly
- Steady upward trend in cumulative difference

**Weak Advantage Indicators:**
- Win rate 50-60%
- Cumulative winnings lines stay close together
- Small, gradual divergence

**No Advantage:**
- Win rate ~50%
- Cumulative winnings lines overlap or cross frequently
- No clear trend

### Example Plot Locations

All plots are saved in the `plots/` directory:
- `lab_2d_random_vs_fixed_win_rate_analysis.png`
- `lab_2d_random_vs_fixed_winnings_after_x_games.png`
- `lab_2e_win_rate_analysis.png`
- `lab_2e_winnings_after_x_games.png`
- `lab_2e_e2_win_rate_analysis.png`
- `lab_2e_e2_winnings_after_x_games.png`
- `lab_2f_reflex_memory_vs_no_memory_win_rate_analysis.png`
- `lab_2f_reflex_memory_vs_no_memory_winnings_after_x_games.png`

Plots are saved as high-resolution PNG files (300 DPI) suitable for presentations and reports.

## 🔬 Experiments

### Lab 2d: Random vs Fixed
Compares two baseline strategies to establish baseline performance.

### Lab 2e: Reflex Agent Comparisons
- Experiment 1: Reflex vs Random (generates plots with prefix `lab_2e`)
- Experiment 2: Reflex vs Fixed (generates plots with prefix `lab_2e_e2`)
- Demonstrates value of hand strength information

### Lab 2f: Memory Agent
Compares Reflex agent with and without memory to evaluate opponent observation value.

## 🛠️ Development

### Adding a New Agent

1. Create a new file (e.g., `lab_2x.py`)
2. Implement agent class inheriting from `Agent`
3. Implement `make_bid()` method
4. Optionally implement `observe_showdown()` for learning
5. Add comparison experiment

### Running Custom Experiments

```python
from libs.poker_game import PokerGame
from your_agent import create_your_agent

game = PokerGame(
    agent1_factory=lambda: create_your_agent("Agent 1"),
    agent2_factory=lambda: create_random_agent("Agent 2"),
    num_hands=50
)
result = game.play_game()
```

## 📝 License

This project is part of an AI labs course assignment.

## 👥 Authors

Created for AI Labs course - Poker Agent Comparison Project

---

For questions or issues, refer to the [documentation](documentation/README.md) or check the code comments.


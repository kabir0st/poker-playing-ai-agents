# Poker AI Lab - Agent Comparison Project

A simplified poker game environment for comparing different AI agent strategies, from simple random bidding to sophisticated reflex agents with memory.

## 📋 Overview

This project implements and compares multiple poker-playing agents in a simplified 3-card poker game. The goal is to understand how different information usage strategies affect agent performance.

## 🎯 Key Features

- **Multiple Agent Types**: Random, Fixed, Reflex, and Reflex with Memory
- **Comprehensive Experiments**: Statistical analysis with 100 games × 50 hands
- **Rich Visualizations**: 6 types of plots per experiment (18 total plots)
- **Modular Architecture**: Easy to extend with new agent strategies

## 🚀 Quick Start

### Prerequisites
```bash
pip install matplotlib numpy
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
│   ├── QUICK_REFERENCE.md # Quick reference guide
│   ├── GAME_STRUCTURE.md  # Game rules and structure
│   ├── CODE_FLOW.md      # Code architecture and flow
│   └── FLOW_DIAGRAMS.md   # Visual flow diagrams
└── README.md              # This file
```

## 📊 Results Summary

| Agent Comparison | Mean Advantage | Key Finding |
|-----------------|----------------|--------------|
| Reflex vs Random | ~$400-600/game | Hand strength information is highly valuable |
| Reflex vs Fixed | ~$400-600/game | Adaptive strategy beats fixed strategy |
| Reflex+Memory vs Reflex | ~$60-100/game | Opponent observation provides incremental value |

## 📚 Documentation

Comprehensive documentation is available in the [`documentation/`](documentation/) directory:

### Main Documentation
- **[Full Documentation](documentation/README.md)** - Complete guide covering game rules, architecture, agents, and statistics
- **[Quick Reference](documentation/QUICK_REFERENCE.md)** - Quick lookup guide for agents and statistics

### Detailed Guides
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
- Hand strength + opponent observation
- Adjusts bid based on opponent's last bid
- More adaptive strategy

## 📈 Visualizations

Each experiment generates 6 types of plots:
1. Bankroll differences histogram
2. Winnings comparison box plot
3. Cumulative differences over games
4. Winnings over games line plot
5. Statistics summary bar chart
6. Win rate analysis

See `plots/README.md` for detailed plot descriptions.

## 🔬 Experiments

### Lab 2d: Random vs Fixed
Compares two baseline strategies to establish baseline performance.

### Lab 2e: Reflex Agent Comparisons
- Experiment 1: Reflex vs Random
- Experiment 2: Reflex vs Fixed
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


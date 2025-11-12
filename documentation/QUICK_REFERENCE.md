# Quick Reference Guide

## Agent Comparison Summary

| Agent | Strategy | Information Used | Performance |
|-------|----------|------------------|-------------|
| **Random** | Random bids ($0-$50) | None | Baseline |
| **Fixed** | Fixed bid ($25) | None | Baseline |
| **Reflex** | Hand strength proportional | Own hand | ~$400-600 advantage vs Random/Fixed |
| **Reflex + Memory** | Hand strength + opponent adjustment | Own hand + opponent bids | ~$60-100 advantage vs Reflex |

## Key Statistics Explained

- **Mean Difference**: Average advantage per game (positive = Agent 1 better)
- **Std Deviation**: Variability in outcomes (lower = more consistent)
- **Win Rate**: Percentage of games won
- **Average Winnings**: Mean winnings per game

## File Locations

- **Documentation**: `documentation/README.md` (full documentation)
- **Plots**: `plots/` directory (PNG visualizations)
- **Source Code**: `src/` directory
- **Experiments**:
  - `src/lab_2d.py` - Random vs Fixed
  - `src/lab_2e.py` - Reflex agent experiments
  - `src/lab_2f.py` - Memory agent experiment

## Quick Commands

```bash
# Run all experiments
python src/lab_2d.py
python src/lab_2e.py
python src/lab_2f.py

# View plots
ls plots/*.png
```

## Hand Scoring

- **High Card**: 1-13 (rank value)
- **Pair**: 14-26 (14 + rank - 1)
- **Three of a Kind**: 27-39 (27 + rank - 1)

## Game Flow

1. **Deal**: 3 cards to each agent
2. **Bid**: 3 phases, $0-$50 per phase
3. **Showdown**: Compare scores, winner takes pot


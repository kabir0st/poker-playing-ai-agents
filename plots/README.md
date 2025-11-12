# Poker Agent Experiment Plots

This directory contains visualization plots generated from poker agent experiments.

## Lab 2e: Reflex Agent vs Random/Fixed Agents

### Experiment 1: Reflex Agent vs Random Agent
- `lab_2e_experiment1_reflex_vs_random_bankroll_differences.png` - Histogram showing distribution of bankroll differences
- `lab_2e_experiment1_reflex_vs_random_winnings_comparison.png` - Box plot comparing winnings distributions
- `lab_2e_experiment1_reflex_vs_random_cumulative_differences.png` - Line plot showing cumulative difference over games
- `lab_2e_experiment1_reflex_vs_random_winnings_over_games.png` - Line plot showing winnings of both agents over games
- `lab_2e_experiment1_reflex_vs_random_statistics_summary.png` - Bar charts comparing key statistics
- `lab_2e_experiment1_reflex_vs_random_win_rate_analysis.png` - Bar charts showing win counts and win rates

### Experiment 2: Reflex Agent vs Fixed Agent
- `lab_2e_experiment2_reflex_vs_fixed_bankroll_differences.png` - Histogram showing distribution of bankroll differences
- `lab_2e_experiment2_reflex_vs_fixed_winnings_comparison.png` - Box plot comparing winnings distributions
- `lab_2e_experiment2_reflex_vs_fixed_cumulative_differences.png` - Line plot showing cumulative difference over games
- `lab_2e_experiment2_reflex_vs_fixed_winnings_over_games.png` - Line plot showing winnings of both agents over games
- `lab_2e_experiment2_reflex_vs_fixed_statistics_summary.png` - Bar charts comparing key statistics
- `lab_2e_experiment2_reflex_vs_fixed_win_rate_analysis.png` - Bar charts showing win counts and win rates

## Lab 2f: Reflex Agent with Memory vs Without Memory

- `lab_2f_reflex_memory_vs_no_memory_bankroll_differences.png` - Histogram showing distribution of bankroll differences
- `lab_2f_reflex_memory_vs_no_memory_winnings_comparison.png` - Box plot comparing winnings distributions
- `lab_2f_reflex_memory_vs_no_memory_cumulative_differences.png` - Line plot showing cumulative difference over games
- `lab_2f_reflex_memory_vs_no_memory_winnings_over_games.png` - Line plot showing winnings of both agents over games
- `lab_2f_reflex_memory_vs_no_memory_statistics_summary.png` - Bar charts comparing key statistics
- `lab_2f_reflex_memory_vs_no_memory_win_rate_analysis.png` - Bar charts showing win counts and win rates

## Plot Types

### 1. Bankroll Differences Histogram
Shows the distribution of bankroll differences (Agent1 - Agent2) across all games. Includes mean and standard deviation lines.

### 2. Winnings Comparison Box Plot
Compares the distribution of winnings per game for both agents using box plots, showing median, quartiles, and outliers.

### 3. Cumulative Differences Line Plot
Shows how the cumulative bankroll difference evolves over the course of all games, helping visualize trends.

### 4. Winnings Over Games Line Plot
Plots the winnings of both agents for each game, allowing comparison of performance over time.

### 5. Statistics Summary Bar Chart
Side-by-side bar charts comparing:
- Average winnings per game for each agent
- Mean difference and standard deviation

### 6. Win Rate Analysis Bar Chart
Shows:
- Number of games won by each agent (and ties)
- Win rates as percentages

## Generating Plots

Plots are automatically generated when running:
- `python src/lab_2e.py` - Generates plots for both experiments
- `python src/lab_2f.py` - Generates plots for memory comparison

All plots are saved as PNG files with 300 DPI resolution.


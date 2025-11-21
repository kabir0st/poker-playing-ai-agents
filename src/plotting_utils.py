"""Plotting utilities for poker agent experiments."""

import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


def plot_winnings_after_x_games(results, output_dir, filename_prefix):
    """
    Plot cumulative winnings after different numbers of games.
    Plots raw data for all games.

    Parameters
    ----------
    results : dict
        Results dictionary from run_experiment
    output_dir : str
        Directory to save plots
    filename_prefix : str
        Prefix for filename
    """
    agent1_winnings = results['agent1_winnings']
    agent2_winnings = results['agent2_winnings']
    agent1_name = results['agent1_name']
    agent2_name = results['agent2_name']
    total_games = len(agent1_winnings)

    # Calculate cumulative winnings for all games (raw data)
    cumulative_agent1 = np.cumsum(agent1_winnings)
    cumulative_agent2 = np.cumsum(agent2_winnings)

    # Plot raw data - cumulative winnings for every game
    games = np.arange(1, total_games + 1)

    plt.figure(figsize=(12, 6))
    plt.plot(games,
             cumulative_agent1,
             linewidth=1.5,
             label=agent1_name,
             alpha=0.8,
             color='steelblue')
    plt.plot(games,
             cumulative_agent2,
             linewidth=1.5,
             label=agent2_name,
             alpha=0.8,
             color='coral')

    plt.xlabel('Number of Games', fontsize=12)
    plt.ylabel('Cumulative Winnings', fontsize=12)
    plt.title(
        f'Cumulative Winnings After X Games\n{agent1_name} vs {agent2_name}',
        fontsize=14,
        fontweight='bold')

    # Format y-axis to show dollar signs
    ax = plt.gca()
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axhline(0, color='black', linestyle='-', linewidth=1, alpha=0.3)

    plt.tight_layout()

    filepath = os.path.join(output_dir,
                            f'{filename_prefix}_winnings_after_x_games.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"  Saved: {filepath}")


def plot_win_rate_analysis(results, output_dir, filename_prefix):
    """
    Plot win rate analysis (how many games each agent won).

    Parameters
    ----------
    results : dict
        Results dictionary from run_experiment
    output_dir : str
        Directory to save plots
    filename_prefix : str
        Prefix for filename
    """
    differences = results['differences']
    agent1_name = results['agent1_name']
    agent2_name = results['agent2_name']

    agent1_wins = sum(1 for d in differences if d > 0)
    agent2_wins = sum(1 for d in differences if d < 0)
    ties = sum(1 for d in differences if d == 0)

    total_games = len(differences)
    win_rate1 = (agent1_wins / total_games) * 100
    win_rate2 = (agent2_wins / total_games) * 100
    tie_rate = (ties / total_games) * 100

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Win counts
    categories = [agent1_name, agent2_name, 'Ties']
    counts = [agent1_wins, agent2_wins, ties]
    colors = ['steelblue', 'coral', 'gray']

    bars1 = ax1.bar(categories,
                    counts,
                    color=colors,
                    alpha=0.7,
                    edgecolor='black')
    ax1.set_ylabel('Number of Games', fontsize=12)
    ax1.set_title('Win Counts', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')

    # Add value labels
    for bar, count in zip(bars1, counts):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2.,
                 height,
                 f'{count}',
                 ha='center',
                 va='bottom',
                 fontsize=11,
                 fontweight='bold')

    # Win rates
    rates = [win_rate1, win_rate2, tie_rate]
    bars2 = ax2.bar(categories,
                    rates,
                    color=colors,
                    alpha=0.7,
                    edgecolor='black')
    ax2.set_ylabel('Win Rate (%)', fontsize=12)
    ax2.set_title('Win Rates', fontsize=13, fontweight='bold')
    ax2.set_ylim([0, 100])
    ax2.grid(True, alpha=0.3, axis='y')

    # Add value labels
    for bar, rate in zip(bars2, rates):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2.,
                 height,
                 f'{rate:.1f}%',
                 ha='center',
                 va='bottom',
                 fontsize=11,
                 fontweight='bold')

    plt.suptitle(f'Win Rate Analysis: {agent1_name} vs {agent2_name}',
                 fontsize=14,
                 fontweight='bold',
                 y=1.02)
    plt.tight_layout()

    filepath = os.path.join(output_dir,
                            f'{filename_prefix}_win_rate_analysis.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"  Saved: {filepath}")


def generate_all_plots(results, output_dir, filename_prefix):
    """
    Generate selected plots for an experiment.

    Parameters
    ----------
    results : dict
        Results dictionary from run_experiment
    output_dir : str
        Directory to save plots
    filename_prefix : str
        Prefix for filename
    """
    print(f"\nGenerating plots for {filename_prefix}...")
    print("-" * 70)

    plot_win_rate_analysis(results, output_dir, filename_prefix)
    plot_winnings_after_x_games(results, output_dir, filename_prefix)

    print(f"All plots saved to: {output_dir}")

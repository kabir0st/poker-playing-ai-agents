"""Plotting utilities for poker agent experiments."""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import os


def plot_bankroll_differences(results, output_dir, filename_prefix):
    """
    Plot histogram of bankroll differences.

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
    mean_diff = results['mean_difference']
    std_diff = results['std_difference']

    plt.figure(figsize=(10, 6))
    plt.hist(differences, bins=30, edgecolor='black', alpha=0.7, color='steelblue')
    plt.axvline(mean_diff, color='red', linestyle='--', linewidth=2,
                label=f'Mean: ${mean_diff:.2f}')
    plt.axvline(mean_diff + std_diff, color='orange', linestyle='--', linewidth=1,
                label=f'Mean ± Std: ${mean_diff + std_diff:.2f}')
    plt.axvline(mean_diff - std_diff, color='orange', linestyle='--', linewidth=1)
    plt.axvline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)

    plt.xlabel(f'Bankroll Difference ({agent1_name} - {agent2_name})', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title(f'Distribution of Bankroll Differences\n{agent1_name} vs {agent2_name}',
              fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    filepath = os.path.join(output_dir, f'{filename_prefix}_bankroll_differences.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filepath}")


def plot_winnings_comparison(results, output_dir, filename_prefix):
    """
    Plot box plot comparing winnings of both agents.

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

    plt.figure(figsize=(10, 6))
    data = [agent1_winnings, agent2_winnings]
    labels = [agent1_name, agent2_name]

    bp = plt.boxplot(data, labels=labels, patch_artist=True,
                     boxprops=dict(facecolor='lightblue', alpha=0.7),
                     medianprops=dict(color='red', linewidth=2))

    plt.ylabel('Winnings per Game ($)', fontsize=12)
    plt.title(f'Winnings Comparison\n{agent1_name} vs {agent2_name}',
              fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()

    filepath = os.path.join(output_dir, f'{filename_prefix}_winnings_comparison.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filepath}")


def plot_cumulative_differences(results, output_dir, filename_prefix):
    """
    Plot cumulative bankroll differences over games.

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

    cumulative = np.cumsum(differences)
    games = range(1, len(differences) + 1)

    plt.figure(figsize=(12, 6))
    plt.plot(games, cumulative, linewidth=2, color='steelblue', label='Cumulative Difference')
    plt.axhline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)

    plt.xlabel('Game Number', fontsize=12)
    plt.ylabel(f'Cumulative Difference ({agent1_name} - {agent2_name})', fontsize=12)
    plt.title(f'Cumulative Bankroll Difference Over Games\n{agent1_name} vs {agent2_name}',
              fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    filepath = os.path.join(output_dir, f'{filename_prefix}_cumulative_differences.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filepath}")


def plot_winnings_over_games(results, output_dir, filename_prefix):
    """
    Plot winnings of both agents over games.

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

    games = range(1, len(agent1_winnings) + 1)

    plt.figure(figsize=(12, 6))
    plt.plot(games, agent1_winnings, linewidth=2, label=agent1_name, alpha=0.8)
    plt.plot(games, agent2_winnings, linewidth=2, label=agent2_name, alpha=0.8)

    plt.xlabel('Game Number', fontsize=12)
    plt.ylabel('Winnings per Game ($)', fontsize=12)
    plt.title(f'Winnings Over Games\n{agent1_name} vs {agent2_name}',
              fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    filepath = os.path.join(output_dir, f'{filename_prefix}_winnings_over_games.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filepath}")


def plot_statistics_summary(results, output_dir, filename_prefix):
    """
    Plot bar chart comparing key statistics.

    Parameters
    ----------
    results : dict
        Results dictionary from run_experiment
    output_dir : str
        Directory to save plots
    filename_prefix : str
        Prefix for filename
    """
    agent1_name = results['agent1_name']
    agent2_name = results['agent2_name']
    mean_agent1 = results['mean_agent1_winnings']
    mean_agent2 = results['mean_agent2_winnings']
    mean_diff = results['mean_difference']
    std_diff = results['std_difference']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Average winnings comparison
    agents = [agent1_name, agent2_name]
    means = [mean_agent1, mean_agent2]
    colors = ['steelblue', 'coral']

    bars1 = ax1.bar(agents, means, color=colors, alpha=0.7, edgecolor='black')
    ax1.set_ylabel('Average Winnings per Game ($)', fontsize=12)
    ax1.set_title('Average Winnings Comparison', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for bar, mean in zip(bars1, means):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'${mean:.2f}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Statistics summary
    stats_labels = ['Mean\nDifference', 'Std\nDeviation']
    stats_values = [mean_diff, std_diff]
    colors2 = ['green' if mean_diff > 0 else 'red', 'gray']

    bars2 = ax2.bar(stats_labels, stats_values, color=colors2, alpha=0.7, edgecolor='black')
    ax2.set_ylabel('Value ($)', fontsize=12)
    ax2.set_title('Difference Statistics', fontsize=13, fontweight='bold')
    ax2.axhline(0, color='black', linestyle='-', linewidth=1)
    ax2.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for bar, val in zip(bars2, stats_values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'${val:.2f}',
                ha='center', va='bottom' if height > 0 else 'top',
                fontsize=11, fontweight='bold')

    plt.suptitle(f'Statistics Summary: {agent1_name} vs {agent2_name}',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()

    filepath = os.path.join(output_dir, f'{filename_prefix}_statistics_summary.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
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

    bars1 = ax1.bar(categories, counts, color=colors, alpha=0.7, edgecolor='black')
    ax1.set_ylabel('Number of Games', fontsize=12)
    ax1.set_title('Win Counts', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')

    # Add value labels
    for bar, count in zip(bars1, counts):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Win rates
    rates = [win_rate1, win_rate2, tie_rate]
    bars2 = ax2.bar(categories, rates, color=colors, alpha=0.7, edgecolor='black')
    ax2.set_ylabel('Win Rate (%)', fontsize=12)
    ax2.set_title('Win Rates', fontsize=13, fontweight='bold')
    ax2.set_ylim([0, 100])
    ax2.grid(True, alpha=0.3, axis='y')

    # Add value labels
    for bar, rate in zip(bars2, rates):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{rate:.1f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    plt.suptitle(f'Win Rate Analysis: {agent1_name} vs {agent2_name}',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()

    filepath = os.path.join(output_dir, f'{filename_prefix}_win_rate_analysis.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filepath}")


def generate_all_plots(results, output_dir, filename_prefix):
    """
    Generate all plots for an experiment.

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

    plot_bankroll_differences(results, output_dir, filename_prefix)
    plot_winnings_comparison(results, output_dir, filename_prefix)
    plot_cumulative_differences(results, output_dir, filename_prefix)
    plot_winnings_over_games(results, output_dir, filename_prefix)
    plot_statistics_summary(results, output_dir, filename_prefix)
    plot_win_rate_analysis(results, output_dir, filename_prefix)

    print(f"All plots saved to: {output_dir}")


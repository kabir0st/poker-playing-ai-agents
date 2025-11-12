def _get_agent_type(agent_name):
    """
    Determine the agent type from its name.

    Parameters
    ----------
    agent_name : str
        Name of the agent

    Returns
    -------
    str
        Agent type: 'random', 'fixed', 'reflex_memory', 'reflex', or 'unknown'
    """
    name_lower = agent_name.lower()
    if 'random' in name_lower:
        return 'random'
    elif 'fixed' in name_lower:
        return 'fixed'
    elif 'memory' in name_lower and 'reflex' in name_lower:
        return 'reflex_memory'
    elif 'reflex' in name_lower:
        return 'reflex'
    else:
        return 'unknown'


def _print_strategy_analysis(agent_name, agent_type, results):
    """
    Print strategy analysis for a specific agent.

    Parameters
    ----------
    agent_name : str
        Name of the agent
    agent_type : str
        Type of the agent
    results : dict
        Results dictionary that may contain agent-specific info
    """
    print(f"  {agent_name} Strategy:")
    if agent_type == 'random':
        print("    - Bids randomly between $0-$50 each phase")
        print("    - Average bid per phase: ~$25 (uniform distribution)")
        print("    - Total average bid per hand: ~$75 (3 phases)")
    elif agent_type == 'fixed':
        fixed_bid = results.get('fixed_bid_amount', 25)
        print(f"    - Always bids ${fixed_bid} each phase")
        print(f"    - Total bid per hand: ${fixed_bid * 3} (3 phases)")
    elif agent_type == 'reflex':
        print("    - Evaluates hand strength (score 1-39)")
        print("    - Bids proportionally: bid = (hand_score / 39) * 50")
        print("    - Strong hands (27-39) bid high ($35-$50)")
        print("    - Medium hands (14-26) bid medium ($18-$33)")
        print("    - Weak hands (1-13) bid low ($1-$16)")
        print("    - Does not consider opponent bidding")
    elif agent_type == 'reflex_memory':
        print("    - Base bid from hand strength (like reflex agent)")
        print("    - Adjusts bid based on opponent's last bid:")
        print("      * Uses proportional adjustments based on opponent bid")
        print("      * Considers difference between opponent bid and")
        print("        expected bid (~$25 average)")
        print("      * Confidence-based scaling: stronger hands adjust")
        print("        more aggressively")
        print("      * Can react to opponent's bid in current phase")
    else:
        print("    - Strategy details unknown")


def analyze_results(results):
    """
    Analyze and print the results of the experiment.

    Supports all agent types: Random, Fixed, Reflex, Reflex with Memory.

    Parameters
    ----------
    results : dict
        Results dictionary from run_experiment containing:
        - num_games: int
        - num_hands: int
        - mean_difference: float
        - std_difference: float
        - mean_agent1_winnings: float
        - mean_agent2_winnings: float
        - agent1_name: str
        - agent2_name: str
        - fixed_bid_amount: int (optional, for fixed agents)
    """
    print("\n" + "-" * 70)
    print("EXPERIMENTAL RESULTS")
    print("-" * 70)

    print("\nConfiguration:")
    print(f"  Number of games: {results['num_games']}")
    print(f"  Hands per game: {results['num_hands']}")
    total_hands = results['num_games'] * results['num_hands']
    print(f"  Total hands played: {total_hands}")

    agent1_name = results.get('agent1_name', 'Agent 1')
    agent2_name = results.get('agent2_name', 'Agent 2')

    print(f"\nBankroll Difference Statistics "
          f"({agent1_name} - {agent2_name}):")
    print(f"  Mean difference: ${results['mean_difference']:.2f}")
    print(f"  Standard deviation: ${results['std_difference']:.2f}")

    print("\nAverage Winnings per Game:")
    print(f"  {agent1_name}: "
          f"${results['mean_agent1_winnings']:.2f}")
    print(f"  {agent2_name}: "
          f"${results['mean_agent2_winnings']:.2f}")

    # Determine which agent is better
    mean_diff = results['mean_difference']
    std_diff = results['std_difference']

    print("\n" + "-" * 70)
    print("ANALYSIS")
    print("-" * 70)

    if mean_diff > 0:
        better_agent = agent1_name
        worse_agent = agent2_name
        advantage = mean_diff
    elif mean_diff < 0:
        better_agent = agent2_name
        worse_agent = agent1_name
        advantage = abs(mean_diff)
    else:
        print("\nThe agents perform equally well on average.")
        # Still print strategy analysis even if equal
        print("\nStrategy Analysis:")
        agent1_type = _get_agent_type(agent1_name)
        agent2_type = _get_agent_type(agent2_name)
        _print_strategy_analysis(agent1_name, agent1_type, results)
        print()
        _print_strategy_analysis(agent2_name, agent2_type, results)
        return

    print("\nWhich agent is better?")
    print(f"  {better_agent} is better on average.")
    print(f"  Average advantage: ${advantage:.2f} per game")

    print("\nWhy?")
    print(f"  The mean bankroll difference is ${mean_diff:.2f}, "
          f"meaning {better_agent}")
    print(f"  wins ${advantage:.2f} more per game on average "
          f"than {worse_agent}.")

    # Additional insights
    print("\nAdditional Insights:")
    print(f"  1. Standard deviation of ${std_diff:.2f} indicates "
          "the variability")
    print("     in outcomes across games.")

    if abs(mean_diff) > 2 * std_diff:
        msg = "  2. The difference is statistically significant "
        msg += "(mean > 2*std),"
        print(msg)
        print(f"     suggesting a consistent advantage for "
              f"{better_agent}.")
    else:
        msg = "  2. The difference is relatively small compared "
        msg += "to variability,"
        print(msg)
        print("     suggesting the advantage may not be consistent.")

    # Strategy analysis
    print("\nStrategy Analysis:")
    agent1_type = _get_agent_type(agent1_name)
    agent2_type = _get_agent_type(agent2_name)

    _print_strategy_analysis(agent1_name, agent1_type, results)
    print()
    _print_strategy_analysis(agent2_name, agent2_type, results)

    # Key differences and theoretical analysis
    print("\n  Key Difference:")
    if agent1_type == 'random' and agent2_type == 'fixed':
        if mean_diff > 0:
            print("    Random agent's variable bidding may allow it to:")
            print("    - Bid higher when it has strong hands "
                  "(though it doesn't know)")
            print("    - Bid lower when it has weak hands (by chance)")
            print("    However, since random agent doesn't use hand "
                  "information,")
            print("    this advantage is purely coincidental.")
        else:
            print("    Fixed agent's consistent strategy provides:")
            print("    - Predictable pot sizes")
            print("    - No risk of over-bidding on weak hands")
            print("    - No risk of under-bidding on strong hands")
        print("\n    Theoretically, both agents should perform equally "
              "since:")
        print("    - Both have equal probability of getting "
              "good/bad hands")
        print("    - Neither uses hand information to make decisions")
        print("    - The difference is likely due to random variance")
    elif agent1_type == 'reflex' and agent2_type == 'random':
        print("    Reflex agent uses hand strength information to make")
        print("    informed bidding decisions, while random agent does not.")
        print("    This should give reflex agent an advantage.")
    elif agent1_type == 'reflex' and agent2_type == 'fixed':
        print("    Reflex agent adapts bids based on hand strength,")
        print("    while fixed agent uses a constant strategy.")
        print("    Reflex agent should outperform fixed agent by")
        print("    bidding appropriately for each hand.")
    elif agent1_type == 'reflex_memory' and agent2_type == 'reflex':
        print("    Reflex agent with memory considers opponent bidding")
        print("    patterns in addition to hand strength.")
        print("    This allows it to adjust strategy based on opponent")
        print("    behavior, potentially gaining an advantage.")
    elif agent2_type == 'reflex_memory' and agent1_type == 'reflex':
        print("    Reflex agent with memory considers opponent bidding")
        print("    patterns in addition to hand strength.")
        print("    This allows it to adjust strategy based on opponent")
        print("    behavior, potentially gaining an advantage.")

    # Statistical significance test
    print("\nStatistical Significance:")
    z_score = abs(mean_diff) / std_diff if std_diff > 0 else 0
    if z_score > 2:
        print(f"  Z-score: {z_score:.2f} (> 2.0)")
        msg = "  The difference is statistically significant at "
        msg += "95% confidence level."
        print(msg)
        print("  This suggests a real difference in performance, "
              "not just variance.")
    else:
        print(f"  Z-score: {z_score:.2f} (≤ 2.0)")
        print("  The difference is NOT statistically significant.")
        print("  The observed difference is likely due to random "
              "variance.")
        print("  Both agents perform equally well on average.")



def analyze_memory_effectiveness(results):
    """
    Analyze why memory agent performs better or worse.

    Parameters
    ----------
    results : dict
        Results dictionary from run_experiment
    """
    mean_diff = results['mean_difference']
    memory_agent_name = results['agent1_name'] if "Memory" in results['agent1_name'] else results['agent2_name']
    reflex_agent_name = results['agent2_name'] if "Memory" in results['agent1_name'] else results['agent1_name']

    print(f"\n" + "-" * 70)
    print("MEMORY AGENT ANALYSIS")
    print("-" * 70)

    if mean_diff > 0 and "Memory" in results['agent1_name']:
        print(f"\n✓ Memory agent performs BETTER than reflex agent without memory.")
        print(f"\nWhy memory helps:")
        print(f"  1. Opponent bidding provides information about their hand strength")
        print(f"  2. Adjusting bids based on opponent behavior allows:")
        print(f"     - Avoiding overcommitting when opponent is strong")
        print(f"     - Capitalizing when opponent is weak")
        print(f"  3. This creates a more adaptive strategy")
    elif mean_diff < 0 and "Memory" in results['agent1_name']:
        print(f"\n✗ Memory agent performs WORSE than reflex agent without memory.")
        print(f"\nWhy memory might hurt:")
        print(f"  1. The adjustment strategy might be too simplistic")
        print(f"  2. Opponent bidding may not reliably indicate hand strength")
        print(f"     (especially against a reflex agent that also bids based on hand)")
        print(f"  3. The fixed adjustment amounts (+$5/-$5) might not be optimal")
        print(f"  4. Both agents bid based on hand strength, so bids correlate")
        print(f"     with actual hand strength, making opponent bids informative")
        print(f"     but our adjustments might be counterproductive")
    elif mean_diff > 0 and "Memory" in results['agent2_name']:
        print(f"\n✗ Memory agent performs WORSE than reflex agent without memory.")
        print(f"\nWhy memory might hurt:")
        print(f"  1. The adjustment strategy might be too simplistic")
        print(f"  2. Opponent bidding may not reliably indicate hand strength")
        print(f"  3. The fixed adjustment amounts (+$5/-$5) might not be optimal")
    else:
        print(f"\n✓ Memory agent performs BETTER than reflex agent without memory.")
        print(f"\nWhy memory helps:")
        print(f"  1. Opponent bidding provides information about their hand strength")
        print(f"  2. Adjusting bids based on opponent behavior allows:")
        print(f"     - Avoiding overcommitting when opponent is strong")
        print(f"     - Capitalizing when opponent is weak")

    print(f"\n" + "-" * 70)
    print("POTENTIAL IMPROVEMENTS")
    print("-" * 70)
    print(f"\nTo improve the memory agent, consider:")
    print(f"\n1. More sophisticated adjustment strategy:")
    print(f"   - Use proportional adjustments based on opponent bid amount")
    print(f"   - Consider the difference between opponent bid and expected bid")
    print(f"   - Adjust more aggressively when confidence is high")
    print(f"\n2. Multi-phase memory:")
    print(f"   - Track opponent bidding pattern across all phases")
    print(f"   - Detect if opponent is increasing/decreasing bids")
    print(f"   - Use trend analysis to predict opponent strength")
    print(f"\n3. Hand strength comparison:")
    print(f"   - Compare own hand strength with inferred opponent strength")
    print(f"   - Only adjust when there's a significant difference")
    print(f"   - Be more aggressive when own hand is clearly stronger")
    print(f"\n4. Learning from showdown:")
    print(f"   - Use observe_showdown() to learn opponent patterns")
    print(f"   - Build a model of opponent bidding behavior")
    print(f"   - Calibrate adjustments based on historical accuracy")
    print(f"\n5. Pot odds consideration:")
    print(f"   - Consider current pot size when making adjustments")
    print(f"   - Calculate expected value based on hand strength and pot")
    print(f"   - Make adjustments that maximize expected value")
    print(f"\n6. Adaptive thresholds:")
    print(f"   - Instead of fixed thresholds ($20, $30), use dynamic ones")
    print(f"   - Base thresholds on opponent's average bidding pattern")
    print(f"   - Adjust thresholds based on game history")


    print("-" * 70)

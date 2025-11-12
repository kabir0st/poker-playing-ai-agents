Task 2: Poker game agent
Introduction
This part of the lab requires you to implement three different agents to play a simplified poker game,
the rules of the game are stated as follows:
• There will be two agents playing against each other within the game.
• We assume that coins/money are provided by the “central bank”, agents don’t play with their
own money and they have an unlimited amount of money to play. The goal for each agent is
to win as much money as possible while making the opponent win as little as possible. In other
words, the agents should be evaluated based on the difference between their winnings and the
winnings of their opponents.
• There are 52 cards in a deck, divided into four suits (i.e. spade, heart, club, and diamond) of 13
ranks each (i.e. Ace, K, Q, J, and from 2 to 10). The suits are all of equal value, i.e., no suit is
higher than any other suit.
• This is a simplified version of a poker game and agents are only dealing with hands of three
cards. The possible hands are “three of a kind”, “a pair” and the rest are “high cards”. Each of
these three types has a maximum of 13 ranks, corresponding to the number of variants in each
3
suit. Therefore, one way to evaluate the hand is to assign a score, according to the type and the
strength. For example, high cards can be assigned with scores ranging from 1 to 13; paris from
14 to 26; three-of-a-kind from 27 to 39.
• There will be 50 hands for each game.
• Each hand includes the following flow:
– Card dealing phase: assign a randomly generated hand (three cards) to each agent.
– Bidding phase (1-3): agents decide how much money ($0-50) they want to bid into the
pot. There are three bidding phases for every hand.
– Showdown phase: after three bidding phases, both agents show their hands, and the
agent with a stronger hand gets the pot.
– After every 50 hands compute the difference in winnings between the two agents.
Here is an example game flow of one hand:
• Card dealing phase, generate a random hand (3 cards) for each agent:
Agent 1 got a hand ‘4h, Ks, Kc’
Agent 2 got a hand ‘5s, 5h 5c’
• Bidding phase 1, two agents decide the amount of money to bid:
Agent 1 bids $20
Agent 2 bids $30
• Bidding phase 2:
Agent 1 bids $30
Agent 2 bids $25
• Bidding phase 3:
Agent 1 bids $5
Agent 2 bids $45
• Showdown phase, both agents show their hand. Agent 2 has a ‘three of a kind’ while Agent 1
has only a pair of King. Therefore, agent 2 wins and gets the pot, which is $155.
Tasks
2a. Implement a random agent that bids randomly.
2b. Implement a fixed agent.
2c. Build the environment of the game, and have the two agents play against each other. At this
point, you need to implement the following:
(a) game flow, according to the rules above.
(b) hand identification and strength evaluation function for this simplified poker game. Lab1.zip
contains a simple example that checks whether there is one pair in the hand.
(c) sensor input for the agents:
i. agent’s own hand (during card dealing phase)
ii. hand of opponent (during showdown phase)
iii. amount of money both agents bid (during betting phase).
(d) a way of recording the results.

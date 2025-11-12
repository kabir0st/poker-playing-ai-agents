# Flow Diagrams

Visual flowcharts for each lab experiment.

## Lab 2d: Random vs Fixed Agent Comparison

```mermaid
flowchart TD
    Start([Start Experiment]) --> Init[Initialize: 100 games, 50 hands/game]
    Init --> GameLoop{For each game<br/>1 to 100}

    GameLoop --> CreateAgents[Create Random Agent<br/>Create Fixed Agent]
    CreateAgents --> HandLoop{For each hand<br/>1 to 50}

    HandLoop --> Deal[Deal 3 cards to each agent]
    Deal --> Phase1[Phase 1: Bidding]
    Phase1 --> Random1[Random Agent:<br/>Bid random 0-50]
    Phase1 --> Fixed1[Fixed Agent:<br/>Bid 25]

    Random1 --> Phase2[Phase 2: Bidding]
    Fixed1 --> Phase2
    Phase2 --> Random2[Random Agent:<br/>Bid random 0-50]
    Phase2 --> Fixed2[Fixed Agent:<br/>Bid 25]

    Random2 --> Phase3[Phase 3: Bidding]
    Fixed2 --> Phase3
    Phase3 --> Random3[Random Agent:<br/>Bid random 0-50]
    Phase3 --> Fixed3[Fixed Agent:<br/>Bid 25]

    Random3 --> Showdown[Showdown:<br/>Compare hand scores]
    Fixed3 --> Showdown

    Showdown --> Winner{Determine Winner}
    Winner -->|Random wins| AddRandom[Add pot to Random]
    Winner -->|Fixed wins| AddFixed[Add pot to Fixed]
    Winner -->|Tie| SplitPot[Split pot]

    AddRandom --> Record[Record winnings]
    AddFixed --> Record
    SplitPot --> Record

    Record --> CheckHand{More hands?}
    CheckHand -->|Yes| HandLoop
    CheckHand -->|No| CalcDiff[Calculate difference:<br/>Random - Fixed]

    CalcDiff --> CheckGame{More games?}
    CheckGame -->|Yes| GameLoop
    CheckGame -->|No| Stats[Calculate Statistics:<br/>Mean, Std Dev]

    Stats --> Analysis[Analyze Results]
    Analysis --> End([End])

    style Start fill:#90EE90
    style End fill:#FFB6C1
    style Random1 fill:#87CEEB
    style Random2 fill:#87CEEB
    style Random3 fill:#87CEEB
    style Fixed1 fill:#DDA0DD
    style Fixed2 fill:#DDA0DD
    style Fixed3 fill:#DDA0DD
```

---

## Lab 2e: Reflex Agent Experiments

### Experiment 1: Reflex vs Random

```mermaid
flowchart TD
    Start([Start Experiment 1]) --> Init[Initialize: 100 games, 50 hands/game]
    Init --> GameLoop{For each game<br/>1 to 100}

    GameLoop --> CreateAgents[Create Reflex Agent<br/>Create Random Agent]
    CreateAgents --> HandLoop{For each hand<br/>1 to 50}

    HandLoop --> Deal[Deal 3 cards to each agent]
    Deal --> EvalReflex[Reflex Agent:<br/>Evaluate hand strength]

    EvalReflex --> CalcBid[Calculate bid:<br/>hand_score/39 * 50]

    CalcBid --> Phase1[Phase 1: Bidding]
    Phase1 --> Reflex1[Reflex Agent:<br/>Bid based on hand]
    Phase1 --> Random1[Random Agent:<br/>Bid random 0-50]

    Reflex1 --> Phase2[Phase 2: Bidding]
    Random1 --> Phase2
    Phase2 --> Reflex2[Reflex Agent:<br/>Bid based on hand]
    Phase2 --> Random2[Random Agent:<br/>Bid random 0-50]

    Reflex2 --> Phase3[Phase 3: Bidding]
    Random2 --> Phase3
    Phase3 --> Reflex3[Reflex Agent:<br/>Bid based on hand]
    Phase3 --> Random3[Random Agent:<br/>Bid random 0-50]

    Reflex3 --> Showdown[Showdown:<br/>Compare hand scores]
    Random3 --> Showdown

    Showdown --> Winner{Determine Winner}
    Winner -->|Reflex wins| AddReflex[Add pot to Reflex]
    Winner -->|Random wins| AddRandom[Add pot to Random]
    Winner -->|Tie| SplitPot[Split pot]

    AddReflex --> Record[Record winnings]
    AddRandom --> Record
    SplitPot --> Record

    Record --> CheckHand{More hands?}
    CheckHand -->|Yes| HandLoop
    CheckHand -->|No| CalcDiff[Calculate difference:<br/>Reflex - Random]

    CalcDiff --> CheckGame{More games?}
    CheckGame -->|Yes| GameLoop
    CheckGame -->|No| Stats[Calculate Statistics]

    Stats --> Plots[Generate 6 plots]
    Plots --> Analysis[Analyze Results]
    Analysis --> End([End Experiment 1])

    style Start fill:#90EE90
    style End fill:#FFB6C1
    style EvalReflex fill:#FFD700
    style CalcBid fill:#FFD700
    style Reflex1 fill:#87CEEB
    style Reflex2 fill:#87CEEB
    style Reflex3 fill:#87CEEB
    style Random1 fill:#DDA0DD
    style Random2 fill:#DDA0DD
    style Random3 fill:#DDA0DD
```

### Experiment 2: Reflex vs Fixed

```mermaid
flowchart TD
    Start([Start Experiment 2]) --> Init[Initialize: 100 games, 50 hands/game]
    Init --> GameLoop{For each game<br/>1 to 100}

    GameLoop --> CreateAgents[Create Reflex Agent<br/>Create Fixed Agent]
    CreateAgents --> HandLoop{For each hand<br/>1 to 50}

    HandLoop --> Deal[Deal 3 cards to each agent]
    Deal --> EvalReflex[Reflex Agent:<br/>Evaluate hand strength]

    EvalReflex --> CalcBid[Calculate bid:<br/>hand_score/39 * 50]

    CalcBid --> Phase1[Phase 1: Bidding]
    Phase1 --> Reflex1[Reflex Agent:<br/>Bid based on hand]
    Phase1 --> Fixed1[Fixed Agent:<br/>Bid 25]

    Reflex1 --> Phase2[Phase 2: Bidding]
    Fixed1 --> Phase2
    Phase2 --> Reflex2[Reflex Agent:<br/>Bid based on hand]
    Phase2 --> Fixed2[Fixed Agent:<br/>Bid 25]

    Reflex2 --> Phase3[Phase 3: Bidding]
    Fixed2 --> Phase3
    Phase3 --> Reflex3[Reflex Agent:<br/>Bid based on hand]
    Phase3 --> Fixed3[Fixed Agent:<br/>Bid 25]

    Reflex3 --> Showdown[Showdown:<br/>Compare hand scores]
    Fixed3 --> Showdown

    Showdown --> Winner{Determine Winner}
    Winner -->|Reflex wins| AddReflex[Add pot to Reflex]
    Winner -->|Fixed wins| AddFixed[Add pot to Fixed]
    Winner -->|Tie| SplitPot[Split pot]

    AddReflex --> Record[Record winnings]
    AddFixed --> Record
    SplitPot --> Record

    Record --> CheckHand{More hands?}
    CheckHand -->|Yes| HandLoop
    CheckHand -->|No| CalcDiff[Calculate difference:<br/>Reflex - Fixed]

    CalcDiff --> CheckGame{More games?}
    CheckGame -->|Yes| GameLoop
    CheckGame -->|No| Stats[Calculate Statistics]

    Stats --> Plots[Generate 6 plots]
    Plots --> Analysis[Analyze Results]
    Analysis --> End([End Experiment 2])

    style Start fill:#90EE90
    style End fill:#FFB6C1
    style EvalReflex fill:#FFD700
    style CalcBid fill:#FFD700
    style Reflex1 fill:#87CEEB
    style Reflex2 fill:#87CEEB
    style Reflex3 fill:#87CEEB
    style Fixed1 fill:#DDA0DD
    style Fixed2 fill:#DDA0DD
    style Fixed3 fill:#DDA0DD
```

---

## Lab 2f: Reflex Agent with Memory vs Without Memory

```mermaid
flowchart TD
    Start([Start Experiment]) --> Init[Initialize: 100 games, 50 hands/game]
    Init --> GameLoop{For each game<br/>1 to 100}

    GameLoop --> CreateAgents[Create Reflex Agent with Memory<br/>Create Reflex Agent without Memory]
    CreateAgents --> HandLoop{For each hand<br/>1 to 50}

    HandLoop --> Deal[Deal 3 cards to each agent]
    Deal --> EvalBoth[Both agents:<br/>Evaluate hand strength]

    EvalBoth --> CalcBaseBoth[Both calculate base bid:<br/>hand_score/39 * 50]

    CalcBaseBoth --> Phase1[Phase 1: Bidding]
    Phase1 --> Memory1[Memory Agent:<br/>Base bid + adjustment]
    Phase1 --> NoMemory1[No Memory Agent:<br/>Base bid only]

    Memory1 --> CheckOpp1{Opponent bid<br/>available?}
    CheckOpp1 -->|Yes| Adjust1[Adjust based on<br/>opponent bid]
    CheckOpp1 -->|No| NoAdjust1[No adjustment]
    Adjust1 --> Phase2[Phase 2: Bidding]
    NoAdjust1 --> Phase2

    NoMemory1 --> Phase2
    Phase2 --> Memory2[Memory Agent:<br/>Base bid + adjustment]
    Phase2 --> NoMemory2[No Memory Agent:<br/>Base bid only]

    Memory2 --> CheckOpp2{Opponent bid<br/>available?}
    CheckOpp2 -->|Yes| Adjust2[Adjust based on<br/>opponent bid]
    CheckOpp2 -->|No| NoAdjust2[No adjustment]
    Adjust2 --> Phase3[Phase 3: Bidding]
    NoAdjust2 --> Phase3

    NoMemory2 --> Phase3
    Phase3 --> Memory3[Memory Agent:<br/>Base bid + adjustment]
    Phase3 --> NoMemory3[No Memory Agent:<br/>Base bid only]

    Memory3 --> CheckOpp3{Opponent bid<br/>available?}
    CheckOpp3 -->|Yes| Adjust3[Adjust based on<br/>opponent bid]
    CheckOpp3 -->|No| NoAdjust3[No adjustment]
    Adjust3 --> Showdown[Showdown:<br/>Compare hand scores]
    NoAdjust3 --> Showdown

    NoMemory3 --> Showdown

    Showdown --> Winner{Determine Winner}
    Winner -->|Memory wins| AddMemory[Add pot to Memory]
    Winner -->|No Memory wins| AddNoMemory[Add pot to No Memory]
    Winner -->|Tie| SplitPot[Split pot]

    AddMemory --> Record[Record winnings]
    AddNoMemory --> Record
    SplitPot --> Record

    Record --> CheckHand{More hands?}
    CheckHand -->|Yes| HandLoop
    CheckHand -->|No| CalcDiff[Calculate difference:<br/>Memory - No Memory]

    CalcDiff --> CheckGame{More games?}
    CheckGame -->|Yes| GameLoop
    CheckGame -->|No| Stats[Calculate Statistics]

    Stats --> Plots[Generate 6 plots]
    Plots --> Analysis[Analyze Results]
    Analysis --> End([End])

    style Start fill:#90EE90
    style End fill:#FFB6C1
    style EvalBoth fill:#FFD700
    style CalcBaseBoth fill:#FFD700
    style Adjust1 fill:#FFA500
    style Adjust2 fill:#FFA500
    style Adjust3 fill:#FFA500
    style Memory1 fill:#87CEEB
    style Memory2 fill:#87CEEB
    style Memory3 fill:#87CEEB
    style NoMemory1 fill:#DDA0DD
    style NoMemory2 fill:#DDA0DD
    style NoMemory3 fill:#DDA0DD
```

---

## Memory Agent Adjustment Logic

```mermaid
flowchart TD
    Start([Memory Agent Bidding]) --> BaseBid[Calculate base bid<br/>from hand strength]
    BaseBid --> CheckOpp{Opponent has<br/>previous bids?}

    CheckOpp -->|No| NoAdjust[No adjustment<br/>Return base bid]
    CheckOpp -->|Yes| GetLast[Get last opponent bid]

    GetLast --> Compare{Compare bid}
    Compare -->|> $30| HighBid[Opponent bid high<br/>Reduce by $5]
    Compare -->|< $20| LowBid[Opponent bid low<br/>Increase by $5]
    Compare -->|$20-$30| Neutral[No adjustment]

    HighBid --> Apply[Apply adjustment]
    LowBid --> Apply
    Neutral --> Apply

    Apply --> Clamp[Clamp to 0-50 range]
    Clamp --> Return[Return final bid]
    NoAdjust --> Return

    Return --> End([End])

    style Start fill:#90EE90
    style End fill:#FFB6C1
    style HighBid fill:#FF6B6B
    style LowBid fill:#51CF66
    style Neutral fill:#FFD93D
```

---

## Overall Experiment Flow

```mermaid
flowchart LR
    Start([Start]) --> Lab2d[Lab 2d:<br/>Random vs Fixed]
    Lab2d --> Lab2e[Lab 2e:<br/>Reflex Experiments]
    Lab2e --> Lab2f[Lab 2f:<br/>Memory Experiment]

    Lab2d --> Plots1[Generate 6 plots]
    Lab2e --> Plots2[Generate 12 plots]
    Lab2f --> Plots3[Generate 6 plots]

    Plots1 --> Analysis1[Analyze Results]
    Plots2 --> Analysis2[Analyze Results]
    Plots3 --> Analysis3[Analyze Results]

    Analysis1 --> Report1[Report Statistics]
    Analysis2 --> Report2[Report Statistics]
    Analysis3 --> Report3[Report Statistics]

    Report1 --> End([End])
    Report2 --> End
    Report3 --> End

    style Start fill:#90EE90
    style End fill:#FFB6C1
    style Lab2d fill:#87CEEB
    style Lab2e fill:#87CEEB
    style Lab2f fill:#87CEEB
```

---

## Note on Diagrams

These diagrams use Mermaid syntax. To view them:
- GitHub automatically renders Mermaid diagrams
- Use online Mermaid editors: https://mermaid.live/
- VS Code with Mermaid extension
- Many markdown viewers support Mermaid

For ASCII-style diagrams, see the code comments in each lab file.


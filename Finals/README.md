# <div align="center">**Reinforcement Learning - Finals**</div>

* Implement Q-learning in the tic-tac-toe game setting.

* Steps:
    
    0) Change the probability transition function to have probability 1 (for all actions) to empty board on all terminal states.

    1) Generate a trajectory starting from empty board as follows:
        
        a) Start from empty board state,
        
        b) Choose one action uniformly at random from all the possible actions from that state,
        
        c) Choose the next state using the probability transition function,
        
        d) Obtain the reward for the transition,
        
        e) Continue this process on the next state.
    2) Update Q-value using Q-learning for each transition.

    3) Stop the process after sufficiently long iteration (5-10 million transitions.)

    4) Find the optimal policy from the Q-value.

    5) Apply the optimal policy to the game and play for 1000 games and print the outcomes (wins/loses/ties.)
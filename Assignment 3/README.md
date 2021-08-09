# <div align="center">**Reinforcement Learning - Assignment 3**</div>

* Implement `Value Iteration` and `Policy Iteration` on the tictactoe game to find the optimal policy. Then apply this policy to play the game.

* Play 1000 games and find the ratio of wins + ties to losses.

* Before that, you require some pre-requisites:
    1) Develop a reward function `R`. The reward function can reward
        - 100 points for transition to a win board configuration.
        - minus 100 for transition to loss board configuration.
        - 10 points for transition to tie board configuration.

    2) Out of the 3139 states some states are win configuration; some are loss configuration and some are tie configuration (We call them "terminal states")
        - We should change the probability transition from these terminal states. The probability transition from these states should only have transition (probability 1) to state 0 (empty board). There is no meaning in having a probability transition from these terminal states.

        - It is better to keep additional info with states to specify whether it is a win/ loss /tie configuration. Scan through the states in the pre-processing to mark these states. You can use the isgameover function.

    3) So reward function is easy R(x; a; y) = 100 if y is win
        - R(x; a; y) = -100 if y is loss
        - R(x;a; y) = 10 if y is ties
        - R(x;a;y) = 0 othewise
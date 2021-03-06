# Index

*   [DMC](algorithms.md#deep-monte-carlo)
*   [Deep-Q Learning](algorithms.md#deep-q-learning)
*   [NFSP](algorithms.md#nfsp)
*   [CFR (chance sampling)](algorithms.md#cfr)

## Deep Monte-Carlo
Deep Monte-Carlo (DMC) is a very effective algorithm for card games. This is the only algorithm that shows human-level performance on complex games such as Dou Dizhu.

## Deep-Q Learning
Deep-Q Learning (DQN) [[paper]](https://arxiv.org/abs/1312.5602) is a basic reinforcement learning (RL) algorithm. We wrap DQN as an example to show how RL algorithms can be connected to the environments. In the DQN agent, the following classes are implemented:

*   `DQNAgent`: The agent class that interacts with the environment.
*   `Memory`: A memory buffer that manages the storing and sampling of transitions.
*   `Estimator`: The neural network that is used to make predictions.

## NFSP
Neural Fictitious Self-Play (NFSP) [[paper]](https://arxiv.org/abs/1603.01121) end-to-end approach to solve card games with deep reinforcement learning. NFSP has an inner RL agent and a supervised agent that is trained based on the data generated by the RL agent. In the toolkit, we use DQN as RL agent.

## CFR (chance sampling)
Counterfactual Regret Minimization (CFR) [[paper]](http://papers.nips.cc/paper/3306-regret-minimization-in-games-with-incomplete-information.pdf) is a regret minimizaiton method for solving imperfect information games.

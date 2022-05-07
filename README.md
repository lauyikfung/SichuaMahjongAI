# SichuaMahjongAI
## Motivation & Background 
Artificial Intelligence (AI) has achieved great success in many domains, including playing games against human players. AI has defeated human top players in many games, such as Go game, Chess, Texas Hold’em Poker and DoTA. In some other games, such as Japanese mahjong, although AI does not occupy an overwhelming position, it also exceeds the average level of human masters. All members of our group are fond of playing mahjong. So we choose Sichuan mahjong as our research object and we would like to design an AI that can help us a lot on online gaming platforms.
## Problem Statement 
We will train a model for Sichuan mah-jong that decides whether to Pung, Kong, and which tile to discard automatically. It focus on making the tiles into certain structures and aims at getting a higher score while avoiding another player to win the game. It need to guess other players’ tiles and balance the strategy of attack and defence. We will evaluate our model’s performance by evaluating its winning rate and average scores. If possible, we will also let our model to play in real-time multi-player arenas and check the rank our model can achieve.
## Related Work 
According to [1, Yajun Zheng & Shuqin Li], there are a lot of AI models of Mahjong, especially International Mahjong and Japanese Mahjong, such as opponent models based on logistic regression, strategy or deep learning, and deep learning-based and deep reinforcement learning based models. The most renowned work is [2, J. Li et al., 2020], which has demonstrated a complicated model on Japanese Mahjong using self-play based deep reinforcement learning with ResNet and GRU networks, and guiding the training procedure by cheating oracles. And another similar work has provided a simpler convolutional neural networks for 3-Player Japanese Mahjong via self-play reinforcement learning using the Monte Carlo policy gradient method [3, Xiangyu Zhao & Sean B. Holden, 2022]. Moreover, both of the 2 models construct one model for each of the actions including Discard, Riichi, Chow, Pong and Kong, hence they consume a lot of calculation, has higher requirements on computer hardware, and is difficult to reproduce. However, there are few deep learning networks on Sichuan mahjong.
## References
+ [1] Yajun Zheng & Shuqin Li. A Review of Mahjong AI Research. https://dl.acm.org/doi/pdf/10.1145/3438872.3439104, 2020.
+ [2] J. Li et al. Suphx: Mastering Mahjong with Deep Reinforcement Learning. arXiv preprint arXiv:2003.13590, 2020.
+ [3] Xiangyu Zhao & Sean B. Holden. Building a 3-Player Mahjong AI using Deep Reinforcement Learning. arXiv preprint arXiv:2202.12847, 2022.

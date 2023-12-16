# Board Game AI Strategies

## Description
This repository contains a Python-based implementation of various AI strategies for playing different board games 
like TicTacToe, Connect4, and Boop. It includes implementations for Human players, Minimax, AlphaBeta, 
Monte Carlo Tree Search (MCTS), and a MCTS Solver. This project is aimed at exploring AI in board games and providing 
an interactive platform for testing different AI strategies.

## Installation
To run the games and AI strategies, you will need Python installed on your machine.

1. Clone the repository:
   ```sh
   git clone https://github.com/lrubiorod/boardgameBots.git
   ```
2. Navigate to the cloned directory:
   ```sh
    cd boardgameBots
   ```
3. (Optional) Set up a virtual environment:
   ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

## Usage

Run the main.py script to start a game. You will be prompted to choose the game and the type of players. 
You can select between human players and various AI strategies.

   ```sh
    python main.py
   ```

Follow the on-screen instructions to play the game.

## Games

- [**TicTacToe**](https://boardgamegeek.com/boardgame/11901/tic-tac-toe): The classic 3x3 grid game.
- [**Connect4**](https://boardgamegeek.com/boardgame/2719/connect-four): The popular 4-in-a-row game. 
- [**Boop.**](https://boardgamegeek.com/boardgame/355433/boop): A deceptively cute, deceivingly challenging abstract 
strategy game for two players. 

## AI Strategies

- **Human**: Manually choose moves. 
- **Minimax**: Basic Minimax algorithm.
- **AlphaBeta**: Minimax with Alpha-Beta pruning.
- **MCTS**: Monte Carlo Tree Search.
- **MCTS-Solver**: MCTS with added solving capabilities.
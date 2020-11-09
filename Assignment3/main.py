from game import Game
from agent import MinimaxPlayer, RandomPlayer
from util import get_arg
from connect3 import State
from human import HumanPlayer

if __name__ == '__main__':
    arg1 = get_arg(1)
    arg2 = get_arg(2)
    if arg1 and arg2:
        player1, player2 = None, None
        if arg1 == 'human':
            player1 = HumanPlayer('X')
        elif arg1 == 'random':
            player1 = RandomPlayer('X')
        elif arg1 == 'minimax':
            player1 = MinimaxPlayer('X')
        else:
            print('Invalid Input for Player1. Try Again.')
            exit(1)
        if arg2 == 'human':
            player2 = HumanPlayer('O')
        elif arg2 == 'random':
            player2 = RandomPlayer('O')
        elif arg2 == 'minimax':
            player2 = MinimaxPlayer('O')
        else:
            print('Invalid Input for Player2. Try Again.')
            exit(1)
        
        game = Game(State(), player1, player2)
        game.play()
    else:
        print('Invalid Input. Try Again.')

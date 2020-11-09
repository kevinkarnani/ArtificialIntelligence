from connect3 import State
from util import pprint

class Player:
    def __init__(self, character: str):
        self.character = character
    
    def choose_action(self, state: State):
        pass

class Game:
    def __init__(self, state: State, player1: Player, player2: Player):
        self.state = state
        self.player1 = player1
        self.player2 = player2
    
    def play(self):
        state_list = [self.state]
        while not self.state.game_over():
            self.state = self.state.clone().execute(self.player1.choose_action(self.state))
            pprint(self.state)
            state_list.append(self.state)
            if self.state.game_over():
                break
            self.state = self.state.clone().execute(self.player2.choose_action(self.state))
            pprint(self.state)
            state_list.append(self.state)
        pprint(state_list)
        print(f'{self.state.winner()} wins!')
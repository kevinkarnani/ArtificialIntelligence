from connect3 import State
from game import Player

class HumanPlayer(Player):
    def __init__(self, character: str):
        super().__init__(character)
    
    def choose_action(self, state: State):
        super().choose_action(state)
        action_list = state.actions(self.character)
        for index, action in enumerate(action_list):
            print(f'{index}: {action}')
        inp = int(input('Please choose an action:\n'))
        return action_list[inp] if inp in range(len(action_list)) else None

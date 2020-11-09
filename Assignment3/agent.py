from connect3 import State
from game import Player
from random import randrange

class RandomPlayer(Player):
    def __init__(self, character: str):
        super().__init__(character)
    
    def choose_action(self, state: State):
        super().choose_action(state)
        action_list = state.actions(self.character)
        return action_list[randrange(len(action_list))]

class MinimaxPlayer(Player):
    def __init__(self, character: str):
        super().__init__(character)
    
    def choose_action(self, state: State):
        def eval(state: State, character: str):
            eval_list = []
            for action in state.actions(character):
                new_state = state.clone().execute(action)
                score = 0
                if new_state.winner() == 'X':
                    score = 100
                elif new_state.winner():
                    score = -100 
                elif new_state.num_empties() == 0:
                    score = 0
                else:
                    my_two = count_streak(state, character, 2)
                    my_one = count_streak(state, character, 1)
                    opp = 'O' if character == 'X' else 'X'
                    opp_two = count_streak(state, opp, 2)
                    opp_one = count_streak(state, opp, 1)
                    score += (my_two * 10 + my_one)
                    score -= (opp_two * 10 + opp_one)
                eval_list.append(score)
            return eval_list

        def count_streak(state: State, character: str, num: int):
            count = 0
            for row in range(state.max_y):
                for col in range(state.max_x):
                    if state.board[row][col] == character:
                        '''Vertical'''
                        vert_count = 0
                        for i in range(row, 3):
                            if state.board[i][col] == state.board[row][col]:
                                vert_count += 1
                            else:
                                break
                        if vert_count >= num:
                            vert_count = 1
                        else:
                            vert_count = 0
                        count += vert_count
                        '''Horizontal'''
                        hor_count = 0
                        for j in range(col, 4):
                            if state.board[row][j] == state.board[row][col]:
                                hor_count += 1
                            else:
                                break
                        if hor_count >= num:
                            hor_count = 1
                        else:
                            hor_count = 0
                        count += hor_count
                        '''Diagonal'''
                        diag_count = 0
                        j = col
                        for i in range(row, -1, -1):
                            if j > 6:
                                break
                            elif state.board[i][j] == state.board[row][col]:
                                diag_count += 1
                            else:
                                break
                        if diag_count >= num:
                            diag_count = 1
                        else:
                            diag_count = 0
                        count += diag_count
            return count

        super().choose_action(state)
        action_list = state.actions(self.character)
        eval_list = eval(state, self.character)
        return action_list[eval_list.index(max(eval_list))] if self.character == 'X' else action_list[eval_list.index(min(eval_list))]
'''
    Author: Kevin Karnani
    Class: CS 380 (Artificial Intelligence)
    Professor: Jeffrey Popyack
    Date: 10/9/2020
    Language: Python 3.9
    Purpose: To represent a	single state of	the	rotator puzzle,	to compute possible next states
             after executing a single action, and to execute a simple walkthrough the state space.
'''

from sys import argv

class State:
    '''
        Class designed to keep track of the state of the puzzle.

        -----------
            state: str - The locations of the tiles on the puzzle where each row gets separated by a |.
    '''
    def __init__(self, state: str):
        self.state: str = state
        self.rows: list[str] = state.split('|')
    
    def __eq__(self, obj):
        '''
            Check to see if two states are equal.
        '''
        return isinstance(obj, self.__class__) and self.state == obj.state
    
    def print_state(self) -> None:
        '''
            Prints the current state.
        '''
        print(self.state)

    def is_goal(self) -> None:
        '''
            Checks to see if the current state is a goal state.
        '''
        index: int = None
        for row in self.rows:
            if ' ' in row:
                index = row.index(' ')
        rows: list[str] = [row.replace(row[index], '') for row in self.rows if index is not None]
        print(rows.count(rows[0]) == len(rows))

    def actions(self) -> str:
        '''
            Prints and returns a string of all possible actions that can be taken in the current state.
        '''
        position: list[int] = []
        actions: str = ''
        for index in range(len(self.rows)):
            actions += f'rotate({index}, -1)\nrotate({index}, 1)\n'
        for index, row in enumerate(self.rows):
            if ' ' in row:
                position.append(row.index(' '))
                position.append(index)
        if position[1] - 1 in range(len(self.rows)):
            actions += f'slide({position[0]}, {position[1] - 1}, {position[0]}, {position[1]})'
        if position[1] - 1 in range(len(self.rows)) and position[1] + 1 in range(len(self.rows)):
            actions += '\n'
        if position[1] + 1 in range(len(self.rows)):
            actions += f'slide({position[0]}, {position[1] + 1}, {position[0]}, {position[1]})'
        return actions

    def execute(self, action: str):
        '''
            Executes a specified action.

            ---------
                action: str - string of the command with the parameters
        '''
        l_paren = action.index('(')
        return eval(f'{action[:l_paren]}(self, {action[l_paren + 1:]}')

    def walk(self, i: int) -> None:
        '''
            Executes a specified action until a previously seen state is encountered.

            ----------
                i: int - index of action to take.
        '''
        states: list[State] = [self]
        print(self.state)
        for state in states:
            action: str = state.actions().splitlines()[i]
            new_state: State = self.execute(action)
            if new_state not in states:
                states.append(new_state)
                print(new_state.state)


class Action:
    '''
        Class designed to store actions that can be performed upon a state.

        -----------
            type: str - Describes the nature of the action that will take place. 
    '''
    def __init__(self, type: str):
        self.type: str = type
    
    def __str__(self) -> None:
        '''
            String overloading, allowing for a class variable to be printed.
        '''
        print(self.type)

def slide(state: State, x: int, y: int, x2: int, y2: int) -> State:
    '''
        Slides a tile into the empty tile's position. When y = 0, we assume we are at the top row.

        -----------
            x: int - Column of the tile to move.
            y: int - Row of the tile to move.
            x2: int - Column of the empty tile.
            y2: int - Row of the empty tile.
    '''
    if [x, y] == [x2, y2]:
        print('Coordinates are the same. Try again.')
        exit(0)
    if state.rows[y2][x2] != ' ':
        print('[y2, x2] is not the location of the empty tile. Try again.')
        exit(0)
    init_row, init_tile = state.rows[y], state.rows[y][x]
    dest_row, dest_tile = state.rows[y2], state.rows[y2][x2]
    init_row = init_row[:x] + dest_tile + init_row[x + 1:]
    dest_row = dest_row[:x2] + init_tile + dest_row[x + 1:]
    state.rows[y] = init_row
    state.rows[y2] = dest_row
    return State('|'.join(state.rows))

def rotate(state: State, y: int, dx: int) -> State:
    '''
        Rotates a specified row by a specified amount of tiles.

        -----------
            y: int - Row to rotate.
            dx: int - Number of times to rotate.
    '''
    row: str = state.rows[y]
    while(abs(dx)):
        if dx > 0:
            row = row[len(row) - 1] + row[:-1]
            dx -= 1
        else:
            row = row[1:] + row[0]
            dx += 1
    state.rows[y] = row
    return State('|'.join(state.rows))

if __name__ == '__main__':
    if len(argv) < 2:
        print('Please provide at least one argument.')
        exit(0)
    args = argv[1:]
    input_state: str = '12345|1234 |12354'
    if len(args) > 1:
        input_state = args[1]
    state: State = State(input_state)
    if args[0] == 'print':
        state.print_state()
    elif args[0] == 'goal':
        state.is_goal()
    elif args[0] == 'actions':
        print(state.actions())
    elif args[0][:4] == "walk" and len(args[0][4:]) == 1:
        state.walk(int(args[0][4:]))
    else:
        print('Invalid Input.')
        exit(0)

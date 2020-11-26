import json
import os
import random

from .state import State


class Q_State(State):
    '''Augments the game state with Q-learning information'''

    def __init__(self, string):
        super().__init__(string)

        # key stores the state's key string (see notes in _compute_key())
        self.key = self._compute_key()

    def _compute_key(self):
        '''
        Returns a key used to index this state.

        The key should reduce the entire game state to something much smaller
        that can be used for learning. When implementing a Q table as a
        dictionary, this key is used for accessing the Q values for this
        state within the dictionary.
        '''

        # this produces a 3 x 3 grid around the frog
        # and combines them into a key string
        return ''.join([
            self.get(self.frog_x - 1, self.frog_y - 1) or '_',
            self.get(self.frog_x, self.frog_y - 1) or '_',
            self.get(self.frog_x + 1, self.frog_y - 1) or '_',
            self.get(self.frog_x - 1, self.frog_y) or '_',
            self.get(self.frog_x + 1, self.frog_y) or '_',
            self.get(self.frog_x - 1, self.frog_y + 1) or '_',
            self.get(self.frog_x, self.frog_y + 1) or '_',
            self.get(self.frog_x + 1, self.frog_y + 1) or '_',
        ])

    def reward(self):
        '''Returns a reward value for the state.'''

        if self.at_goal:
            return self.score
        elif self.is_done:
            return -1000 + (self.max_y - self.frog_y) * 100
        elif '_' in self.key:
            return -10
        else:
            return 0


class Agent:

    def __init__(self, train=None):

        # train is either a string denoting the name of the saved
        # Q-table file, or None if running without training
        self.train = train

        # q is the dictionary representing the Q-table
        self.q = {}

        # keeps track of the previous state
        self.previous_state = None

        # keeps track of previous action
        self.previous_action = None

        # name is the Q-table filename
        # (you likely don't need to use or change this)
        self.name = train or 'q'

        # path is the path to the Q-table file
        # (you likely don't need to use or change this)
        self.path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'train', self.name + '.json')

        self.load()

    def load(self):
        '''Loads the Q-table from the JSON file'''
        try:
            with open(self.path, 'r') as f:
                self.q = json.load(f)
            if self.train:
                print('Training {}'.format(self.path))
            else:
                print('Loaded {}'.format(self.path))
        except IOError:
            if self.train:
                print('Training {}'.format(self.path))
            else:
                raise Exception('File does not exist: {}'.format(self.path))
        return self

    def save(self):
        '''Saves the Q-table to the JSON file'''
        with open(self.path, 'w') as f:
            json.dump(self.q, f)
        return self

    def choose_action(self, state_string):
        '''
        Returns the action to perform.

        This is the main method that interacts with the game interface:
        given a state string, it should return the action to be taken
        by the agent.

        The initial implementation of this method is simply a random
        choice among the possible actions. You will need to augment
        the code to implement Q-learning within the agent.
        '''
        alpha, gamma, epsilon = 0.3, 0.6, 0.1
        action = None
        state = Q_State(state_string)

        if state.key not in self.q:
            self.q[state.key] = {
                'u': 10,
                'd': -5,
                'l': 0,
                'r': 0,
                '_': -1
            }

        if random.random() < epsilon:
            action = random.choice(State.ACTIONS)
        else:
            action = max(self.q[state.key], key=self.q[state.key].get)

        # check if we need to update the q table
        # only occurs if agent didnt just spawn
        if self.previous_state and not self.previous_state.is_done:
            old_val = self.q[self.previous_state.key][self.previous_action]
            curr_max = max(self.q[state.key].values())
            new_val = (1 - alpha) * old_val + alpha * (state.reward() + gamma * curr_max)
            self.q[self.previous_state.key][self.previous_action] = new_val

        self.previous_state = state
        self.previous_action = action
        self.save()

        return action

from rgb import State
from agent import Agent, Node
import util

DEFAULT_STATE = 'rgrb|grbr|b gr|gbbr'

def heuristic(node: Node) -> int:
    def neighbors(state: State, row: int, col: int) -> int:
        neighbors = 0
        if state.get(col, row) == state.get(col + 1, row) or state.get(col, row) == state.get(col - 1, row) or \
            state.get(col, row) == state.get(col, row + 1) or state.get(col, row) == state.get(col, row - 1):
            neighbors += 1
        return neighbors
    rows = len(node.state.board)
    cols = len(node.state.board[0])
    count = 0

    for r in range(rows):
        for c in range(cols):
            count += neighbors(node.state, r, c)
    return node.depth() + count

if __name__ == '__main__':
    cmd = util.get_arg(1)
    if cmd:
        state: State = State(util.get_arg(2))
        agent: Agent = Agent()
        if cmd == 'print':
            util.pprint(state)
        elif cmd == 'goal':
            print(state.is_goal())
        elif cmd == 'actions':
            for action in state.actions():
                print(action)
        elif cmd == 'random':
            util.pprint(agent.random_walk(state, 8))
        elif cmd == 'bfs':
            agent.bfs(state)
        elif cmd == 'dfs':
            agent.dfs(state)
        elif cmd == 'a_star':
            agent.a_star(state, heuristic)
        else:
            print('Invalid Input. Try again.')

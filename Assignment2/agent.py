from random import randrange
from util import pprint

DEFAULT_STATE: str = 'rgrb|grbr|b gr|gbbr'

class Node:
    def __init__(self, state, parent = None, value = None):
        self.state = state
        self.parent = parent
        self.value = value
    
    def path(self) -> list:
        state_list: list = []
        node = self
        while node is not None:
            state_list.append(node.state)
            node = node.parent
        return state_list[::-1]

    def depth(self) -> int:
        node = self
        depth = 0
        while node is not None:
            depth += 1
            node = node.parent
        return depth

    def __repr__(self):
        return str(self.state)

class Agent:
    def random_walk(self, state, n: int):
        count = 0
        parent_node, node = None, None
        current_state = state
        if n <= 0:
            print('Please provide a positive number.')
            exit(1)
        while count < n:
            node = Node(current_state, parent_node)
            actions = current_state.actions()
            action = actions[randrange(len(actions))]
            parent_node = node
            current_state = current_state.clone().execute(action)
            count += 1
        return node.path()
    
    def bfs(self, state) -> Node:
        def bfs_search(node: Node) -> int:
            return node.depth()
        return self._search(state, bfs_search)

    def dfs(self, state) -> Node:
        def dfs_search(node: Node) -> int:
            return -1 * node.depth()
        return self._search(state, dfs_search)

    def a_star(self, state, heuristic) -> Node:
        return self._search(state, heuristic)

    def _search(self, state, func) -> Node:
        def descendants(current: Node, node_list):
            node_list = node_list or []
            for node in node_list:
                if node.parent == current:
                    node_list.append(node)
                    descendants(node, node_list)
            return node_list
        
        def sort(node_list):
            for i in range(len(node_list)):
                min_index = i
                for j in range(i + 1, len(node_list)):
                    if node_list[min_index].value > node_list[j].value:
                        min_index = j
                node_list[i], node_list[min_index] = node_list[min_index], node_list[i]
            return node_list


        OPEN: list[Node] = [Node(state, None)]
        CLOSED: list[Node] = []
        paths = 0

        while len(OPEN) != 0:
            current = OPEN.pop(0)
            CLOSED.append(current)
            current.value = func(current)
            pprint(current.path())

            if current.state.is_goal():
                print(paths)
                return current
            
            for action in current.state.actions():
                new = Node(current.state.clone().execute(action), current)
                in_open = True in [node.state == new.state for node in OPEN]
                in_closed = True in [node.state == new.state for node in CLOSED]

                if not in_open and not in_closed:
                    new.parent = current
                    new.value = func(new)
                    OPEN.insert(0, new)
                elif in_open:
                    if new.parent.depth() > current.depth():
                        new.parent = current
                    new.value = func(new)
                elif in_closed:
                    if new.parent.depth() > current.depth():
                        new.parent = current
                    new.value = func(new)
                    for d in descendants(new, CLOSED):
                        d.value = func(d)
                OPEN = sort(OPEN)
            paths += 1

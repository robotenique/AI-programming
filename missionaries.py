import numpy as np
from collections import deque

class Node(object):
    actions = [[1, 0, 1], [2, 0, 1], [0, 1, 1], [0, 2, 1], [1, 1, 1]]
    goal = []
    g_nodes = set()
    def __init__(self, value, signal=-1, parent=None):
        self.parent = parent
        self.signal = signal
        self.value = value
        if parent == None:
            Node.g_nodes.add(str(self))

    def successors(self):
        for act in Node.actions:
            new_value = Node(self.value + self.signal*np.array(act), signal=-1*self.signal, parent=self)
            #print(new_value)
            if act[0] + act[1] >= 1 and act[0] + act[1] <= 2 and new_value.is_valid() and str(new_value) not in Node.g_nodes:
                Node.g_nodes.add(str(new_value))
                yield new_value

    def is_valid(self):
        if (self.value[0] < 0 or self.value[1] < 0 or self.value[0] > 3 or
            self.value[1] > 3 or (self.value[2] != 0 and self.value[2] != 1)):
            return False
        if self.value[1] > self.value[0] and self.value[0] > 0:
            return False
        if self.value[1] < self.value[0] and self.value[0] < 3:
            return False
        return True

    def __str__(self):
        return f"<{self.value[0], self.value[1], self.value[2]}>"

    def __repr__(self):
        return f"<{self.value[0], self.value[1], self.value[2]}>"

    def is_goal(self):
        return (self.value == Node.goal).all()

    def set_goal(goal):
        Node.goal = goal

def retrieve_path(node):
    path = deque()
    path.appendleft(node)
    while node.parent != None:
        path.appendleft(node.parent)
        node = node.parent
    return path

def main():
    state = np.zeros(3, dtype=int)
    state[0] = 3 # Missionaries
    state[1] = 3 # Cannibals
    state[2] = 1 # Boat
    Node.set_goal(np.array([0, 0, 0], dtype=int))
    root = Node(state)

    # BFS
    queue = deque()
    queue.append(root)
    final_path = []
    while queue:
        curr = queue.popleft()
        if curr.is_goal():
            final_path = retrieve_path(curr)
            break
        for succ in curr.successors():
            queue.append(succ)
    if final_path:
        print("Solution found: ")
        for i, node in enumerate(final_path):
            print(f"  {node}\n")

if __name__ == '__main__':
    main()

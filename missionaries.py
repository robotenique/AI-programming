import numpy as np

def succ(x):
    state = x[0]
    s = x[1]
    actions = [[1, 0, 1], [2, 0, 1], [0, 1, 1], [0, 2, 1], [1, 1, 1]]
    next_states = []
    for act in actions:
        sc = np.copy(state)
        act = np.array(act)
        sc += s*act
        if not(sc[0] > 0 and sc[1] > sc[0]):
            if not(sc[0] > 3 or sc[1] > 3 or sc[2] > 1):
                next_states.append((sc, -1*s))
    return next_states

def bfs(start, goal):
    queue = []
    queue.append(start)
    while queue:
        path = queue.pop(0)
        node = path
        if (node[1] == goal).all():
            return path
        print("===============================================\n\n")
        for adj in succ(node):
            print("\t\t")
            print(adj)
            new_path = list(path)
            new_path.append(adj)
            queue.append(new_path)



def main():
    state = np.zeros(3, dtype=int)
    state[0] = 3 # Missionarie
    state[1] = 3 # Cannibals
    state[2] = 1 # Boat
    step = -1 # subtract or add
    init_state = (state, step)
    goal = np.array([0, 0, 0], dtype=int)
    t0 = succ(init_state)
    print(bfs(init_state, goal))




if __name__ == '__main__':
    main()

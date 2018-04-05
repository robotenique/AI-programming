import util
graph = {'A' : ['B', 'C'],
         'B' : ['F', 'G'],
         'C' : ['G'],
         'G' : [],
         'F' : []}

def dfs(graph, start='A'):
    st = util.Stack()
    st.push(start)
    pathTo = {start : []}
    found = False
    goalNode = 'G'
    while not st.isEmpty():
        curr = st.pop()
        if curr == goalNode:
            break
        for succ in graph[curr]:
            pathTo[succ] = curr
            st.push(succ)

    path = [goalNode]
    while goalNode:
        if pathTo[goalNode]:
            path.append(pathTo[goalNode])
        goalNode = pathTo[goalNode]
    print(path[::-1])

dfs(graph)

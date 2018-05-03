# Juliano Garcia de Oliveira NUSP 9277086
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import math
import random
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()



def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    marked = set()
    st = util.Stack()
    root = problem.getStartState()
    st.push(root) # (x, y)
    pathTo = {root : []}
    actionTo = {root : []}
    goal_state = None
    while not st.isEmpty():
        curr = st.pop()
        if curr not in marked:
            marked.add(curr)
        if problem.isGoalState(curr):
            goal_state = curr
            break
        for succ, action, cost in problem.getSuccessors(curr):
            if succ not in marked:
                pathTo[succ] = curr
                actionTo[succ] = action
                st.push(succ)
    if goal_state == None:
        raise AssertionError("No valid path found!!")

    path = [goal_state]
    action_path = []
    while goal_state != root:
        if pathTo[goal_state]:
            path.append(pathTo[goal_state])
            action_path.append(actionTo[goal_state])
        goal_state = pathTo[goal_state]

    return action_path[::-1]

def breadthFirstSearch(problem):
    marked = set()
    q = util.Queue()
    root = problem.getStartState()
    q.push(root) # (x, y)
    pathTo = {root : []}
    actionTo = {root : []}
    goal_state = None
    marked.add(root)
    while not q.isEmpty():
        curr = q.pop()
        if problem.isGoalState(curr):
            goal_state = curr
            break
        for succ, action, cost in problem.getSuccessors(curr):
            if succ not in marked:
                marked.add(succ)
                pathTo[succ] = curr
                actionTo[succ] = action
                q.push(succ)

    if goal_state == None:
        raise AssertionError("No valid path found!!")

    path = [goal_state]
    action_path = []
    while goal_state != root:
        if pathTo[goal_state]:
            path.append(pathTo[goal_state])
            action_path.append(actionTo[goal_state])
        goal_state = pathTo[goal_state]

    return action_path[::-1]

def iterativeDeepeningSearch(problem):
    depth = 0
    found = False

    while not found:
        st = util.Stack()
        root = problem.getStartState()
        st.push((root, 0)) # (x, y)
        marked = set()
        bestCostTo = {root: 0}
        pathTo = {root : []}
        actionTo = {root : []}
        goal_state = None
        while not st.isEmpty() and not found:
            curr, curr_d = st.pop()
            if curr not in marked:
                marked.add(curr)
            if problem.isGoalState(curr):
                goal_state = curr
                found = True
            if curr_d + 1 <= depth:
                for succ, action, cost in problem.getSuccessors(curr):
                    bcost = bestCostTo.get(succ, None)
                    if succ not in marked and not bcost or (bcost and  bestCostTo[curr] + cost < bcost):
                            pathTo[succ] = curr
                            actionTo[succ] = action
                            bestCostTo[succ] = bestCostTo[curr] + cost
                            st.push((succ, curr_d + 1))
                    elif bcost and bestCostTo[curr] + cost < bcost:
                        pathTo[succ] = curr
                        actionTo[succ] = action
                        bestCostTo[succ] = bestCostTo[curr] + cost
                        st.push((succ, curr_d + 1))
                #print "stack = ", st.list
        depth+=1

    if goal_state == None:
        raise AssertionError("No valid path found!!")

    path = [goal_state]
    action_path = []
    while goal_state != root:
        if pathTo[goal_state]:
            path.append(pathTo[goal_state])
            action_path.append(actionTo[goal_state])
        goal_state = pathTo[goal_state]

    return action_path[::-1]


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    pq = util.PriorityQueue()
    root = problem.getStartState()
    bestCostTo = {root: 0}
    pathTo = {root : []}
    actionTo = {root : []}
    pq.push(root, bestCostTo[root] + heuristic(root, problem=problem))
    goal_state = None    
    while not pq.isEmpty():
        curr = pq.pop()
        if problem.isGoalState(curr):
            goal_state = curr
            break
        for succ, action, cost in problem.getSuccessors(curr):
            new_cost = bestCostTo[curr] + cost
            if bestCostTo.get(succ, None) == None or new_cost < bestCostTo[succ]:            
                pathTo[succ] = curr
                actionTo[succ] = action
                bestCostTo[succ] = new_cost
                pq.update(succ, new_cost + heuristic(succ, problem=problem))
            

    if goal_state == None:
        raise AssertionError("No valid path found!!")

    path = [goal_state]
    action_path = []
    while goal_state != root:
        if pathTo[goal_state]:
            path.append(pathTo[goal_state])
            action_path.append(actionTo[goal_state])
        goal_state = pathTo[goal_state]

    return action_path[::-1]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch

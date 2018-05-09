# multiAgents.py
# --------------
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


from util import manhattanDistance
import random, util, math
from game import Agent, Actions, Directions, Configuration

from pacman import * # TODO: REMOVE

import random as r
class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)

        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = bestIndices[0] # Pick randomly among the best
        "Add more of your code here if you want to"
        # print(legalMoves)
        # print(scores)
        # print("Choosen: ", legalMoves[chosenIndex])
        return legalMoves[chosenIndex]



    def evaluationFunction(self, currentGameState, action):
        #TODO: Refatorar..

        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        currPos = currentGameState.getPacmanPosition()
        newPos = successorGameState.getPacmanPosition()
        gpos_s = successorGameState.getGhostPositions()
        best_dist_food = food_dijkstra(successorGameState, newPos)
        score_food = 1.0/best_dist_food
        score = score_food
        newGhostStates = successorGameState.getGhostStates()
        # print(newPos)
        # print("\n\n")
        capsules = successorGameState.getCapsules()
        neighbors_pos = [[newPos[0], newPos[1]], [currPos[0], currPos[1]]]
        get_neigh = lambda x, y: [[x, y - 1], [x, y + 1], [x + 1, y], [x - 1, y]]
        # for pos in [[x, y - 1], [x, y + 1], [x + 1, y], [x - 1, y]]:
        #     x_p, y_p = pos
        #     if x_p > 0 and x_p < currentGameState.getWalls().width and y_p > 0 and y_p < currentGameState.getWalls().height:
        #         if not currentGameState.getWalls()[x_p][y_p]:
        #             neighbors_pos.append(pos)
        ghosts = gpos_s + currentGameState.getGhostPositions()
        ng = []
        full_ghosts = ghosts + ng
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        min_d = float("inf")
        min_ghost = None
        for i, gp in enumerate(ghosts):
            new = manhattanDistance(newPos, gp)
            if new < min_d:
                min_d = new
                min_ghost = i
        # print("---------")
        # print("Distancia retornada:", best_dist_food)
        # print(neighbors_pos)
        # print(ghosts)
        # print("---------")
        for pos in neighbors_pos:
            for gp in full_ghosts:
                x_g, y_g = gp
                x_g = int(x_g)
                y_g = int(y_g)
                x, y = pos
                if x_g == x and y_g == y:
                    return -float("inf")

        if action == Directions.STOP:
            return -float("inf")

        if currentGameState.getFood()[newPos[0]][newPos[1]]:
            score += 5
            if min_ghost < len(gpos_s):
                neighbors_ghost = Actions.getLegalNeighbors(gpos_s[min_ghost], successorGameState.getWalls())
                if any(n_g == newPos for n_g in neighbors_ghost):
                    return -float("inf")
        for cap in capsules:
            x_c, y_c = cap
            if x_c == currPos[0] and y_c == currPos[1]:
                score += 100
        if min_ghost < len(newScaredTimes) and newScaredTimes[min_ghost] > min_d:
            score += 10/min_d
        else:
            score -= 1.0/min_d
        return score

def food_dijkstra(game_state, start):
    graph = game_state.getWalls()
    food = game_state.getFood()
    dist_to = []
    path_to = []
    is_out = {}
    found_food = False
    best_dist = float("inf")
    for _ in range(graph.width):
        dist_to.append([float("inf") for _ in range(graph.height)])
        path_to.append([None for _ in range(graph.height)])
    dist_to[start[0]][start[1]] = 0
    pq = util.PriorityQueue()
    for x in range(graph.width):
        for y in range(graph.height):
            if not graph[x][y]:
                pq.update((x, y), dist_to[x][y])
    while not pq.isEmpty():
        curr = pq.pop()
        is_out[curr] = True
        if food[curr[0]][curr[1]]:
            best_dist = dist_to[curr[0]][curr[1]]
            break
        neighbors = Actions.getLegalNeighbors(curr, graph)
        for v in neighbors:
            if not is_out.get(v, False):
                alt = dist_to[curr[0]][curr[1]] + 1
                if alt < dist_to[v[0]][v[1]]:
                    dist_to[v[0]][v[1]] = alt
                    path_to[v[0]][v[1]] = curr
                    pq.update(v, alt)

    return best_dist

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        next_depth = 0
        next_agent = 1
        bval = -float("inf")
        baction = None
        t = gameState.getLegalActions(0)
        if "Stop" in t:
            t.remove("Stop")

        for a in t:
            next_state = gameState.generateSuccessor(0, a)
            result = self.minimax(next_state, next_depth, next_agent)
            if result > bval:
                bval = result
                baction = a
        return baction

    def minimax(self, gameState, depth, agent_index):
        MAX = agent_index == 0
        MIN = agent_index > 0
        actions = gameState.getLegalActions(agent_index)
        if "Stop" in actions:
            actions.remove("Stop")

        if depth == self.depth or actions == []:
            return self.evaluationFunction(gameState)
        if MAX:
            bval = -float("inf")
            for a in actions:
                next_state = gameState.generateSuccessor(agent_index, a)
                bval = max(bval, self.minimax(next_state, depth, agent_index + 1))
            return bval

        if MIN:
            bval = float("inf")
            next_agent = (agent_index + 1)%gameState.getNumAgents()
            for a in actions:
                next_state = gameState.generateSuccessor(agent_index, a)
                next_depth = depth + 1 if next_agent == 0 else depth
                bval = min(bval, self.minimax(next_state, next_depth, next_agent))
            return bval


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -float("inf")
        beta = float("inf")
        next_depth = 0
        next_agent = 1
        bval = -float("inf")
        baction = None
        t = gameState.getLegalActions(0)
        if "Stop" in t:
            t.remove("Stop")
        for a in t:
            next_state = gameState.generateSuccessor(0, a)
            result = self.minimax_alpha_beta(next_state, next_depth, next_agent, alpha, beta)
            if result > bval:
                bval = result
                baction = a
            if bval > beta:
                return baction
            alpha = max(alpha, bval)
        return baction

    def minimax_alpha_beta(self, gameState, depth, agent_index, alpha, beta):
        MAX = agent_index == 0
        MIN = agent_index > 0
        actions = gameState.getLegalActions(agent_index)
        if "Stop" in actions:
            actions.remove("Stop")
        if depth == self.depth or actions == []:
            return self.evaluationFunction(gameState)
        if MAX:
            bval = -float("inf")
            for a in actions:
                next_state = gameState.generateSuccessor(agent_index, a)
                bval = max(bval, self.minimax_alpha_beta(next_state, depth, agent_index + 1, alpha, beta))
                if bval > beta:
                    return bval
                alpha = max(alpha, bval)
            return bval

        if MIN:
            bval = float("inf")
            next_agent = (agent_index + 1)%gameState.getNumAgents()
            for a in actions:
                next_state = gameState.generateSuccessor(agent_index, a)
                next_depth = depth + 1 if next_agent == 0 else depth
                bval = min(bval, self.minimax_alpha_beta(next_state, next_depth, next_agent, alpha, beta))
                if bval < alpha:
                    return bval
                beta = min(beta, bval)
            return bval


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # print("\n=======================")
        # print("CHAMANDO better() para estado atual.")
        # better(gameState)
        # for a in gameState.getLegalActions(0):
        #     print("CHAMANDO better() para estado proximo fazendo", a)
        #     better(gameState.generateSuccessor(0, a))
        # print("=======================\n")
        # __import__("time").sleep(1)
        next_depth = 0
        next_agent = 1
        results = [] # List of vals
        actions = [] # List of actions to achieve that vals
        for a in gameState.getLegalActions(0):
            next_state = gameState.generateSuccessor(0, a)
            result = self.expectiminimax(next_state, next_depth, next_agent)
            results.append(result)
            actions.append(a)

        best_action = [actions[i] for i in range(len(actions)) if results[i] == max(results)]

        if len(best_action) > 1 and "Stop" in best_action:
            best_action.remove("Stop")

        return best_action[0]


    def expectiminimax(self, gameState, depth, agent_index):
        #__import__("time").sleep(0.7)

        MAX = agent_index == 0
        CHANCE = agent_index > 0
        # if MAX:
            # print("CHAMADA MINIMAX (MAX): ", depth, agent_index)
        # elif CHANCE:
            # print("CHAMADA MINIMAX (CHANCE): ", depth, agent_index)
        actions = gameState.getLegalActions(agent_index)
        if depth == self.depth or actions == []:
            # print("node folha, retorna: ", self.evaluationFunction(gameState))
            return self.evaluationFunction(gameState)
        if MAX:
            bval = -float("inf")
            for a in actions:
                next_state = gameState.generateSuccessor(agent_index, a)
                bval = max(bval, self.expectiminimax(next_state, depth, agent_index + 1))
            # print("Retornando (max): ", bval)
            return bval

        if CHANCE:
            if len(actions) > 0:
                prob = 1.0/len(actions)
                acc = 0
            else:
                # print("Retornando (CHANCE) infinito, pois nao tem acao pra fazer...")
                return float("inf")

            next_agent = (agent_index + 1)%gameState.getNumAgents()
            for a in actions:
                next_state = gameState.generateSuccessor(agent_index, a)
                next_depth = depth + 1 if next_agent == 0 else depth
                acc = acc + prob*self.expectiminimax(next_state, next_depth, next_agent)
            # print("Tirei a media, retornando (CHANCE): ", acc)
            return acc


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    cgs = currentGameState
    # cgs = GameState()
    if cgs.isWin():
        return float("inf")
    elif cgs.isLose():
        return -float("inf")

    pacpos = cgs.getPacmanPosition()
    score = cgs.getScore()
    capsules = cgs.getCapsules()
    foods = cgs.getFood()
    ghosts = cgs.getGhostPositions()
    if foods.asList() != []:
        dist2_closest_food = min(map(lambda f: manhattanDistance(pacpos, f), foods.asList()))
    else:
        # If the state has no food left, it doesn't matter for future states
        dist2_closest_food =  0


    num_foods = len(foods.asList())
    num_capsules = len(capsules)
    # Ghosts
    scared_times = [g_state.scaredTimer for g_state in cgs.getGhostStates()]
    ghost_matrix = [[g, sc_t] for g, sc_t in zip(ghosts, scared_times)]
    dist_ghost = lambda e: manhattanDistance(pacpos, e[0])
    awoke_g = []
    scared_g = []
    for g in ghost_matrix:
        if g[1] == 0:
            awoke_g.append(g)
        else:
            scared_g.append(g)


    if list(awoke_g):
        dist2_closest_awokeGhost = dist_ghost(min(awoke_g, key = dist_ghost))
    else:
        dist2_closest_awokeGhost = float("inf")
    if list(scared_g):
        dist2_closest_scaredGhost = dist_ghost(min(scared_g, key = dist_ghost))
    else: # If there isn't a scared ghost, this doesn't impact in the evaluation (the capsules will)
        dist2_closest_scaredGhost = 0
    # print("returns: ", score, dist2_closest_food, num_capsules, 1.0/dist2_closest_awokeGhost, dist2_closest_scaredGhost, num_capsules, num_foods, (score + -2*dist2_closest_food + -15*num_capsules +
    #         -1.7*(1.0/dist2_closest_awokeGhost) +
    #         -2*dist2_closest_scaredGhost +
    #         -17*num_capsules +
    #         -5*num_foods
    #         ))
    type_1 = (score +
            -2*dist2_closest_food +
            -1.7*(1.0/dist2_closest_awokeGhost) +
            -5*dist2_closest_scaredGhost +
            -20*num_capsules +
            -5*num_foods
            )
    type_2 = (score -2*dist2_closest_food)
    type_3 = (4*score-2*dist2_closest_food)
    #print("returns:", dist2_closest_food, type_3)
    return type_1
# Abbreviation
better = betterEvaluationFunction

import numpy as np
import numpy.ma as ma
from math import inf

def get_indexes(v, val):
    """
    Returns the indexes of the v array which have the value 'val':
    Cases:
        if v = column of a matrix:
            returns the rows which have the value 'val'
        if v = row of a matrix:
            returns the columns which have the value 'val'
    """
    max_mask = ma.getmask(ma.masked_not_equal(v, val))
    return list(ma.array(np.arange(len(v)), mask=max_mask).compressed())

class ZSGame(object):
    """
    Represents a simple zero-sum game.
    The normal_form is a matrix with the payments (only player 1 payments),
    as the game is a zero-sum game, the payment of the other player at [i][j]
    -(normal_form[i][j]) (they both sum to zero).
    """
    def __init__(self, normal_form):
        self.n_form = np.array(normal_form)

    def get_state(self):
        return self.n_form

    def print_state(self):
        print("")
        for i in range(len(self.n_form)):
            print(f"{[str(x).zfill(2) for x in self.n_form[i]]}")

    def get_eq(self):
        equilibrium = []
        max_c = {}
        min_r = {}
        for cnum, col in enumerate(self.n_form.T):
            max_val = np.max(col)
            max_c[cnum] = [max_val, get_indexes(col, max_val)]
        for rnum, row in enumerate(self.n_form):
            min_val = np.min(row)
            if any(min_val == j for j in map(lambda v: v[0], max_c.values())):
                min_r[rnum] = [min_val, get_indexes(row, min_val)]
        for row, val in min_r.items():
            for col in val[1]:
                if row in max_c[col][1]:
                    equilibrium.append((row, col))

        return equilibrium

class ProbabilisticGame(ZSGame):
    def __init__(self, normal_form, player1, player2):
        super().__init__(normal_form)
        self.player1 = player1
        self.player2 = player2

    def expectation(self, player=1):
        "Return the expected payment (for 'player') given a fixed player choice"
        expect = self.player1.strategy@self.n_form@self.player2.strategy
        expect = expect if player == 1 else -expect
        return expect[0][0]

    def get_best_strategy(self, player=1):
        """Return the best strategy and the payment for 'player', for a fixed
           strategy for the opponent, and varying all the strategies for
           the 'player'.
        """
        best_strat = []
        best_payment = -inf if player == 1 else +inf
        pl = self.player1 if player == 1 else self.player2
        optimize = max if player == 1 else min
        for strat in pl.get_all_strategy():
            pl.strategy = strat
            new_expectation = self.expectation(player)
            if optimize(new_expectation, best_payment) != best_payment:
                best_strat = strat
                best_payment = optimize(new_expectation, best_payment)
        return best_payment, best_strat



class Player(object):
    def __init__(self, p_set, pos):
        self.pos = pos
        self.n_moves = len(p_set[0])
        for p_dist in p_set:
            assert sum(p_dist) == 1
            assert all(p <= 1 and p >= 0 for p in p_dist)
        # Column or row vector, depending on what player
        if pos == 'r':
            self.p_set = [np.array(p_dist).reshape(1, len(p_dist)) for p_dist in p_set]
        elif pos == 'c':
            self.p_set = [np.array(p_dist).reshape(len(p_dist), 1) for p_dist in p_set]
        self.strategy = self.p_set[0]
        print("New player sucessfully created!")

    def get_all_strategy(self):
        "Returns all strategies of the player"
        return self.p_set


def main():
    # The test_board matrix represents the payments from the player A (row)
    # test_board = [[ 0,  0, -71],
    #               [-1, -1,  -1],
    #               [ 1,  0,  0]]
    # my_game = ZSGame(test_board)
    test_board = [[ 0,  0, -71],
                  [-1, -1,  -1],
                  [ 1,  0,  0]]
    luiza_strategies = [[0.2, 0.3, 0.5], [0.4, 0.4, 0.2], [0.1, 0.8, 0.1]]
    carlos_strategies = [[0.7, 0.15, 0.15]]
    luiza = Player(luiza_strategies, 'r')
    carlos = Player(carlos_strategies, 'c')
    prob_game = ProbabilisticGame(test_board, luiza, carlos)
    print("----------------PAGAMENTO ESPERADO : 'luiza' ------------------")
    print(prob_game.expectation())
    print("----------------MELHOR ESTRATÉGIA (fixo primeira estratégia de carlos) : 'luiza' ------------------")
    print(prob_game.get_best_strategy())



if __name__ == '__main__':
    main()

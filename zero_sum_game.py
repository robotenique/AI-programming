import numpy as np
import numpy.ma as ma

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





def main():
    # The test_board matrix represents the payments from the player A (row)
    test_board = [[ 0,  0, -71],
                  [-1, -1,  -1],
                  [ 1,  0,  0]]
    my_game = ZSGame(test_board)

    my_game.print_state()
    eq = my_game.get_eq()
    print("----------------EQUILÍBRIO------------------")
    print(eq)


if __name__ == '__main__':
    main()

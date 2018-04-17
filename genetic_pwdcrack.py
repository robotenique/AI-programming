import random as rnd

def word_generate(length):
    """
    Generate a string with random lowercase letters, with length = length!
    """
    # Generate a random letter from alphabet, lowercase, and add to result
    return "".join((chr(97 + rnd.randint(0, 26)) for _ in range(length)))

def initial_pop(size, password):
    """
    Generate a population consisting of random words, each with the same
    length as the password, and the population has the size specified.
    """
    return [word_generate(len(password)) for _ in range(size)]




def fitness (password, test_word):
    """
    The fitness function:
        fitness(test_word): (# of correct chars) / (total number of chars)


        fitness(test_word) = 0 if # of correct chars = 0
        fitness(test_word) = 100 if # of correct chars = total number of chars
    """
    if (len(test_word) != len(password)):
        print("Incompatible password...")
        return
    else:
        score = 0
        i = 0
        while(i < len(password)):
            if (password[i] == test_word[i]):
                score += 1
            i += 1

        return score*100/len(password)

def main():
    pass

if __name__ == '__main__':
    main()

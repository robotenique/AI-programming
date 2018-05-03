"""
Crack a password using a genetic algorithm!
"""
import random as rnd

def main():
    """
    This file implements a genetic algorithm to solve the problem of
    cracking a given password, by creating 'generations' of different
    words, selecting the best, breeeding them, applying a simple crossover
    (randomized) and a mutation chance.
    """
    #variables dict: Define the problem constants
    genetic_variables = {
        'password' : "verylongwordpass",
        'size_population' : 100,
        'best_sample' : 20,
        'lucky_few' : 20,
        'number_of_child' : 5,
        'number_of_generations' : 10000, #Overkill >:D
        'chance_of_mutation' : .5
    }
    prob = genetic_variables
    #program
    if (prob['best_sample'] + prob['lucky_few'])/2*prob['number_of_child'] != prob['size_population']:
        print ("population size not stable")
        return

    last_gen, _ = genetic_algorithm(**genetic_variables)
    print("Last generation: \n\n")
    print(last_gen)

def genetic_algorithm(**kwargs):
    """
    Execute the genetic algorithm.
    This algorithm takes a dict as an argument.
    It will iterate based on the variable 'number_of_generations', and return
    the last_gen and the historic
    """
    # Unpack the values from the dict
    password = kwargs['password']
    size_population = kwargs['size_population']
    best_sample = kwargs['best_sample']
    lucky_few = kwargs['lucky_few']
    number_of_child = kwargs['number_of_child']
    number_of_generations = kwargs['number_of_generations']
    chance_of_mutation = kwargs['chance_of_mutation']
    hist = []
    # The genetic algorithm
    curr_pop = initial_pop(size_population, password)
    hist = curr_pop
    last_found = -1
    for _ in range (number_of_generations):
        curr_pop = next_gen(curr_pop, password, best_sample, lucky_few, number_of_child, chance_of_mutation)
        hist.append(curr_pop)
        if check_solution(curr_pop, password):
            last_found = _
            break
    if last_found != -1:
        print(f"Found a solution in the {last_found} generation!!")
    else:
        print("No solution found! D':")


    return curr_pop, hist

def next_gen(curr_pop, password, best_sample, lucky_few, number_of_child, chance_of_mutation):
    """
    -> This is the main task of the Genetic Algorithm <-

    Given the current population, apply the following steps:
        - Compute the fitness of each individual in the population
        - Select the best ones (and some lucky guys)
        - Make them reproduce
        - Mutate the children
        - Return this new population
    """
    pop_sorted = compute_perf_pop(curr_pop, password)
    next_breeders = select_from_population(pop_sorted, best_sample, lucky_few)
    next_pop = create_children(next_breeders, number_of_child)
    next_gen = mutate_pop(next_pop, chance_of_mutation)
    return next_gen

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
        score = (1 if password[i] == test_word[i] else 0 for i in range(len(password)))
        return sum(score)*100/len(password)

def compute_perf_pop(population, password):
    """
        Return the population, sorted by the fitness from each individual
    """
    populationPerf = {ind:fitness(password, ind) for ind in population}
    # Sort by fitness, reversed (best ones in the beginning of the list)
    return sorted(populationPerf.items(), key= lambda it: it[1], reverse=True)

def select_from_population(pop_sorted, best_sample, lucky_few):
    """
    Create the next breeders, with 'best_sample' individuals which have the
    top fitness value from the population, and 'lucky_few' individuals which
    are randomly selected.
    """
    next_gen = []

    for i in range(best_sample):
        next_gen.append(pop_sorted[i][0])
    # Simple lucky few: randomly select some elements from the population
    for i in range(lucky_few):
        next_gen.append(rnd.choice(pop_sorted)[0])

    rnd.shuffle(next_gen)

    return next_gen

def create_children(breeders, nof_childs):
    """
    Create the next population of individuals, by breeding two by two
    """
    next_pop = []
    mid_pos = len(breeders)//2 # len(breeders) must be an even number
    for ind_1, ind_2 in zip(breeders[:mid_pos], breeders[mid_pos:]):
        for _ in range(nof_childs):
            next_pop.append(create_child(ind_1, ind_2))
    return next_pop

def mutate_pop(population, chance):
    """
    Given a chance for mutation, this apply the mutation layer
    to the genetic algorithm, by generating a mutation with the chance
    specified.
    """
    for i in range(len(population)):
        if rnd.random() < chance:
            population[i] = mutate_word(population[i])
    return population

def mutate_word(word):
    """
    Mutate a letter(gene) from the word, then return it
    """
    pos = int(rnd.random()*len(word))
    word = word[:pos] + chr(97 + int(26*rnd.random())) + word[pos + 1:]
    return word

def create_child(ind_1, ind_2):
    """
    For each letter of the child, get a random gene from ind_1 or ind_2
    in the i-th position.
    """
    temp = [ind_1[i] if rnd.random() < 0.5 else ind_2[i] for i in range(len(ind_1))]
    return "".join(temp)

def word_generate(length):
    """
    Generate a string with random lowercase letters, with length = length!
    """
    # Generate a random letter from alphabet, lowercase, and add to result
    return "".join((chr(97 + rnd.randint(0, 26)) for _ in range(length)))

def check_solution(population, password):
    """
    Check if the population found a solution to the problem
    """
    return any(ind == password for ind in population)

if __name__ == '__main__':
    main()

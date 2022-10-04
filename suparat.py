#rat breeding sim
#%%
import time
import random
import statistics
#%%

"""Rewrite the super_rats.py code to accommodate a variable number of male and female individuals. 
Then rerun the program with the same total number of rats as before, but use 4 males and 16 females. 
How does this impact the number of years required to reach the target weight of 50,000 grams?"""

#constants (grams)
goal = 50000

num_rats = 20
num_male = int((1/5) * num_rats)
num_female = num_rats - num_male

init_min_wt = 200
init_max_wt = 600
init_mode_wt = 300

mutate_odds = 0.05
mutate_min = 0.5
mutate_max = 1.2

litter_size = 8
litters_per_year = 10
generation_limit = 500

# ensure even number of rats for breeding pairs:
# if num_rats %2 != 0:
#     num_rats += 1

def populate(num_rats, min_wt, max_wt, mode_wt):
    ''' Initialize a population with a triangular distribution of weights'''
    return [int(random.triangular(min_wt, max_wt, mode_wt))\
            for i in range(num_rats)]

def fitness(population,goal):
    '''Measure population fitness based on an attribute mean vs target'''
    avg = statistics.mean(population)
    return avg / goal

def select(population, to_retain):
    '''Cull a population to retain only a specified number of members'''
    sorted_population = sorted(population)
    to_retain_by_sex = to_retain//2
    # members_per_sex = len(sorted_population)//2
    # females = sorted_population[:members_per_sex]
    # males = sorted_population[members_per_sex:]
    selected_females = females[-to_retain_by_sex:]
    selected_males = males[-to_retain_by_sex:]
    return selected_males, selected_females

def breed(males, females, litter_size):
    '''Crossover genes among members (weights) of a population'''
    random.shuffle(males)
    random.shuffle(females)
    children = []
    for male, female in zip(males,females):
        for child in range(litter_size):
            child = random.randint(female, male)
            children.append(child)
    return children

def mutate(children, mutate_odds, mutate_min, mutate_max):
    '''Randomly alter rat weights using input odds & fractional changes'''
    for index, rat in enumerate(children):
        if mutate_odds >= random.random():
            children[index] = round(rat * random.uniform(mutate_min,mutate_max))
    return children

def main():
    '''Initialize population; select, breed, and mutate; display results'''
    generations = 0
    parents = populate(num_rats, init_min_wt, init_max_wt, init_mode_wt)
    print("initial population weights = {}".format(parents))
    pop_fitness = fitness(parents, goal)
    print("initial population fitness = {}".format(pop_fitness))
    print("number to retain = {}".format(num_rats))

    avg_wt = []

    while pop_fitness < 1 and generations < generation_limit:
        selected_males, selected_females = select(parents,num_rats)
        children = breed(selected_males, selected_females, litter_size)
        children = mutate(children, mutate_odds, mutate_min, mutate_max)
        parents = selected_males + selected_females + children
        pop_fitness = fitness(parents, goal)
        print("Generation {} fitness = {:.4f}".format(generations, pop_fitness))
        
        avg_wt.append(int(statistics.mean(parents)))
        generations += 1
    
    print("average weight per generation = {}".format(avg_wt))
    print("\nnumber of generations = {}".format(generations))
    print("number of years = {}".format(int(generations / litters_per_year)))

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    print("\nRuntime for this program was {} seconds.".format(duration))
# %%

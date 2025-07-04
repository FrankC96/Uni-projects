# Genetic Algotihms

---
### Hyperparameters
1. probability of crossover
2. probability of mutation
3. the size of the population
4. the number of iterations

### Components
1. A fitness function
    
    The fitness function is the function the algorithm is trying to optimize (minimize).
    It defines how **fit** each chromosome is.
2. A chromosome
    
    A chromosome is a numerical value or a data structure with numerical values that represents a candidate solution.
    It would be really helpfull to describe a chromosome with bits (1s and 0s).
3. A selection process
    
    Each chromosome in the population
is evaluated by the fitness function to test how well it solves the problem at hand.
The fitter a chromosome is, the more likely it
is to be selected.
4. A crossover process

    The crossover process is trying to combine fitting chromosomes together.
5. A mutation process

    The mutation operator randomly flips individual bits in the new
chromosomes (turning a 0 into a 1 and vice versa). Typically mutation happens with a very
low probability, such as 0.001. The mutation process is crucial to escape local minima, the selection and crossover processes are carrying information only from the current fitting information.

### A final note for the fitness function
It is important
to consider which partial solutions should be favored over other partial solutions because
that will determine the direction in which the whole population moves


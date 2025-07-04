import random
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Callable


from optimizer import f, Simulator


class GeneticAlgorithm:
    def __init__(self, model: Simulator, x0: List[float], cross_prob: float, mutate_prob: float, pop_size: int, max_iter: int):
        """
        A general genetic algorithm with chromosomes representing PID controller gains.
        Each chromosome is a list of length 3 representing Kp, Ki, Kd gains of the controller.
        Parameters
        ----------
        model:              The function to be optimized(minimized)
        cross_prob:     Crossover probability
        mutate_prob:    Mutation probability
        pop_size:       Population size
        max_iter:       Maximum number of iterations
        """
        self.model: Simulator = model
        self.x0: List[float] = x0
        self.cross_prob: float = cross_prob
        self.mutate_prob: float = mutate_prob
        self.pop_size: int = pop_size
        self.max_iter: int = max_iter

        self.pop = [[random.uniform(-100, 100) for _ in range(3)] for _ in range(pop_size)]

    def fitness(self, x: List[float], y_idx: int = 0, ref: float = 1.0) -> float:
        # TODO: scale the fitness function in a specific range
        # TODO: y_idx and ref, and put them as class attributes
        
        x, u, e = sys.evolve(pid_gains=x, x0=self.x0, y_idx=y_idx, ref=ref)
        return e

    def crossover(self, pars: List[List[float]]):
        for pop_idx in range(len(self.pop)):
            random_prop = random.random()
            random_gain_choice = random.randint(0, 2)
            if random_prop < self.cross_prob:
                self.pop[pop_idx][random_gain_choice] = random.choice(pars)[0][random_gain_choice]

    def mutate(self, pars: List[List[float]]):
        for pop_idx in range(len(self.pop)):
            random_prop = random.random()
            random_gain_choice = random.randint(0, 2)
            if random_prop < self.mutate_prob:
                self.pop[pop_idx][random_gain_choice] += random.choice(pars)[0][random_gain_choice] * 0.6  # Again, constant for now

    def run(self)-> List[List[float]]:
        fitnesses = []
        cons_fit = 0

        k = 0
        while cons_fit < 15:
            chromosomes_fitness: List[List[float]] = [[pop, self.fitness(pop)] for pop in self.pop]
            chromosomes_fitness.sort(key=lambda x: x[1])

            parents = chromosomes_fitness[:4]  # Number of parents is constant for now
            self.crossover(parents)
            self.mutate(parents)

            if k > int(0.4 * self.max_iter) and parents[0][1] > 10:
                # This is a safeguard, escape local minima by re-initializing
                self.pop = [[random.uniform(-100, 100) for _ in range(3)] for _ in range(self.pop_size)]

            fitnesses.append(parents[0][1])

            if np.isclose(fitnesses[k], fitnesses[k-1], atol=1e-3):
                print(f'Reaching stagnation {cons_fit}/15')
                cons_fit += 1

            print(f"Epoch {k} with best fitness {fitnesses[-1]}")
            k += 1

        return parents, fitnesses

if __name__ == "__main__":
    """
    I need to find a way to model the chattering of the input signal
    so I can penalize it in my fitness function.
    """
    X0 = [0.0, 0.1]

    sys = Simulator(model=f, nx=2, nu=1, nsim=30, dt=0.1)
    opt = GeneticAlgorithm(sys, X0, cross_prob=0.4, mutate_prob=0.1, pop_size=100, max_iter=1000)

    res, fit = opt.run()

    plt.figure()
    plt.grid()

    x, u, e = sys.evolve(pid_gains=res[0][0], x0=[0.0, 0.5], y_idx=0, ref=10)

    plt.plot(x)
    plt.plot(u, '--')
    plt.suptitle("State / Input trajectories")
    plt.figure()
    plt.plot(fit)
    plt.suptitle("Fitness over epochs")
    plt.grid()
    plt.show()
from __future__ import annotations
import math
import random
import typing as t

T = t.TypeVar("T")


class Chromosome:
    """
    Represents a single chromosome in the genetic algorithm, holding a list of genes and a fitness value.

    Attributes:
        genes (List[T]): The genes that make up the chromosome.
        fitness (float): The fitness score of the chromosome.
    """

    def __init__(self, genes: t.List[T]) -> None:
        """
        Initialize a Chromosome with a list of genes.

        Args:
            genes (List[T]): The genes for this chromosome.
        """
        self.fitness = 1e-5
        self.genes = genes

    def crossover(self, other: Chromosome) -> Chromosome:
        """
        Perform crossover with another chromosome to produce a child chromosome.

        Args:
            other (Chromosome): The other parent chromosome.

        Returns:
            Chromosome: The resulting child chromosome after crossover.
        """
        mid_point = random.randint(0, len(self.genes) - 1)
        return Chromosome(self.genes[:mid_point] + other.genes[mid_point:])

    def mutate(
        self,
        mutation_rate: float,
        mutation_fn: t.Optional[t.Callable[[T], T]] = None,
    ) -> None:
        """
        Mutate the chromosome's genes with a given mutation rate and mutation function.

        Args:
            mutation_rate (float): Probability of each gene being mutated.
            mutation_fn (Optional[Callable[[T], T]]): Function to mutate a gene. If None, a random gene is chosen.
        """
        if mutation_fn is None:
            mutation_fn = lambda _: random.choice(self.genes)
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[i] = mutation_fn(self.genes[i])


class Population:
    """
    Represents a population of chromosomes and manages the evolution process.

    Attributes:
        chromosomes (List[Chromosome]): The list of chromosomes in the population.
        global_best (Chromosome): The best chromosome found so far.
        local_best (Chromosome): The best chromosome in the current generation.
        mutation_rate (float): The mutation rate for the population.
        mutation_fn (Optional[Callable[[T], T]]): The mutation function for genes.
    """

    def __init__(
        self,
        chromosomes: t.List[Chromosome],
        mutation_rate: float = 0.01,
        mutation_fn: t.Optional[t.Callable[[T], T]] = None,
    ) -> None:
        """
        Initialize a Population with a list of chromosomes and optional mutation settings.

        Args:
            chromosomes (List[Chromosome]): The initial chromosomes.
            mutation_rate (float, optional): The mutation rate. Defaults to 0.01.
            mutation_fn (Optional[Callable[[T], T]], optional): The mutation function. Defaults to None.
        """
        self.chromosomes = chromosomes
        self.global_best = random.choice(chromosomes)
        self.local_best = random.choice(chromosomes)
        self.mutation_rate = mutation_rate
        self.mutation_fn = mutation_fn

    def step(self) -> None:
        """
        Perform one generation step: selection, crossover, mutation, and replacement.
        """
        mating_pool = [
            c
            for c in self.chromosomes
            for _ in range(math.floor((100 * c.fitness) / self.global_best.fitness))
        ]
        for i in range(len(self.chromosomes)):
            parent1 = random.choice(mating_pool)
            parent2 = random.choice(mating_pool)
            child = parent1.crossover(parent2)
            child.mutate(self.mutation_rate, self.mutation_fn)
            self.chromosomes[i] = child

    def eval(self, fitness_fn: t.Callable[[Chromosome], float]) -> None:
        """
        Evaluate the fitness of all chromosomes and update the best chromosomes.

        Args:
            fitness_fn (Callable[[Chromosome], float]): Function to compute fitness for a chromosome.
        """
        for c in self.chromosomes:
            c.fitness = fitness_fn(c)
        self.local_best = max(
            self.chromosomes,
            key=lambda c: c.fitness,
        )
        self.global_best = max(
            self.global_best,
            self.local_best,
            key=lambda c: c.fitness,
        )

    def run(
        self,
        iterations: int,
        fitness_fn: t.Callable[[Chromosome], float],
    ) -> t.Generator[t.Tuple[int, Chromosome, Chromosome], None, None]:
        """
        Run the genetic algorithm for a number of iterations.

        Args:
            iterations (int): Number of generations to run.
            fitness_fn (Callable[[Chromosome], float]): Function to compute fitness for a chromosome.

        Yields:
            Tuple[int, Chromosome, Chromosome]: The generation index, local best, and global best chromosomes for each iteration.
        """
        for i in range(iterations):
            self.step()
            self.eval(fitness_fn)
            yield (i, self.local_best, self.global_best)

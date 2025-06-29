import string
import random
import argparse
import typing as t
from ..base import Population, Chromosome


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Evolve a string to match a target using a genetic algorithm.",
    )
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        default="To be or not to be!",
        help="Target string that the genetic algorithm will try to evolve towards.",
    )
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=1000,
        help="Number of generations (iterations) to run the genetic algorithm.",
    )
    parser.add_argument(
        "-p",
        "--population-size",
        type=int,
        default=200,
        help="Number of individuals in the population.",
    )
    parser.add_argument(
        "-m",
        "--mutation-rate",
        type=float,
        default=0.02,
        help="Probability of mutation for each gene (character) in a chromosome.",
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility.",
    )
    return parser.parse_args()


def main(args):

    def random_char(*a) -> str:
        return random.choice(string.printable)

    def random_string() -> t.List[str]:
        return [random_char() for _ in range(len(args.target))]

    def fitness_fn(chromosome: Chromosome) -> float:
        return sum(1 for i, c in enumerate(chromosome.genes) if c == args.target[i])

    random.seed(args.seed)
    population = Population(
        chromosomes=[Chromosome(random_string()) for _ in range(args.population_size)],
        mutation_rate=args.mutation_rate,
        mutation_fn=random_char,
    )
    for i, local_best, global_best in population.run(args.iterations, fitness_fn):
        best_string = "".join(global_best.genes)
        best_fitness = global_best.fitness
        print(f"Iteration {i:4d}: {best_string!r} (fit: {best_fitness:.2f})")
        if best_string == args.target:
            print(f"Target was generated in {i} iterations.")
            break


if __name__ == "__main__":
    args = parse_args()
    main(args)

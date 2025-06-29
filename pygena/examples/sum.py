import string
import random
import argparse
import typing as t
from ..base import Population, Chromosome


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Evolve a list of numbers to sum to a target using a genetic algorithm.",
    )
    parser.add_argument(
        "-t",
        "--target",
        type=int,
        default=100,
        help="Target sum that the genetic algorithm will try to evolve towards.",
    )
    parser.add_argument(
        "-r",
        "--range",
        type=float,
        nargs=2,
        default=(-100, 100),
        help="Range (min max) of possible values for each gene (number) in a chromosome.",
    )
    parser.add_argument(
        "-c",
        "--chromosome-size",
        type=int,
        default=10,
        help="Number of genes (numbers) in each chromosome.",
    )
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=100,
        help="Number of generations (iterations) to run the genetic algorithm.",
    )
    parser.add_argument(
        "-p",
        "--population-size",
        type=int,
        default=10,
        help="Number of individuals in the population.",
    )
    parser.add_argument(
        "-m",
        "--mutation-rate",
        type=float,
        default=0.05,
        help="Probability of mutation for each gene (number) in a chromosome.",
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

    def random_int(*a) -> str:
        return random.randint(*args.range)

    def random_list() -> t.List[str]:
        return [random_int() for _ in range(args.chromosome_size)]

    def fitness_fn(chromosome: Chromosome) -> float:
        diff = abs(sum(chromosome.genes) - args.target)
        return 1 / (diff + 1e-5)

    random.seed(args.seed)
    population = Population(
        chromosomes=[Chromosome(random_list()) for _ in range(args.population_size)],
        mutation_rate=args.mutation_rate,
        mutation_fn=random_int,
    )
    for i, local_best, global_best in population.run(args.iterations, fitness_fn):
        best_numbers = global_best.genes
        best_sum = sum(best_numbers)
        print(f"Iteration {i:4d}: {best_numbers} (sum: {best_sum:.2f})")
        if sum(best_numbers) == args.target:
            print(f"Target was generated in {i} iterations.")
            print(f"Numbers: {global_best.genes}")
            break


if __name__ == "__main__":
    args = parse_args()
    main(args)

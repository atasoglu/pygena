import random
import argparse
import typing as t
from ..base import Chromosome, Population


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Solve the knapsack problem using a genetic algorithm.",
    )
    parser.add_argument(
        "-n",
        "--num-items",
        type=int,
        default=20,
        help="Number of items in the knapsack.",
    )
    parser.add_argument(
        "-w",
        "--weights",
        type=int,
        default=20,
        help="Maximum weight of an item.",
    )
    parser.add_argument(
        "-v",
        "--values",
        type=int,
        default=10,
        help="Maximum value of an item.",
    )
    parser.add_argument(
        "-c",
        "--capacity",
        type=int,
        default=50,
        help="Capacity of the knapsack.",
    )
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=1000,
        help="Number of iterations to run the genetic algorithm.",
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

    def random_int(gene=None) -> int:
        return random.randint(0, 1)

    def random_list() -> t.List[int]:
        return [random_int() for _ in range(args.num_items)]

    def calc_total_weight(chromosome: Chromosome) -> float:
        return sum(chromosome.genes[i] * weights[i] for i in range(args.num_items))

    def calc_total_value(chromosome: Chromosome) -> float:
        return sum(chromosome.genes[i] * values[i] for i in range(args.num_items))

    def fitness_fn(chromosome: Chromosome) -> float:
        total_weight = calc_total_weight(chromosome)

        if total_weight > args.capacity:
            penalty = total_weight - args.capacity
            return -penalty

        return calc_total_value(chromosome)

    random.seed(args.seed)
    weights = [random.randint(1, args.weights) for _ in range(args.num_items)]
    values = [random.randint(1, args.values) for _ in range(args.num_items)]
    population = Population(
        chromosomes=[Chromosome(random_list()) for _ in range(args.population_size)],
        mutation_rate=args.mutation_rate,
        mutation_fn=random_int,
    )
    for i, local_best, global_best in population.run(args.iterations, fitness_fn):
        total_weight = calc_total_weight(global_best)
        total_value = calc_total_value(global_best)
        print(f"Iteration {i:4d}: Weight={total_weight} Value={total_value}")


if __name__ == "__main__":
    args = parse_args()
    main(args)

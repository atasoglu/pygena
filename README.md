# pygena

A simple, flexible genetic algorithm library for Python. Easily define your own chromosomes, fitness functions, and evolutionary strategies to solve optimization and search problems.

## Features
- Minimal, intuitive API
- Customizable chromosomes and fitness functions
- Population management and evolution

## Installation
```bash
pip install pygena
```
Or clone and install from source:
```bash
git clone https://github.com/atasoglu/pygena.git
cd pygena
pip install .
```

## Usage
Here's a minimal example of evolving a list of numbers to sum to a target:
```python
from pygena import Chromosome, Population
import random

target = 100
chromosome_size = 10
population_size = 10
mutation_rate = 0.05
iterations = 100

def random_int(gene=None):
    return random.randint(-100, 100)

def random_list():
    return [random_int() for _ in range(chromosome_size)]

def fitness_fn(chromosome):
    diff = abs(sum(chromosome.genes) - target)
    return 1 / (diff + 1e-5)

random.seed(42)
population = Population(
    chromosomes=[Chromosome(random_list()) for _ in range(population_size)],
    mutation_rate=mutation_rate,
    mutation_fn=random_int,
)
for i, local_best, global_best in population.run(iterations, fitness_fn):
    print(f"Iteration {i}: {global_best.genes} (sum: {sum(global_best.genes)})")
    if sum(global_best.genes) == target:
        print(f"Target reached in {i} iterations.")
        break
```

For more examples, see the [`examples/`](pygena/examples/) directory.

You can simply run an example script: `python3 -m pygena.examples.text`. Run with the `--help` flag to see the full list of arguments.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to help improve pygena.

## License
MIT License. See [LICENSE](LICENSE).
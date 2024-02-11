import random

@profile
def main():
    orders = [random.randint(0, 100) for _ in range(100_000)]
    comperehension = [2 * amount for amount in orders if amount > 50]
    generator = (2 * amount for amount in orders if amount > 50)

    sum(comperehension)
    sum(generator)

main()

# kernprof -lv caching.py
# python3 -m memory_profiler generators.py

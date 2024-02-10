import time

#@profile
def heavy_work():
    for _ in range(1_000_000):
        do_stuff()

#@profile
def do_stuff():
    return 1+2 


if __name__ == '__main__':
    start = time.time()
    heavy_work()
    end = time.time()
    print(f'Execution time: {end - start: .2f} seconds')




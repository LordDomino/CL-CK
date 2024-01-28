import time
from clck.formulang.common import Formulang

i = 1
iters = 100
start = time.time()

while i < iters:
    res = Formulang.generate("a")
    i += 1

stop = time.time()

print(f"{iters} iterations: {stop - start} seconds")
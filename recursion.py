from timeit import default_timer as timer
from numba import njit

class Memoize:
    def __init__(self, func):
        self.func = func
        self.dct = {}

    def __call__(self, *args):
        if args not in self.dct:
            self.dct[args] = self.func(*args)
        return self.dct[args]

@njit
def poly(x, order):
    if order == 0:
        return 1
    else:
        return x * poly(x,order-1)
# wow, slower! I guess that lookup does cost something
@Memoize
def mempoly(x, order):
    if order == 0:
        return 1
    else:
        return x * mempoly(x,order-1)
@njit
def polyNoRecur(x, order):
    return x ** order

def make_poly(order, poly_generator):
    def p(x):
        return poly_generator(x, order)
    return p

def timeTestPoly(func, order, xLocs):
    f = make_poly(order, func)
    yLocs = list(range(len(xLocs)))
    count = 0
    start = timer()
    for x in xLocs:
        yLocs[count] = f(x)
        count += 1
    stop = timer()
    print("Time for ", count, " evaluations: ", stop - start, " seconds.")




def main():
    orders = list([i*i for i in range(1,10)])
    xLocs = [0.01* i for i in range(100)]
    for order in orders:
        print("Order ", order, ":")
        print("No recursion: ")
        timeTestPoly(polyNoRecur, order, xLocs)
        print("Non-memoized recursion: ")
        timeTestPoly(poly, order, xLocs)
        print("Memoized recursion: ")
        timeTestPoly(mempoly, order, xLocs)

if __name__ == "__main__":
    main()

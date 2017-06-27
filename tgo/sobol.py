""" sobol.cc translated to Python 3 by Carl Sandrock 2016-03-31

The original program is available and described at
http://web.maths.unsw.edu.au/~fkuo/sobol/

"""

import argparse
import numpy
import sys

parser = argparse.ArgumentParser(
    "Prints the first N sobol points in D dimensions. "
    "The points are generated in graycode order. "
    "The primitive polynomials and initial direction numbers are given by the input file.")
parser.add_argument("N", type=int, help="Number of points")
parser.add_argument("D", type=int, help="Dimensions")
parser.add_argument("file", type=argparse.FileType('r'))
parser.add_argument("-o", "--outfile", type=argparse.FileType('w'),
                    default=sys.stdout)

args = parser.parse_args()

unsigned = "uint64"

def sobol_points(N, D, f):
    # swallow header
    buffer = next(f)

    L = int(numpy.log(N)//numpy.log(2.0)) + 1

    C = numpy.ones(N, dtype=unsigned)
    for i in range(1, N):
        value = i
        while value & 1:
            value >>= 1
            C[i] += 1

    POINTS = numpy.zeros((N, D), dtype='double')

    # XXX: This appears not to set the first element of V
    V = numpy.empty(L+1, dtype=unsigned)
    for i in range(1, L+1):
        V[i] = 1 << (32 - i)

    X = numpy.empty(N, dtype=unsigned)
    X[0] = 0
    for i in range(1, N):
        X[i] = X[i-1] ^ V[C[i-1]]
        POINTS[i, 0] = X[i]/2**32

    for j in range(1, D):
        F_int = [int(item) for item in next(f).strip().split()]
        (d, s, a), m = F_int[:3], [0] + F_int[3:]

        if L <= s:
            for i in range(1, L+1): V[i] = m[i] << (32 - i)
        else:
            for i in range(1, s+1): V[i] = m[i] << (32 - i)
            for i in range(s+1, L+1):
                V[i] = V[i-s] ^ (V[i-s] >> numpy.array(s, dtype=unsigned))
                for k in range(1, s):
                    V[i] ^= numpy.array((((a >> (s-1-k)) & 1) * V[i-k]), dtype=unsigned)

        X[0] = 0
        for i in range(1, N):
            X[i] = X[i-1] ^ V[C[i-1]]
            POINTS[i, j] = X[i]/2**32  # *** the actual points

    return POINTS

P = sobol_points(args.N, args.D, args.file)

for row in P:
    args.outfile.write(" ".join(["{}"]*len(row)).format(*row) + "\n")

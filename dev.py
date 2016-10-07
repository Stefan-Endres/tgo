from tgo._tgo import *
import numpy

def f(x):
    #if (x > 5.001) and (x < 5.01):
    if (x > 5.01) and (x < 5.05):
        return 100*(x - 5.02)**2
    return numpy.nan#100.0#numpy.nan

X = numpy.linspace(0, 10, 10000)
F = []
for x in X:
    F.append(f(x))

if False:
    from matplotlib import pyplot as plot
    plot.figure()
    plot.plot(X, F)
    plot.show()

#options =
print(tgo(f, [(0, 10)], n=10, options={'disp':True, 'maxiter':300}))
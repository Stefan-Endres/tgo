.. image:: https://travis-ci.org/Stefan-Endres/tgo.svg?branch=master
    :target: https://travis-ci.org/Stefan-Endres/tgo
.. image:: https://coveralls.io/repos/github/Stefan-Endres/tgo/badge.png?branch=master
    :target: https://coveralls.io/github/Stefan-Endres/tgo?branch=master


Description
-----------

Finds the global minimum of a function using topographical global
optimisation (tgo_). Appropriate for solving general purpose NLP and blackbox
optimisation problems to global optimality (low dimensional problems).
The general form of an optimisation problem is given by:

.. _tgo: https://stefan-endres.github.io/tgo/

::

    minimize f(x) subject to

    g_i(x) >= 0,  i = 1,...,m
    h_j(x)  = 0,  j = 1,...,p

where x is a vector of one or more variables. ``f(x)`` is the objective
function ``R^n -> R``, ``g_i(x)`` are the inequality constraints.
``h_j(x)`` are the equality constrains.


Installation
------------
Stable:

.. code::

    $ pip install tgo
    
Latest:

.. code::

    $ git clone https://bitbucket.org/upiamcompthermo/tgo
    $ cd tgo
    $ python setup.py install
    $ python setup.py test

Documentation
-------------
The docstrings and project website https://stefan-endres.github.io/tgo/ contains more detailed examples, notes and performance profiles.

Quick example
-------------

Consider the problem of minimizing the Rosenbrock function. This function is implemented in ``rosen`` in ``scipy.optimize``

.. code:: python

    >>> from scipy.optimize import rosen
    >>> from tgo import tgo
    >>> bounds = [(0,2), (0, 2), (0, 2), (0, 2), (0, 2)]
    >>> result = shgo(rosen, bounds)
    >>> result.x, result.fun
    (array([ 1.,  1.,  1.,  1.,  1.]), 2.9203923741900809e-18)

Note that bounds determine the dimensionality of the objective function and is therefore a required input, however you can specify empty bounds using ``None`` or objects like numpy.inf which will be converted to large float numbers.


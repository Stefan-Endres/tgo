<script type="text/x-mathjax-config"> MathJax.Hub.Config({ TeX: { equationNumbers: { autoNumber: "all" } } }); </script>
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [ ['$','$'], ["\\(","\\)"] ],
      displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
      processEscapes: false
    }
  });
</script>
<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

[![Build Status](https://travis-ci.org/Stefan-Endres/shgo.svg?branch=master)](https://travis-ci.org/Stefan-Endres/shgo)
[![Coverage Status](https://s3.amazonaws.com/assets.coveralls.io/badges/coveralls_99.svg)](https://coveralls.io/github/Stefan-Endres/shgo?branch=master)
<sup>*Corresponding author for shgo: [Stefan Endres](https://stefan-endres.github.io/)*<sup>

### Table of Contents
1. **[Introduction](#introduction)**<br>
1. **[Performance summary](#performance-summary)**<br>
    + **[Open-source black-box algorithms](#open-source-black-box-algorithms)**<br>
    + **[Recently published black-box algorithms](#recently-published-black-box-algorithms)**<br>
1. **[Installation](#installation)**<br>
1. **[Examples](#examples)**<br>
    + **[Rosenbrock *unimodal function*](#rosenbrock-unimodal-function)**<br>
        + [Bounded variables](#bounded-variables)
        + [Unbounded variables](#unbounded-variables)
    + **[Eggholder *multimodal function*](#eggholder-multimodal-function)**<br>
        + [Mapping local minima](#mapping-local-minima)
        + [Improving results](#improving-results)
    + **[Cattle feed problem (HS73) with *non-linear constraints*](#cattle-feed-hs73-problem-with-non-linear-constraints)**<br>
1. **[Parameters](#parameters)**<br>
1. **[Returns](#returns)**<br>
1. **[References](#references)**<br>

Introduction
------------

Global optimisation using topographical global optimisation [1]. Appropriate for solving general purpose NLP and blackbox optimisation problems to global optimality (low dimensional problems).

In general, the optimisation problems are of the form::

\begin{eqnarray} \nonumber
  \min_x && f(x),  x \in \mathbb{R}^n \\\\\\ \nonumber
   \text{s.t.} && g_i(x) \ge 0, ~ \forall i = 1,...,m \\\\\\ \nonumber
   && h_j(x) = 0,  ~\forall j = 1,...,p
\end{eqnarray}

where $x$ is a vector of one or more variables.
$f(x)$ is the objective function $f: \mathbb{R}^n \rightarrow \mathbb{R}$

$g_i(x)$ are the inequality constraints $\mathbb{g}: \mathbb{R}^n \rightarrow \mathbb{R}^m$

$h_j(x)$ are the equality constraints $\mathbb{h}: \mathbb{R}^n \rightarrow \mathbb{R}^p$

Optionally, the lower and upper bounds $x_l \le x \le x_u$ for each element in $x$ can also be specified using the `bounds` argument.

ITGO is a clustering method that uses graph theory to generate good starting points for local search methods from points distributed uniformly in the interior of the feasible set.

The local search method may be specified using the ``minimizer_kwargs`` parameter which is inputted to ``scipy.optimize.minimize``. By default the ``SLSQP`` method is used. Other local minimisation methods more suited to the problem can also be used. In general it is recommended to use the ``SLSQP`` or ``COBYLA`` local minimization if inequality constraints are defined for the problem since the other methods do not use constraints.

The `sobol` method points are generated using the Sobol [2] sequence. The primitive polynomials and various sets of initial direction numbers for generating Sobol sequences is provided by [3] by Frances Kuo and Stephen Joe. The original program sobol.cc (MIT) is available and described at http://web.maths.unsw.edu.au/~fkuo/sobol/ translated to Python 3 by Carl Sandrock 2016-03-31.

The algorithm is generally applicable to low dimensional black problems ([~10-dimensional problems](https://www.youtube.com/watch?v=fhNuspYbMeI)) unless more information can be supplied to the algorithm. This is not necessarily only gradients and hessians. For example if it is known that the decision variables of the objective function are symmetric, then the ``symmetry`` option can be used in order to solve problems with hundreds of variables.


Performance summary
-----------------
#### Open-source black-box algorithms

The tgo algorithm only makes use of function evaluations without requiring the derivatives of objective functions. This makes it applicable to black-box global optimisation problems. Here we compare the TGO and SHGO algorithms with the SciPy implementations Jones et al. (2001–) of basinhopping (BH) [4-5] and differential evolution (DE) orignally proposed Storn and Price [6]. These algorithms were chosen because the open source versions are readily available in the SciPy project. The test suite contains multi-modal problems with box constraints, they are described in detail in [infinity77.net/global_optimization/](https:infinity77.net/global_optimization/index.html). We used the stopping criteria pe = 0.01% for shgo and tgo. Any local function evaluations were added to the global count. For the stochastic algorithms (BH and DE) the starting points provided by the test suite were used. For every test the algorithm was terminated if the global minimum was not found after 10 minutes of processing time and the test was flagged as a fail.

This figure shows the performance profiles for SHGO, TGO, DE and BH on the SciPy benchmarking test suite using function evaluations and processing run time as performance criteria:

![./image/Fig12.svg](./image/Fig12.svg)

Performance profiles zoomed in to the range of f.e. = [0, 1000] function evaluations and [0, 0.4] seconds run time:

![./image/Fig12.svg](./image/Fig13.svg)

From the figures it can be observed that for this problem set shgo-sobol was the best performing algorithm, followed closely by tgo and shgo-simpl. The zoomed figure provides a clearer comparison between these three algorithms. While the performance of all 3 algorithms are comparable, shgo-Sobol tends to outperform shgo, solving more problems or a given number of function evaluations. This is expected since, for the same sampling point sequence, tgo produced more than one starting point in the same locally convex domain while shgo is guaranteed to only produce one after adequate sampling. While shgo-simpl has the advantage of having the theoretical guarantee of convergence, the sampling sequence has not been optimised yet requiring more function evaluations with every iteration than shgo-sobol.

#### Recently published black-box algorithms

A recent review and experimental comparison of 22 derivative-free optimisation algorithms by Rios and Sahinidis [7] concluded that global optimisation solvers solvers such as TOMLAB/MULTI-MIN, TOMLAB/GLCCLUSTER, MCS and TOMLAB/LGO perform better, on average, than other derivative-free solvers in terms of solution quality within 2500 function evaluations. Both the TOMLAB/GLC-CLUSTER and MCS Huyer and Neumaier (1999) implementations are based on the well-known DIRECT (DIviding RECTangle) algorithm [8].

The DISIMPL (DIviding SIMPLices) algorithm was recently proposed by Paulavičius and Žilinskas [9]. The experimental investigation in [9] shows that the proposed simplicial algorithm gives very competitive results compared to the DIRECT algorithm. DISIMPL has been extended in [10-11]. The Gb-DISIMPL (Globally-biased DISIMPL) was compared in Paulavičius et al. (2014) [10] to the DIRECT and DIRECT-l methods in extensive numerical experiments on 800 multidimensional multiextremal. Gb-DISIMPL was shown to provide highly competative results compared the other algorithms.

More recently the Lc-DISIMPL variant of the algorithm was developed to handle optimisation problems with linear constraints [12]. Below we use an extract of the results with the highest performing Lc-DISIMPL algorithm (Lc-DISIMPL-v) and  DIRECT-L1 with the best performaning parameters (pp = 10). The full table can be found at [here](files/table.pdf). From the table it can be seen shgo provides competative results compared to the other algorithms:


| Algorithm: | shgo-simpl| shgo-sob | Lc-DISIMPL-v  | PSwarm (avg) | DIRECT-L1 |
|------------|---:|-----:|------:|-------------:|----------:|
| horst-1   |  97 |   24 | 7    | 182            |  287$^a$    |
| horst-2   |  10 |   11 | 5    | 176            |  265$^a$    |
| horst-3   |  6  |    7 | 5    | 43             |  5$^a$      |
| horst-4   |  10 |   25 | 8    | 179            |  58293$^a$  |
| horst-5   | 20  | 15   | 8    | 150            |  7$^a$      |
| horst-6   | 22  | 59   | 10   | 172            |  11$^a$     |
| horst-7   | 10  | 15   | 10   | 201            |  7$^a$      |
| hs021     | 24  | 23   | 189  | 110            | 97          |
| hs024     | 24  | 15   | 3    | 153            |  19$^a$     |
| hs035     | 37  | 41   | 630  | 311            |  >100000    |
| hs036     | 105 | 20   | 8    | 179            |  25$^a$     |
| hs037     | 72  | 63   | 186  | 131            |  7$^a$      |
| hs038     | 225 | 1029 | 3379 | 54445          | 7401        |
| hs044     | 199 | 35   | 20   |  218$^{b(9)}$  | 90283       |
| hs076     | 56  | 37   | 548  | 198            | 19135       |
| s224      | 166 | 165  | 49   | 107            |  7$^a$      |
| s231      | 99  | 99   | 2137 | 1011           | 1261        |
| s232      | 24  | 15   | 3    | 144            |  19$^a$     |
| s250      | 105 | 20   | 8    | 296            |  25$^a$     |
| s251      | 72  | 63   | 186  | 84             |  7$^a$      |
| bunnag1   | 34  | 47   | 630  | 142            | 1529        |
| bunnag2   | 46  | 36   | 16   | 153            |  >100000    |
|           |     |      |      |                |             |
| Average   | 66  | 88   | 366  | 2672           |  >17213     |


$a$ result is outside the feasible region

$b(t)$ $t$ out of 10 times the global solution was not reached 

Lc-DISIMPL-v, PSwarm (avg), DIRECT-L1 results produced by Paulavičius & Žilinskas (2016)



Installation
-----------------

Stable:
```
$ pip install tgo
```

Latest:
```
$ git clone https://github.com/Stefan-Endres/tgo
$ cd tgo
$ python setup.py install
$ python setup.py test
```


Examples
----------

First consider the problem of minimizing the Rosenbrock function. This
function is implemented in `rosen` in `scipy.optimize`

```python
    >>> from scipy.optimize import rosen
    >>> from tgo import tgo
    >>> bounds = [(0,2), (0, 2), (0, 2), (0, 2), (0, 2)]
    >>> result = tgo(rosen, bounds)
    >>> result.x, result.fun
    (array([ 1.,  1.,  1.,  1.,  1.]), 2.9203923741900809e-18)
```

Note that bounds determine the dimensionality of the objective
function and is therefore a required input, however you can specify
empty bounds using ``None`` or objects like numpy.inf which will be
converted to large float numbers.

```python
>>> bounds = [(None, None), (None, None), (None, None), (None, None)]
>>> result = tgo(rosen, bounds)
>>> result.x
array([ 0.99999851,  0.99999704,  0.99999411,  0.9999882 ])
```

Next we consider the Eggholder function, a problem with several local
minima and one global minimum.
(https://en.wikipedia.org/wiki/Test_functions_for_optimization)

```python
    >>> from tgo import tgo
    >>> import numpy as np
    >>> def eggholder(x):
    ...     return (-(x[1] + 47.0)
    ...             * np.sin(np.sqrt(abs(x[0]/2.0 + (x[1] + 47.0))))
    ...             - x[0] * np.sin(np.sqrt(abs(x[0] - (x[1] + 47.0))))
    ...             )
    ...
    >>> bounds = [(-512, 512), (-512, 512)]
    >>> result = tgo(eggholder, bounds)
    >>> result.x, result.fun
    (array([ 512.        ,  404.23180542]), -959.64066272085051)
```

``tgo`` also has a return for any other local minima that was found, these
 can be called using:

```python
>>> result.xl, result.funl
(array([[ 512.        ,  404.23180542],
       [-456.88574619, -382.6233161 ],
       [ 283.07593402, -487.12566542],
       [ 324.99187533,  216.0475439 ],
       [-105.87688985,  423.15324143],
       [-242.97923629,  274.38032063],
       [-414.8157022 ,   98.73012628],
       [ 150.2320956 ,  301.31377513],
       [  91.00922754, -391.28375925],
       [ 361.66626134, -106.96489228]]),
       array([-959.64066272, -786.52599408, -718.16745962, -582.30628005,
       -565.99778097, -559.78685655, -557.85777903, -493.9605115 ,
       -426.48799655, -419.31194957]))
```

Now suppose we want to find a larger amount of local minima, this can be
accomplished for example by increasing the amount of sampling points...

```python
    >>> result_2 = tgo(eggholder, bounds, n=1000)
    >>> len(result.xl), len(result_2.xl)
    (10, 60)
```

...or by lowering the k_t value:

```python
    >>> result_3 = tgo(eggholder, bounds, k_t=1)
    >>> len(result.xl), len(result_2.xl), len(result_3.xl)
    (10, 60, 48)
```

To demonstrate solving problems with non-linear constraints consider the
following example from [5] (Hock and Schittkowski problem 18):

Minimize: f = 0.01 * (x_1)**2 + (x_2)**2

Subject to: x_1 * x_2 - 25.0 >= 0,
            (x_1)**2 + (x_2)**2 - 25.0 >= 0,
            2 <= x_1 <= 50,
            0 <= x_2 <= 50.

Approx. Answer:
    f([(250)**0.5 , (2.5)**0.5]) = 5.0

>>> from scipy.optimize import tgo
>>> def f(x):
...     return 0.01 * (x[0])**2 + (x[1])**2
...
>>> def g1(x):
...     return x[0] * x[1] - 25.0
...
>>> def g2(x):
...     return x[0]**2 + x[1]**2 - 25.0
...
>>> g = (g1, g2)
>>> bounds = [(2, 50), (0, 50)]
>>> result = tgo(f, bounds, g_cons=g)
>>> result.x, result.fun
(array([ 15.81138847,   1.58113881]), 4.9999999999996252)

Parameters
----------
    func : callable

The objective function to be minimized.  Must be in the form
``f(x, *args)``, where ``x`` is the argument in the form of a 1-D array
and ``args`` is a tuple of any additional fixed parameters needed to
completely specify the function.

---

    bounds : sequence

Bounds for variables.  ``(min, max)`` pairs for each element in ``x``,
defining the lower and upper bounds for the optimizing argument of
`func`. It is required to have ``len(bounds) == len(x)``.
``len(bounds)`` is used to determine the number of parameters in ``x``.
Use ``None`` for one of min or max when there is no bound in that
direction. By default bounds are ``(None, None)``.

---

    args : tuple, optional

Any additional fixed parameters needed to completely specify the
objective function.

---

    constraints : dict or sequence of dict, optional

Constraints definition.
Function(s) $\mathbb{R}^n$ in the form:

$g(x) \le 0$ applied as $\mathbb{g}: \mathbb{R}^n \rightarrow \mathbb{R}^m$

$h(x) = 0$ applied as $\mathbb{g}: \mathbb{R}^n \rightarrow \mathbb{R}^p$

Each constraint is defined in a dictionary with fields:

    * type : str
        Constraint type: 'eq' for equality $h(x), 'ineq' for inequality $g(x).
    * fun : callable
        The function defining the constraint.
    * jac : callable, optional
        The Jacobian of `fun` (only for SLSQP).
    * args : sequence, optional
        Extra arguments to be passed to the function and Jacobian.

Equality constraint means that the constraint function result is to
be zero whereas inequality means that it is to be non-negative.
Note that COBYLA only supports inequality constraints.

NOTE:   Only the COBYLA and SLSQP local minimize methods currently
        support constraint arguments. If the ``constraints`` sequence
        used in the local optimization problem is not defined in
        ``minimizer_kwargs`` and a constrained method is used then the
        global ``constraints`` will be used.
        (Defining a ``constraints`` sequence in ``minimizer_kwargs``
        means that ``constraints`` will not be added so if equality
        constraints and so forth need to be added then the inequality
        functions in ``constraints`` need to be added to
        ``minimizer_kwargs`` too).

---

    n : int, optional

Number of sampling points used in the construction of the simplicial complex. Note that this argument is only used for ``sobol`` and other arbitrary sampling_methods.

---

    iters : int, optional

Number of iterations used in the construction of the simplicial complex.

---

    callback : callable, optional

Called after each iteration, as ``callback(xk)``, where ``xk`` is the
current parameter vector.

---

    minimizer_kwargs : dict, optional

Extra keyword arguments to be passed to the minimizer
``scipy.optimize.minimize`` Some important options could be:

    * method : str
        The minimization method (e.g. ``SLSQP``)
    * args : tuple
        Extra arguments passed to the objective function (``func``) and
        its derivatives (Jacobian, Hessian).
    * options : dict, optional
        Note that by default the tolerance is specified as ``{ftol: 1e-12}``

---

    options : dict, optional

A dictionary of solver options. Many of the options specified for the
global routine are also passed to the scipy.optimize.minimize routine.
The options that are also passed to the local routine are marked with an
(L)

Stopping criteria, the algorithm will terminate if any of the specified
criteria are met. However, the default algorithm does not require any to
be specified:

    * maxfev : int (L)
        Maximum number of function evaluations in the feasible domain.
        (Note only methods that support this option will terminate
        the routine at precisely exact specified value. Otherwise the
        criterion will only terminate during a global iteration)
    * f_min
        Specify the minimum objective function value, if it is known.
    * f_tol : float
        Precision goal for the value of f in the stopping
        criterion. Note that the global routine will also
        terminate if a sampling point in the global routine is
        within this tolerance.
    * maxiter : int
        Maximum number of iterations to perform.
    * maxev : int
        Maximum number of sampling evaluations to perform (includes
        searching in infeasible points).
    * maxtime : float
        Maximum processing runtime allowed
    * minhgrd : int
        Minimum  homology group rank differential. The homology group of the
        objective function is calculated (approximately) during every
        iteration. The rank of this group has a one-to-one correspondence
        with the number of locally convex subdomains in the objective
        function (after adequate sampling points each of these subdomains
        contain a unique global minima). If the difference in the hgr is 0
        between iterations for ``maxhgrd`` specified iterations the
        algorithm will terminate.

Objective function knowledge:

    * symmetry : bool
        Specify True if the objective function contains symmetric variables.
        The search space (and therefore performance) is decreased by O(n!).

    * jac : bool or callable, optional
        Jacobian (gradient) of objective function. Only for CG, BFGS,
        Newton-CG, L-BFGS-B, TNC, SLSQP, dogleg, trust-ncg. If jac is a
        Boolean and is True, fun is assumed to return the gradient along
        with the objective function. If False, the gradient will be
        estimated numerically. jac can also be a callable returning the
        gradient of the objective. In this case, it must accept the same
        arguments as fun. (Passed to `scipy.optimize.minmize` automatically)

    * hess, hessp : callable, optional
        Hessian (matrix of second-order derivatives) of objective function
        or Hessian of objective function times an arbitrary vector p.
        Only for Newton-CG, dogleg, trust-ncg. Only one of hessp or hess
        needs to be given. If hess is provided, then hessp will be ignored.
        If neither hess nor hessp is provided, then the Hessian product
        will be approximated using finite differences on jac. hessp must
        compute the Hessian times an arbitrary vector.
        (Passed to `scipy.optimize.minmize` automatically)

Algorithm settings:

    * minimize_every_iter : bool
        If True then promising global sampling points will be passed to a
        local minimisation routine every iteration. If False then only the
        final minimiser pool will be run. Defaults to False.
    * local_iter : int
        Only evaluate a few of the best minimiser pool candiates every
        iteration. If False all potential points are passed to the local
        minimsation routine.
    * infty_constraints: bool
        If True then any sampling points generated which are outside will
        the feasible domain will be saved and given an objective function
        value of numpy.inf. If False then these points will be discarded.
        Using this functionality could lead to higher performance with
        respect to function evaluations before the global minimum is found,
        specifying False will use less memory at the cost of a slight
        decrease in performance.

Feedback:

    * disp : bool (L)
        Set to True to print convergence messages.

---

    sampling_method : str or function, optional

Current built in sampling method options are ``sobol`` and ``simplicial``. The default ``simplicial`` uses less memory and provides the theoretical guarantee of convergence to the global minimum in finite time. The ``sobol`` method is faster in terms of sampling point generation at the cost of higher memory resources and the loss of guaranteed convergence. It is more appropriate for most "easier" problems where the convergence is relatively fast. User defined sampling functions must accept two arguments of ``n`` sampling points of dimension ``dim`` per call and output an array of s ampling points with shape `n x dim`. See SHGO.sampling_sobol for an example function.


Returns
-------
    res : OptimizeResult

The optimization result represented as a `OptimizeResult` object.
Important attributes are:
    ``x`` the solution array corresponding to the global minimum,
    ``fun`` the function output at the global solution,
    ``xl`` an ordered list of local minima solutions,
    ``funl`` the function output at the corresponding local solutions,
    ``success`` a Boolean flag indicating if the optimizer exited
    successfully,
    ``message`` which describes the cause of the termination,
    ``nfev`` the total number of objective function evaluations including
    the sampling calls,
    ``nlfev`` the total number of objective function evaluations
    culminating from all local search optimisations,

# Topograhphical Global Optimisation
Python implementation of the topograhphical global optimisation algorithm. Finds the global minima of a function using topograhphical global optimisation.

  Parameters
  ----------
  ```
  func : callable
      The objective function to be minimized.  Must be in the form
      ``f(x, *args)``, where ``x`` is the argument in the form of a 1-D array
      and ``args`` is a  tuple of any additional fixed parameters needed to
      completely specify the function.
  ```
  ```
  bounds : sequence
      Bounds for variables.  ``(min, max)`` pairs for each element in ``x``,
      defining the lower and upper bounds for the optimizing argument of
      `func`. It is required to have ``len(bounds) == len(x)``.
      ``len(bounds)`` is used to determine the number of parameters in ``x``.
      Use ``None`` for one of min or max when there is no bound in that
      direction. By default bounds are ``(None, None)``.
  ```
  ```
  args : tuple, optional
      Any additional fixed parameters needed to completely specify the
      objective function.
  ```
  ```
  g_cons : sequence of callable functions, optional
      Function(s) used to define a limited subset to defining the feasible
      set of solutions in R^n in the form g(x) <= 0 applied as g : R^n -> R^m

      NOTE: If the ``constraints`` sequence used in the local optimization
            problem is not defined in ``minimizer_kwargs`` and a constrained
            method is used then the ``g_cons`` will be used.
            (Defining a ``constraints`` sequence in ``minimizer_kwargs``
             means that ``g_cons`` will not be added so if equality
             constraints and so forth need to be added then the inequality
             functions in ``g_cons`` need to be added to ``minimizer_kwargs``
             too).
  ```
  ```
  g_args : sequence of tuples, optional
      Any additional fixed parameters needed to completely specify the
      feasible set functions ``g_cons``.
      ex. g_cons = (f1(x, *args1), f2(x, *args2))
      then
          g_args = (args1, args2)
  ```
  ```
  n : int, optional
      Number of sampling points used in the construction of the topography
      matrix.
  ```
  ```
  k_t : int, optional
      Defines the number of columns constructed in the k-t matrix. The higher
      k is the lower the amount of minimisers will be used for local search
      routines. If None the empirical model of Henderson et. al. (2015) will
      be used. (Note: Lower ``k_t`` values increase the number of local
      minimisations that need need to be performed, but could potentially be
      more robust depending on the local solver used due to testing more
      local minimisers on the function hypersuface)
  ```
  ```
  minimizer_kwargs : dict, optional
      Extra keyword arguments to be passed to the minimizer
      ``scipy.optimize.minimize`` Some important options could be:

          method : str
              The minimization method (e.g. ``SLSQP``)
          args : tuple
              Extra arguments passed to the objective function (``func``) and
              its derivatives (Jacobian, Hessian).

          options : {ftol: 1e-12}
  ```
  ```
  disp : bool, optional # (TODO)
      Display status messages
  ```
  ```
  callback : callable, `callback(xk, convergence=val)`, optional: # (TODO)
      A function to follow the progress of the minimization. ``xk`` is
      the current value of ``x0``. ``val`` represents the fractional
      value of the population convergence.  When ``val`` is greater than one
      the function halts. If callback returns `True`, then the minimization
      is halted (any polishing is still carried out).
  ```

  Returns
  -------
  ```
  res : OptimizeResult
      The optimization result represented as a `OptimizeResult` object.
      Important attributes are:
      ``x`` the solution array corresponding to the global minimum,
      ``fun`` the function output at the global solution,
      ``xl`` an ordered list of local minima solutions,
      ``funl`` the function output at the corresponding local solutions,
      ``success`` a Boolean flag indicating if the optimizer exited
      successfully and
      ``message`` which describes the cause of the termination,
      ``nfev`` the total number of objective function evaluations including
      the sampling calls.
      ``nlfev`` the total number of objective function evaluations
      culminating from all local search optimisations.
  ```
  
  Notes
  -----
  Global optimization using the Topographical Global Optimization (TGO)
  method first proposed by T??rn (1990) [1] with the the semi-empirical
  correlation by Hendorson et. al. (2015) [2] for k integer defining the
  k-t matrix.

  The TGO is a clustering method that uses graph theory to generate good
  starting points for local search methods from points distributed uniformly
  in the interior of the feasible set. These points are generated using the
  Sobol (1967) [3] sequence.

  The local search method may be specified using the ``minimizer_kwargs``
  parameter which is inputted to ``scipy.optimize.minimize``. By default
  the ``SLSQP`` method is used. In general it is recommended to use the
  ``SLSQP`` or ``COBYLA`` local minimization if inequality constraints
  are defined for the problem since the other methods do not use constraints.

  Performance can sometimes be improved by either increasing or decreasing
  the amount of sampling points ``n`` depending on the system. Increasing the
  amount of sampling points can lead to a lower amount of minimisers found
  which requires fewer local optimisations. Forcing a low ``k_t`` value will
  nearly always increase the amount of function evaluations that need to be
  performed, but could lead to increased robustness.

  The primitive polynomials and various sets of initial direction numbers for
  generating Sobol sequences is provided by [4] by Frances Kuo and
  Stephen Joe. The original program sobol.cc is available and described at
  http://web.maths.unsw.edu.au/~fkuo/sobol/ translated to Python 3 by
  Carl Sandrock 2016-03-31

  Examples
  --------
  First consider the problem of minimizing the Rosenbrock function. This
  function is implemented in `rosen` in `scipy.optimize`
  ```
  >>> from scipy.optimize import rosen, tgo
  >>> bounds = [(0,2), (0, 2), (0, 2), (0, 2), (0, 2)]
  >>> result = tgo(rosen, bounds)
  >>> result.x, result.fun
  (array([ 1.,  1.,  1.,  1.,  1.]), 2.9203923741900809e-18)
  ```
  Note that bounds determine the dimensionality of the objective
  function and is therefore a required input, however you can specify
  empty bounds using ``None`` or objects like numpy.inf which will be
  converted to large float numbers.
  ```
  >>> bounds = [(None, None), (None, None), (None, None), (None, None)]
  >>> result = tgo(rosen, bounds)
  >>> result.x
  array([ 0.99999851,  0.99999704,  0.99999411,  0.9999882 ])
  ```
  Next we consider the Eggholder function, a problem with several local
  minima and one global minimum.
  (https://en.wikipedia.org/wiki/Test_functions_for_optimization)

  ```
  >>> from scipy.optimize import tgo
  >>> from _tgo import tgo
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

  ```
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
  ```
  >>> result_2 = tgo(eggholder, bounds, n=1000)
  >>> len(result.xl), len(result_2.xl)
  (10, 60)
  ```

  ...or by lowering the k_t value:
  ```
  >>> result_3 = tgo(eggholder, bounds, k_t=1)
  >>> len(result.xl), len(result_2.xl), len(result_3.xl)
  (10, 60, 48)
  ```

  To demonstrate solving problems with non-linear constraints consider the
  following example from [5] (Hock and Schittkowski problem 18):
  ```
  Minimize: f = 0.01 * (x_1)**2 + (x_2)**2

  Subject to: x_1 * x_2 - 25.0 >= 0,
              (x_1)**2 + (x_2)**2 - 25.0 >= 0,
              2 <= x_1 <= 50,
              0 <= x_2 <= 50.

  Approx. Answer:
      f([(250)**0.5 , (2.5)**0.5]) = 5.0
  ```
  ```
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
  ```

References
----------
1. T??rn, A (1990) "Topographical global optimization", Reports on Computer Science and Mathematics Ser. A, No 199, 8p. Abo Akademi University, Sweden
2. Henderson, N, de S?? R??go, M, Sacco, WF, Rodrigues, RA Jr. (2015) "A new look at the topographical global optimization method and its application to the phase stability analysis of mixtures", Chemical Engineering Science, 127, 151-174
3. Sobol, IM (1967) "The distribution of points in a cube and the approximate evaluation of integrals. USSR Comput. Math. Math. Phys. 7, 86-112.
4. Joe and F. Y. Kuo (2008) "Constructing Sobol sequences with better two-dimensional projections", SIAM J. Sci. Comput. 30, 2635-2654
5. Hoch, W and Schittkowski, K (1981) "Test examples for nonlinear programming codes." Lecture Notes in Economics and mathematical Systems, 187. Springer-Verlag, New York. http://www.ai7.uni-bayreuth.de/test_problem_coll.pdf


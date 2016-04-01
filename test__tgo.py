#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NOTE: For TestTgoFuncs test_f1 and test_f2 adequately test the
      functionality of the algorithm, the rest can be omitted to
      increase speed.

Test Run examples:

ex.
$ python2 -m unittest -v tgo_tests.TestTgoFuncs
$ python2 -m unittest -v tgo_tests.TestTgoSubFuncs
$ python2 -m unittest -v tgo_tests.TestTgoSubFuncs.test_t1
"""
import unittest
import numpy
from _tgo import *

class TestFunction(object):
    def __init__(self, bounds, expected_x, expected_fun=None,
                 expected_xl=None, expected_funl=None):
        self.bounds = bounds
        self.expected_x = expected_x
        self.expected_fun = expected_fun
        self.expected_xl = expected_xl
        self.expected_funl = expected_funl

class Test1(TestFunction):
    def f(self, x, r, s):
        return x[0]**2 + x[1]**2

    def g(self, C):
        #return -(numpy.sum(C, axis=1) - 6.0)
        return -(numpy.sum(C, axis=-1) - 6.0)

test1_1 = Test1(bounds=[(-1, 6), (-1, 6)],
                expected_x=[0, 0])
test1_2 = Test1(bounds=[(0, 1), (0, 1)],
                expected_x=[0, 0])

class Test2(TestFunction):
    """
    Scalar function with several minima to test all minimiser retrievals
    """
    g = None

    def f(self, x):
        return (x - 30) * numpy.sin(x)

    def g(self, x):
        return 58 - numpy.sum(x, axis=-1)

test2_1 = Test2(bounds=[(0, 60)],
              expected_x = [1.53567906],
              expected_fun = [-28.44677132],  # Important to test that fun
                                              # return is in the correct order
              expected_xl = numpy.array([[  1.53567906],
                                         [ 55.01782167],
                                         [  7.80894889],
                                         [ 48.74797493],
                                         [ 14.07445705],
                                         [ 42.4913859 ],
                                         [ 20.31743841],
                                         [ 36.28607535],
                                         [ 26.43039605],
                                         [ 30.76371366]]),

              expected_funl = numpy.array([-28.44677132, -24.99785984,
                                           -22.16855376, -18.72136195,
                                           -15.89423937, -12.45154942,
                                           -9.63133158,  -6.20801301,
                                           -3.43727232,  -0.46353338])
              )

test2_2 = Test2(bounds=[(0, 4.5)],
              expected_x = [1.53567906],
              expected_fun = [-28.44677132],  # Important to test that fun
                                              # return is in the correct order
              expected_xl = numpy.array([[1.53567906]]),
              expected_funl = numpy.array([-28.44677132])
              )


class Test3(TestFunction):
    """
    Hock and Schittkowski 19 problem (HS19). Hoch and Schittkowski (1991)

    Approx. Answer:
        f_test_3([14.095, 0.84296]) = -6961.814744487831

    """
    def f(self, x):     # TODO: Add f bounds from original problem
        return (x[0] - 10.0)**3.0 + (x[1] - 20.0)**3.0

    def g(self, C):
        return (-(-(C[:, 0] - 5)**2 - (C[:, 1] - 5)**2 - 100.0)
                & -((C[:, 0] - 6)**2 - (C[:, 1] - 5)**2 - 82.81))


# FIXME: The bounds appear not to include the expected_x value
test3 = Test3(bounds=[(13.0, 100.0), (0.0, 100.0)],
              expected_x=[14.095, 0.84296])


class Test4(TestFunction):
    """ Rosenbrock's function  Ans x1 = 1, x2 = 1, f = 0 """
    g = None

    def f(self, x):
        return (1.0 - x[0])**2.0 + 100.0*(x[1] - x[0]**2.0)**2.0


test4_1 = Test4(bounds=[(-3.0, 3.0), (-3.0, 3.0)],
                expected_x=[1, 1])

test_atol = 1e-5


class Test5(TestFunction):
    """
    Himmelblau's function
    https://en.wikipedia.org/wiki/Himmelblau's_function
    """
    g = None

    def f(self, x):
        return (x[0]**2 + x[1] - 11)**2 + (x[0] + x[1]**2 - 7)**2


test5_1 = Test5(bounds=[(-6, 6),
                        (-6, 6)],
                expected_x=None,
                expected_fun=[0.0],  # Important to test that fun
                # return is in the correct order
                expected_xl=numpy.array([[3.0, 2.0],
                                         [-2.805118, 3.1313212],
                                         [-3.779310, -3.283186],
                                         [3.584428, -1.848126]]),

                expected_funl=numpy.array([0.0, 0.0, 0.0, 0.0])
                )

class Test5(TestFunction):
    """
    Himmelblau's function
    https://en.wikipedia.org/wiki/Himmelblau's_function
    """
    g = None

    def f(self, x):
        return (x[0]**2 + x[1] - 11)**2 + (x[0] + x[1]**2 - 7)**2


test5_1 = Test5(bounds=[(-6, 6),
                        (-6, 6)],
                expected_x=None,
                expected_fun=[0.0],  # Important to test that fun
                # return is in the correct order
                expected_xl=numpy.array([[3.0, 2.0],
                                         [-2.805118, 3.1313212],
                                         [-3.779310, -3.283186],
                                         [3.584428, -1.848126]]),

                expected_funl=numpy.array([0.0, 0.0, 0.0, 0.0])
                )

class Test6(TestFunction):
    """
    Eggholder function
    https://en.wikipedia.org/wiki/Test_functions_for_optimization
    """
    g = None

    def f(self, x):
        return (-(x[1] + 47.0)
                * numpy.sin(numpy.sqrt(abs(x[0]/2.0 + (x[1] + 47.0))))
                - x[0] * numpy.sin(numpy.sqrt(abs(x[0] - (x[1] + 47.0))))
                )


test6_1 = Test6(bounds=[(-512, 512),
                        (-512, 512)],
                expected_x=[512, 404.2319],
                expected_fun=[-959.6407]
                )


def run_test(test, args=(), g_args=()):
    res = tgo(test.f, test.bounds, args=args, g_func=test.g, g_args=g_args)

    # Exceptional cases
    if test == test5_1:
        # Remove the extra minimizer found in this test
        # (note all minima is at the global 0.0 value)
        res.xl = [res.xl[0], res.xl[1],
                  res.xl[3], res.xl[2]]
        res.funl = res.funl[:4]

    # Global minima
    if test.expected_x is not None:
        numpy.testing.assert_allclose(res.x, test.expected_x,
                                      rtol=test_atol,
                                      atol=test_atol)

    # (Optional tests)
    if test.expected_fun is not None:
        numpy.testing.assert_allclose(res.fun,
                                      test.expected_fun,
                                      atol=test_atol)

    if test.expected_xl is not None:

        numpy.testing.assert_allclose(res.xl,
                                      test.expected_xl,
                                      atol=test_atol)

    if test.expected_funl is not None:
        numpy.testing.assert_allclose(res.funl,
                                      test.expected_funl,
                                      atol=test_atol)

# $ python2 -m unittest -v tgo_tests.TestTgoFuncs
class TestTgoFuncs(unittest.TestCase):
    """
    Global optimisation tests:
    """
    def test_f1(self):
        r = [1, 2, 3]  # random args for test func tuple
        s = True
        run_test(test1_1, args=(r, s))

    def test_f2(self):
        run_test(test2_1)
        run_test(test2_2)

    @unittest.skip("OverflowError")
    def test_f3(self):
        """HS19 optimisation:"""
        run_test(test3)

        # OverflowError: Python int too large to convert to C long
        #   Func_min[i] = func(x_min, *args)
        # Why?
        # TODO: implement bounds in local search function
        # >>> test3.f([ -1.04572783e+08,-3.42296527e+08])
        # -4.12493867624096e+25

    def test_t4(self):
        """Rosenbrock function"""
        run_test(test4_1)

    def test_t5(self):
        """Himmelblau's function"""
        run_test(test5_1)

    def test_t6(self):
        """Eggholder function"""
        run_test(test6_1)


# $ python2 -m unittest -v tgo_tests.TestTgoSubFuncs
class TestTgoSubFuncs(unittest.TestCase):
    """
    TGO subfunction tests using known solution (test_f1)
    """
    # Init tgo class
    # Note: Using ints for irrelevant class inits like func
    TGOc = TGO(1, 1)
    #TGOc = TGO()
    # int bool solution for known sampling points
    T_Ans = numpy.array([[0, 0, 0, 0, 0],
                         [0, 1, 1, 1, 1],
                         [1, 0, 0, 0, 0],
                         [1, 1, 1, 1, 1],
                         [0, 0, 0, 0, 1],
                         [1, 1, 0, 1, 0]])

    T_Ans = T_Ans.astype(bool)

    # Known order of sampling points
    A = numpy.array([[2, 1, 5, 3, 4],
                     [3, 2, 5, 0, 4],
                     [0, 5, 1, 3, 4],
                     [1, 5, 2, 0, 4],
                     [5, 1, 2, 3, 0],
                     [2, 4, 1, 0, 3]])

    # function values at test points
    F = numpy.array([29, 5, 25.81, 1, 25, 20])

    # Sampling points used in Henderson example
    TGOc.C = numpy.array([[2, 5],  # P1
                          [1, 2],  # P2
                          [3, 4],  # P3
                          [0, 1],  # P4
                          [5, 0],  # P5
                          [4, 2]   # P6
                          ])
    # func used
    def f_sub(x):
        return x[0]**2 + x[1]**2

    TGOc.func = f_sub
    # TODO Test that A and F from this is correct, change recorded vals
    # to answers


    #t_matrix = TGOc.topograph()
    #H = F[A]

    #T = t_matrix(H, F).astype(int)
    T, H, F = TGOc.topograph()

    def test_t1(self):
        """t-matrix construction:"""
        numpy.testing.assert_array_equal(self.T, self.T_Ans)

        #self.assertEqual(B, self.A)

    def test_t2(self):
        """k-1 topograph"""
        K_1 = self.TGOc.k_t_matrix(self.T, 1).T[0] #
        numpy.testing.assert_array_equal(K_1 , self.T_Ans[:,0])

    def test_t3(self):
        """k-3 topograph"""
        K_3 = self.TGOc.k_t_matrix(self.T, 3)
        Ans = numpy.delete(self.T_Ans, numpy.s_[3:numpy.shape(self.T_Ans)[1]]
                           , axis=-1)
        numpy.testing.assert_array_equal(K_3, Ans)

    def test_t4(self):
        """Minimizer function"""
        self.assertEqual(numpy.float32(self.TGOc.minimizers(self.T_Ans)), 3)

    def test_t5(self):
        """K_optimal"""
        numpy.testing.assert_array_equal(self.TGOc.K_optimal(), self.T_Ans)

def tgo_suite():
    """
    Gather all the TGO tests from this module in a test suite.
    """
    TestTgo = unittest.TestSuite()
    tgo_suite1 = unittest.makeSuite(TestTgoFuncs)
    tgo_suite2 = unittest.makeSuite(TestTgoSubFuncs)
    TestTgo.addTest(tgo_suite1)
    TestTgo.addTest(tgo_suite2)
    return TestTgo



if __name__ == '__main__':
    TestTgo=tgo_suite()
    unittest.TextTestRunner(verbosity=2).run(TestTgo)





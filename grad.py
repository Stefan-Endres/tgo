#!/usr/bin/env python
# -*- coding: utf-8 -*-

import concurrent.futures
import time
import numpy as np

def pmap(f, xs, pool):
    ts = [pool.submit(f,*x) for x in xs]
    return [t.result() for t in ts]


class Scalar:
    def __init__(self, f,
                 step_initial=1e-8,
                 f_eps=None,
                 max_gradient_steps=3,
                 step_tolerance=0.3,
                 gradient_tolerance=0.05,
                 dtype=float,
                 pool=None):
        self.f = f
        self.x = None
        self.f_x = None
        self.dtype = dtype
        try:
            self.step_initial = self.dtype(step_initial)
        except TypeError:
            self.step_initial = np.asarray(step_initial)
        if f_eps is None:
            self.f_eps = np.finfo(self.dtype).eps
        else:
            self.f_eps = self.dtype(f_eps)
        self.up = 1.
        self.eps = 8*np.finfo(self.dtype).eps
        self.eps2 = 2*np.sqrt(np.finfo(self.dtype).eps)
        self._gradient = None
        self._gradient_steps = None
        self._gradient_2nd = None
        self.max_gradient_steps = max_gradient_steps
        self.step_tolerance = step_tolerance
        self.gradient_tolerance = gradient_tolerance
        if pool is None:
            self.pool = concurrent.futures.ProcessPoolExecutor()
        else:
            self.pool = pool
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(65536)


    def __call__(self, x):
        if self.x is None or not np.all(x==self.x):
            self.x = x
            self.f_x = self.pool.submit(self.f,x).result()
        return self.f_x

    def _setup_initial_gradient(self):
        # FIXME: make sure dirin doesn't get too small
        dirin = 2*self.step_initial
        if isinstance(dirin, self.dtype):
            dirin = np.array([dirin]*self.n)
        self._gradient_2nd = 2*self.up/dirin**2
        self._gradient_steps = 0.1*dirin
        self._gradient = self._gradient_2nd*dirin

    def gradient(self, x):
        x = np.asarray(x)
        self(x)
        self.n = len(x)
        if self._gradient is None:
            self._setup_initial_gradient()
        if len(self._gradient_steps) != len(x):
            raise ValueError("Dimensionality of input appears to have changed "
                             "from %d to %d" % (len(self._gradient_steps),
                                                len(x)))
        return np.array(pmap(self._gradient1d,[(d,) for d in range(len(x))],
                             self.thread_pool))

    def _gradient1d(self, d):
        dfmin = 8*self.eps2*(np.abs(self.f_x)+self.up)
        vrysml = 8*self.eps**2

        xtf = self.x[d]
        epspri = self.eps2+np.abs(self._gradient[d]*self.eps2)
        stepb4 = 0
        for j in range(self.max_gradient_steps):
            optstp = np.sqrt(dfmin/(np.abs(self._gradient_2nd[d])+epspri))
            step = max(optstp, np.abs(0.1*self._gradient_steps[d]))
            step = min(step, 10*self._gradient_steps[d])
            step = max(step, vrysml)
            step = max(step, 8*np.abs(self.eps2*self.x[d]))
            if np.abs((step-stepb4)/step) < self.step_tolerance:
                break
            self._gradient_steps[d] = step
            stepb4 = step

            x1 = self.x.copy()
            x1[d] = xtf+step
            x2 = self.x.copy()
            x2[d] = xtf-step
            fs1, fs2 = pmap(self, [(x1,), (x2,)],
                            self.thread_pool)

            step = (x1[d]-x2[d])/2 # in case of round-off

            grdb4 = self._gradient[d]
            self._gradient[d] = 0.5*(fs1-fs2)/step
            self._gradient_2nd[d] = (fs1+fs2 - 2.*self.f_x)/step**2

            if (np.abs(grdb4-self._gradient[d])
                /(np.abs(self._gradient[d])+dfmin/step)
                < self.gradient_tolerance):
                break
        return self._gradient[d]

if __name__=='__main__':
    k = np.array([1e-6,1e-3,1,1e3,1e6])
    def f(x):
        return np.sin(np.dot(k,x))
    def df(x):
        return np.cos(np.dot(k,x))*k

    F = Scalar(f)
    for i in range(20):
        print()
        x = np.random.randn(len(k))
        print(F.gradient(x))
        print(df(x))

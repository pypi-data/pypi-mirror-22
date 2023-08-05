# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 11:26:41 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.core.symbs_tools import simplify as simp
import numpy
import sympy
from sympy.printing.theanocode import theano_function
import copy


try:
    import itertools.imap as map
except ImportError:
    pass

def norm(x):
    return numpy.sqrt(float(numpy.dot(x.flatten(), x.flatten())))


NumericalOperationParser = {'add': numpy.add,
                            'prod': lambda a1, a2: a1*a2,
                            'dot': numpy.dot,
                            'inv': numpy.linalg.inv,
                            'div': numpy.divide,
                            'norm': norm,
                            'copy': lambda x: x,
                            'none': lambda: None,
                            }


def evalop_generator(nums, op):
    args = list()
    for arg in op.args:
        if isinstance(arg, PHSNumericalOperation):
            args.append(evalop_generator(nums, arg))
        elif isinstance(arg, str):
            args.append(getattr(nums, arg))
        elif arg is None:
            args.append(numpy.array([]))
        else:
            assert isinstance(arg, (int, float))
            args.append(arg)
    func = PHSNumericalOperation(op.operation, args)

    if isinstance(func(), (int, float)):
        def eval_func():
            return func()
    else:
        def eval_func():
            return numpy.asarray(func())
    return eval_func


def evalfunc_generator(nums, name):
    """
    Return an evaluator of 'nums'.'name'_expr
    """
    expr = getattr(nums.method, name + '_expr')
    args = getattr(nums.method, name + '_args')
    inds = getattr(nums.method, name + '_inds')
    func = lambdify(args, expr, subs=nums.method.core.subs)

    if len(inds) > 0:
        inds = numpy.array(inds)
    else:
        inds = list()

    def eval_func():
        return numpy.asarray(func(*numpy.array(nums.args[inds])))
    return eval_func


def getarg_generator(nums, inds):
    """
    generators of 'get'
    """
    if len(inds) > 0:
        inds = numpy.array(inds)
    else:
        inds = list()

    def get_func():
        return nums.args[inds].copy()

    return get_func


def setarg_generator(nums, inds):
    """
    generators of 'set'
    """
    if len(inds) > 0:
        inds = numpy.array(inds)
    else:
        inds = list()

    def set_func(array):
        nums.args[inds] = array

    return set_func


def getfunc_generator(nums, name):
    """
    generators of 'get'
    """

    def get_func():
        return copy.copy(getattr(nums, '_' + name))

    return get_func


def setfunc_generator(nums, name):
    """
    generators of 'set'
    """

    def set_func(array):
        setattr(nums, '_' + name, array)

    return set_func


class PHSNumericalOperation:

    def __init__(self, operation, args):

        self.operation = operation
        self.args = args

        func = NumericalOperationParser[self.operation]

        self.call = [func, [None, ]*len(args)]
        self.freesymbols = set()

        for i, arg in enumerate(args):
            if isinstance(arg, PHSNumericalOperation):
                symbs = arg.freesymbols
                arg = arg.call
            elif isinstance(arg, str):
                symbs = set([arg, ])
            else:
                symbs = set()
            self.call[1][i] = arg
            self.freesymbols = self.freesymbols.union(symbs)

    def __call__(self):
        args = list()
        for el in self.args:
            if hasattr(el, '__call__'):
                args.append(el())
            else:
                args.append(el)
        return self.call[0](*args)


def theano_lambdify(args, expr, vector_expr):
    if vector_expr:
        expr_lambda = theano_function(args, expr,
                                      on_unused_input='ignore')
    else:
        expr_lambda = theano_function(args, [expr],
                                      on_unused_input='ignore')
    return expr_lambda


def numpy_lambdify(args, expr):
    func = sympy.lambdify(args,
                          expr,
                          dummify=False,
                          modules='numpy')
    return lambda *args: func(*map(numpy.array, args))


def lambdify(args, expr, subs=None, simplify=True, theano=True):
    """
    call to lambdify with chosen options
    """
    vector_expr = hasattr(expr, 'index')
    if subs is not None:
        if vector_expr:
            for i, e in enumerate(expr):
                expr[i] = e.subs(subs)
        else:
            expr = expr.subs(subs)
    if simplify:
        expr = simp(expr)
    expr = sympy.sympify(expr)

    if theano:
        try:
            expr_lambda = theano_lambdify(args, expr, vector_expr)
        except:
            expr_lambda = numpy_lambdify(args, expr)
    else:
        expr_lambda = numpy_lambdify(args, expr)

    return expr_lambda


def find(symbs, allsymbs):
    """
    sort elements in symbs according to allsymbs, and return args and \
list of positions in allsymbs
    """
    args = []
    inds = []
    n = 0
    for symb in allsymbs:
        if symb in symbs:
            args.append(symb)
            inds.append(n)
        n += 1
    return tuple(args), tuple(inds)


def regularize_dims(vec):
    """
    return column vector of zeros if vec has no shape along 2nd dimension
    """
    if any(dim == 0 for dim in vec.shape):
        vec = sympy.zeros(vec.shape[0], 1)
    return vec

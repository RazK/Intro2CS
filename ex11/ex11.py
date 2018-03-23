#!/usr/bin/env python3

import math

EPSILON = 1e-5
DELTA = 1e-3
SEGMENTS = 100
INVERSE_INITIAL_X = 1


def plot_func(graph, f, x0, x1, num_of_segments=SEGMENTS, c='black'):
    """
    plot f between x0 to x1 using num_of_segments straight lines
    to the graph object. the function will be plotted in color c
    """
    x_step = (x1 - x0) / num_of_segments
    x = x0
    for seg in range(num_of_segments):
        p0 = (x, f(x))
        p1 = (x + x_step, f(x + x_step))
        graph.plot_line(p0, p1, c)
        x += x_step


def const_function(c):
    """return the mathematical function f such that f(x) = c
    >>> const_function(2)(2)
    2
    >>> const_function(4)(2)
    4
    """
    def f(x):
        return c
    return f


def identity():
    """return the mathematical function f such that f(x) = x
    >>> identity()(3)
    3
    """
    def f(x):
        return x
    return f


def sin_function():
    """return the mathematical function f such that f(x) = sin(x)
    >>> sin_function()(math.pi/2)
    1.0
    """
    def f(x):
        return math.sin(x)
    return f


def sum_functions(g, h):
    """return f s.t. f(x) = g(x)+h(x)"""
    def f(x):
        return g(x) + h(x)
    return f


def sub_functions(g, h):
    """return f s.t. f(x) = g(x)-h(x)"""
    def f(x):
        return g(x) - h(x)
    return f


def mul_functions(g, h):
    """return f s.t. f(x) = g(x)*h(x)"""
    def f(x):
        return g(x) * h(x)
    return f


def div_functions(g, h):
    """return f s.t. f(x) = g(x)/h(x)"""
    def f(x):
        return  g(x) / h(x)
    return f


def binary_search(f, x0, x1, fx0, fx1, epsilon):
    """
    Binary search for x where | f(x) | < epsilon
    with minimum calls to f(x)
    Assumes:
        f is monotonic
        epsilon > 0
        x0 < x1
    :param f:       function of x
    :param x0:      lower x limit
    :param x1:      upper x limit
    :param fx0:     f(x0)
    :param fx1:     f(x1)
    :param epsilon: max acceptable x error
    :return:        float - x where | f(x) | < epsilon
    """
    # Assert solution exists between limits
    if fx0 * fx1 > 0:
        return None

    # Find a lion in the desert
    while abs(fx0 - fx1) >= epsilon:
        # Split the desert
        x = (x0 + x1) / 2
        # Call the lion
        fx = f(x)  # The only (expensive) call to f(x)
        # Check if the lion is found
        if abs(fx) < epsilon:
            return x
        # Otherwise look where it roars
        # Lion on the right side?
        if fx * fx1 <= 0:
            x0, fx0  = x, fx
        # Lion on the left side!
        elif fx * fx0 <= 0:
            x1, fx1 = x, fx
        # No lion in this desert?
        else:
            return None

    # Roarrr!
    return None

def binary_search_recursive(f, x0, x1, fx0, fx1, epsilon):
    """
    Note: This is another implementation for the binary_search() method,
    even though I eventually used the latter implementation, I thought it
    would be nice to include this one as well.
    Feel free to comment, or ignore it if you're in a haste.

    Recursive search (Binary search) for x where | f(x) | < epsilon
    with minimum calls to f(x)
    Assumes:
        f is monotonic
        epsilon > 0
        x0 < x1
    :param f:       function of x
    :param x0:      lower x limit
    :param x1:      upper x limit
    :param fx0:     f(x0)
    :param fx1:     f(x1)
    :param epsilon: max acceptable x error
    :return:        float - x where | f(x) | < epsilon
    """
    # Assert solution exists between limits
    if fx0 * fx1 > 0:
        return None

    # Find a lion in the desert
    x = (x0 + x1) / 2
    fx = f(x) # The only (expensive) call to f(x)

    # Check if found a lion
    if abs(fx) < epsilon:
        return x

    # Otherwise split the desert
    else:
        # Look left
        solution = binary_search_recursive(f, x0, x, fx0, fx, epsilon)

        # No lion? Look right
        if solution == None:
            solution= binary_search_recursive(f, x, x1, fx, fx1, epsilon)

        # return the lion
        return solution


def solve(f, x0=-10, x1=10, epsilon=EPSILON):
    """
    Find a solution x : f(x) = 0 to f in the range x0 and x1
    assuming that f is monotonic and x0 < x1
    If no solution was found return None
    """
    return binary_search(f, x0, x1, f(x0), f(x1), epsilon)


def inverse(g, epsilon=EPSILON):
    """return f s.t. f(g(x)) = x"""
    def f(y):
        """
        Find x where g(x) = y <--> g(x) - y = 0 <--> Solve for g(x) - y = 0
        Expand x search limits by shifting to the side and then search
        within new limits using solve().

        Example: finding x where g(x)-y=0 by gradually expanding search limits

        iteration 1           [--0--]       x
        iteration 2        [--]  0  [--]    x
        iteration 3     [--]     0     [--] x
        ...            ...       0       ...x
        iteration n  [--]        0        [-x] ==> found x!

        x is found after n iterations to the left of 0
        """
        gy = sub_functions(g, const_function(y))
        x_limit = INVERSE_INITIAL_X
        x = solve(gy, -1*x_limit, x_limit, epsilon)
        # Start with a small range, keep expanding to both sides - double
        # the search range every iteration
        while x == None:
            # Look for solution on both sides of the previous range
            # Check to the left (negative range)
            x = solve(gy, x_limit, 2*x_limit, epsilon)
            # No solution? Check to the right
            if x == None:
                x = solve(gy, -2*x_limit, -1*x_limit, epsilon)
            # Expand range by 2 (since solving with binary search this makes
            # most sense)
            x_limit *= 2
        return x
    return f


def compose(g, h):
    """return the f which is the compose of g and h """
    def f(x):
        return g(h(x))
    return f


def derivative(g, delta=DELTA):
    """return f s.t. f(x) = g'(x)"""
    def f(x):
        return (g(x + delta) - g(x)) / delta
    return f


def definite_integral(f, x0, x1, num_of_segments=SEGMENTS):
    """
    return a float - the definite_integral of f between x0 and x1
    >>> definite_integral(const_function(3),-2,3)
    15.000000000000025
    """
    if x1 == x0:
        return 0

    area = 0
    seg_width = (x1 - x0) / num_of_segments
    seg_0_x = x0 + (seg_width / 2)
    for i in range(num_of_segments):
        seg_x = seg_0_x + (i * seg_width)
        area += f(seg_x) * seg_width
    return  area


def integral_function(f, delta=0.01):
    """return F such that F'(x) = f(x)"""
    def F(x):
        num_of_segments = math.ceil(abs(x) / delta)
        return definite_integral(f, 0, x, num_of_segments)
    return F


def newton_method_x(f, x0, x1, fx0, fx1, epsilon):
    """
    Find x where |f(x)| < epsilon using Newton's method.
    :param f:       function of x
    :param x0:      lower x limit
    :param x1:      upper x limit
    :param fx0:     f(x0)
    :param fx1:     f(x1)
    :param epsilon: max acceptable x error
    :return:        float - x where | f(x) | < epsilon

    See Newton's Method:
    https://en.wikipedia.org/wiki/Newton%27s_method

    Summary:
    Find t(x) : tangent line approximation of f(x) at x0
    Then, find tangent intersection with X axis (at x = tix) - this is likely
    to be very close to f's intersection with X axis.
    If it isn't - take a new tangent to f at tix, and keep going until done.

    Approximate tangent at x0:
                     (fx1) - fx0))
    t(x) - f(x0) =  --------------- (x - x0)
                     ( x1  -  x0 )

    Therefore, tangent intersection with X (tix) is given:
         ( x1  -  x0 )
    x = -------------- (0 - f(x0)) + x0
         (fx1) - fx0))
    """
    tix = ((x1 - x0) / (fx1 - fx0)) * (0 - fx0) + x0
    fix = f(tix)
    # Check if found the inverted x at tix:
    if abs(fix) < epsilon:
        return tix
    # Otherwise draw another tangent and follow Newton's method
    else:
        return newton_method_x(f,tix,x0,fix,fx0,epsilon)


def inverse_newton(g, epsilon=EPSILON):
    """return f s.t. f(g(x)) = x"""
    def f(y):
        # Guess y values until | g(x) - y | < epsilon using Newton's method
        # https://en.wikipedia.org/wiki/Newton%27s_method

        # Find intersection of tangent at (y0) with x axis ()
        # Check if x' ~= g(x)

        # Get the function gy(x) = g(x) - y
        gy = sub_functions(g, const_function(y))

        # Start by guessing
        x0 = INVERSE_INITIAL_X0
        x1 = INVERSE_INITIAL_X1
        gyx0, gyx1 = gy(x0), gy(x1)

        # Go with Newton
        return  newton_method_x(gy, x0, x1, gyx0, gyx1, epsilon)
    return f


def ex11_func_list():
    """return list with the functions in q.13"""
    # Useful functions
    pow_2 = mul_functions(identity(), identity())
    sin = sin_function()
    cos = derivative(sin)

    # Build functions list
    func_list = {}

    # 0) f(x) = 4
    func_list[0] = const_function(4)

    # 1) f(x) = 3 - sin(x)
    func_list[1] = sub_functions(const_function(3), sin)

    # 2) f(x) = sin(x-2)
    x_minus_2 = sub_functions(identity(), const_function(2))
    func_list[2] = compose(sin, x_minus_2)

    # 3) f(x) = 10 / (2 + sin(x) + x^2)
    sin_plus_pow_2 = sum_functions(sin, pow_2)
    two_plus_sin_plus_pow_2 = sum_functions(const_function(2), sin_plus_pow_2)
    func_list[3] = div_functions(const_function(10),two_plus_sin_plus_pow_2)

    # 4) f(x) = cos(x) / (sin(x) - 2)
    sin_minus_2 = sub_functions(sin, const_function(2))
    func_list[4] = div_functions(cos, sin_minus_2)

    # 5) f(x) = -0.1 * integral(0.3x^2 + 0.7x -1)dx
    zero_3_x_pow2 = mul_functions(const_function(0.3), pow_2)
    zero_7_x = mul_functions(const_function(0.7), identity())
    zero_3_x_pow2_plus_zero_7_x = sum_functions(zero_3_x_pow2, zero_7_x)
    minus_1 = const_function(-1)
    inside_integral = sum_functions(zero_3_x_pow2_plus_zero_7_x, minus_1)
    integral_phrase = integral_function(inside_integral)
    func_list[5] = mul_functions(const_function(-0.1), integral_phrase)

    # 6) f(x) = (cos(sin(x)) - 0.3cos(x)) * 2
    cos_sin = compose(cos, sin)
    zero_3_cos = mul_functions(const_function(0.3), cos)
    cos_sin_minus_zero_3_cos = sub_functions(cos_sin, zero_3_cos)
    func_list[6] = mul_functions(cos_sin_minus_zero_3_cos, const_function(2))

    # 7) f(x) = inverse(2 - x^3)
    pow_3 = mul_functions(pow_2, identity())
    two_minus_pow_3 = sub_functions(const_function(2), pow_3)
    func_list[7] = inverse(two_minus_pow_3)

    # Done!
    return func_list.values()


# func that genrate the figure in the ex description
def example_func(x):
    return (x/5)**3

if __name__ == "__main__":
    import tkinter as tk
    from ex11helper import Graph
    # un-tag the following lines to activate the doctests
    import doctest
    doctest.testmod()
    master = tk.Tk()
    graph = Graph(master, -10, -10, 10, 10)
    # un-tag the line below after implementation of plot_func
#    plot_func(graph,example_func,-10,10,SEGMENTS,'red')
    color_arr = ['black', 'blue', 'red', 'green', 'brown', 'purple',
                 'dodger blue', 'orange']
    # un-tag the lines below after implementation of ex11_func_list
    color = iter(color_arr)
    for f in ex11_func_list():
        plot_func(graph, f, -10, 10, SEGMENTS, next(color))

    master.mainloop()

import moviepy.editor as mpy
from itertools import product
import numpy as np
from math import exp, inf


def default_formula(t):  # returns function for Julia set in current moment
    # it should take only one complex number and returns another one
    q = -0.8 + 0.156j - 0.01 * t  # as many calculations as possible should be here since this block runs only
    # on formula() call, not also on translate()
    def translate(z):
        return pow(z, 2) + q  # in this implementation it's usual z -> z^2 + c translation, and c slowly moves
    return translate


def default_metric(z, translate):  # this function evaluates convergence speed
    # here it's 1-e^(-|z|) after 150 iterations or 1 if it's too large
    # so, 0 means convergence to zero, 1 means infinitely fast growth of |z|
    # although in example resulting value is scalar, it can be tuple, if there are several
    # points of attraction or if several metrics used at the same time
    a = 0
    for k in range(150):  # this number was chosen empirically for better look of .gif
        try:
            z = translate(z)
            a = abs(z)
        except Exception:  # we come here if z is too large
            break
    if np.isnan(a):
        a = inf
    e = 1 - exp(-a * 2)  # also empirically
    return e


def default_color(a):  # shows how to mark convergence by colors
    if isinstance(a, tuple):  # example can't properly deal with tuples in a, but still can work with them
        a = sum(a)
    return 255 * a, 255 * a, 255  # points where z runs to infinity are close to white, where it close to 0 – to blue


class GifBuilder:
    def __init__(self,  # first three arguments are described in detail in their defaults
                 formula=default_formula,  # describes function Julia set will be drawn to and its changes in time
                 metric=default_metric,  # algorithm used to evaluate speed of convergence
                 color=default_color,  # creates a rgb color from value returned by metric()
                 duration=1.0,  # duration of resulting .gif
                 fps=2,  # frames per second in it
                 size=(300, 300),  # and, obviously, its size
                 square_side=3  # side of square with center in (0,0) that will be pictured
                 ):
        self.formula = formula
        self.color = color
        self.metric = metric
        self.duration = duration
        self.fps = fps
        self.size = size
        self.square_side = square_side

    def build(self, file):
        clip = mpy.VideoClip(
            self.make_frame,
            duration=self.duration
        )
        clip.write_gif(file, fps=self.fps)

    def make_frame(self, t):  # creapes a np.array interpreted as frame in rgb
        translate = self.formula(t)  # getting the translation law for current moment
        w, h = self.size
        a = np.zeros((w, h, 3))
        for i, j in product(
                range(w), range(h)  # iterating through all combinations
        ):
            im = self.square_side * (i - w / 2) / w
            re = self.square_side * (j - h / 2) / h
            z = complex(re, im)
            m = self.metric(z, translate)  # getting convergence
            a[(i, j, 0)], a[(i, j, 1)], a[(i, j, 2)] = self.color(m)  # and color
        return a

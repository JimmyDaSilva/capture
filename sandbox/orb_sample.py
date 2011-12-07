#!/usr/bin/env python
import ecto
from ecto_opencv import cv_bp
from ecto_opencv.highgui import ImageReader
from ecto_opencv.features2d import ORB, ORBstats
from ecto_opencv.imgproc import cvtColor, Conversion
from ecto.opts import scheduler_options, run_plasm

import numpy as np
import matplotlib.pyplot as plt

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Test orb on images.')
    parser.add_argument('-i,--input', dest='input',
                        help='The input dir. %(default)s', default='./images')
    scheduler_options(parser.add_argument_group('Scheduler'))
    options = parser.parse_args()
    return options

options = parse_args()

images = ImageReader(path=options.input)
orb_m = ORB(n_features=2500)
rgb2gray = cvtColor (flag=Conversion.RGB2GRAY)
stats = ORBstats()
plasm = ecto.Plasm()
plasm.connect(images['image'] >> rgb2gray ['image'],
              rgb2gray['image'] >> orb_m['image'],
              orb_m['descriptors'] >> stats['descriptors'],
              )

run_plasm(options, plasm, locals=vars())

hist = stats.outputs.distances.toarray()
plt.plot(hist)
plt.xlim((0,255))
plt.show()

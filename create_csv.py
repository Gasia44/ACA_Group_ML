from __future__ import print_function
import argparse
import gzip
import struct
import numpy as np
import pandas as pd


filename = 'SPECTF.dat'
data = np.loadtxt(filename, delimiter=',')

pd.DataFrame(data, columns=list(range(data.shape[1]))).to_csv('SPECTF.csv')
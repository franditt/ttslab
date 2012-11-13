# -*- coding: utf-8 -*-
### PYTHON2 ###
from __future__ import unicode_literals, division, print_function
### PYTHON2 ###

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"
__copyright__ = "Copyright 2012, The DAC, Government of South Africa"
__licence__ = "MIT"
__status__ = "Prototype"

import numpy as np

def synth_filter(times, lpcs, residual, samplerate):
    samples = np.zeros(len(residual), dtype=np.int16)       #16bit samples
    startsample_index = 0
    for i, frame in enumerate(lpcs):
        try:
            endsample_index = int((times[i] + times[i+1]) * samplerate) // 2
        except IndexError:
            endsample_index = len(residual)
        if endsample_index > len(residual):
            endsample_index = len(residual)

        for j in xrange(startsample_index, endsample_index):
            # startindex = j - (len(frame) - 1)
            # if startindex < 0:
            #     offset = abs(startindex)
            #     s = np.sum(samples[j - ((len(frame) - 1) - offset):j][::-1] * frame[1:-offset])
            # else:
            #     s = np.sum(samples[j - (len(frame) - 1):j][::-1] * frame[1:])
            # samples[j] = np.int16(s) + residual[j]
            s = 0.0
            for k in xrange(1, len(frame)):
                if j - k > 0:
                    s += frame[k] * samples[j - k]
            samples[j] = np.int16(s) + residual[j]         #assuming 16bit samples
        startsample_index = endsample_index
    return samples

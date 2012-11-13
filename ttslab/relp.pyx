from __future__ import division

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"
__copyright__ = "Copyright 2012, The DAC, Government of South Africa"
__licence__ = "MIT"
__status__ = "Prototype"

import numpy as np
cimport numpy as np

DTYPE = np.float

ctypedef np.float_t DTYPE_t

def synth_filter(np.ndarray[DTYPE_t, ndim=1] times,
                 np.ndarray[DTYPE_t, ndim=2] lpcs,
                 np.ndarray[DTYPE_t, ndim=1] residual, int samplerate):
    assert times.dtype == DTYPE and lpcs.dtype == DTYPE and residual.dtype == DTYPE
    cdef int rnsamples = len(residual)
    cdef int nframes = len(lpcs)
    cdef int framelen = len(lpcs[0])
    cdef np.ndarray[DTYPE_t, ndim=1] samples = np.zeros(rnsamples, dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=1] frame
    cdef int startsample_index = 0
    cdef int endsample_index
    cdef int i, j, k
    cdef DTYPE_t s
    cdef int offset
    for i, frame in enumerate(lpcs):
        if i < nframes - 1:
            endsample_index = int((times[i] + times[i+1]) * samplerate) // 2
        else:
            endsample_index = rnsamples
        if endsample_index > rnsamples:
            endsample_index = rnsamples

        for j in range(startsample_index, endsample_index):
            s = 0.0
            for k in range(1, framelen):
                if j - k > 0:
                    s += frame[k] * samples[j - k]
            samples[j] = s + residual[j]
        startsample_index = endsample_index
    return samples

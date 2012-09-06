# -*- coding: utf-8 -*-
""" A simple Waveform class to manage audio as numpy arrays.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import os

import numpy as np
try:
    import scikits.audiolab as AL
except ImportError:
    AL = None
    import scipy.io.wavfile as wavfile

if AL:
    class Waveform(object):
        """ Simply holds waveforms in numpy arrays...
        """
        def __init__(self, filename=None):
            self.samplerate = None
            self.samples = None
            self.channels = None
            if filename:
                self.read(filename)

        def __len__(self):
            return len(self.samples)

        def read(self, filename, dtype=np.float64):
            f = AL.Sndfile(filename, 'r')
            self.samplerate = f.samplerate
            self.samples = f.read_frames(f.nframes, dtype=dtype)
            if len(self.samples.shape) == 2:
                self.channels = self.samples.shape[1]
            else:
                self.channels = 1
            f.close()

        def write(self, filename, encoding="pcm16", endianness="file", fileformat=None):
            if not fileformat:
                fileformat = os.path.basename(filename).split(".")[-1]
            format = AL.Format(fileformat, encoding, endianness)
            f = AL.Sndfile(filename, "w", format, self.channels, self.samplerate)
            f.write_frames(self.samples)
            f.close()

        def play(self):
            AL.play(self.samples, self.samplerate)
else:
    class Waveform(object):
        """ Simply holds waveforms in numpy arrays...
        """
        def __init__(self, filename=None):
            self.samplerate = None
            self.samples = None
            self.channels = None
            if filename:
                self.read(filename)

        def __len__(self):
            return len(self.samples)

        def read(self, filename):
            self.samplerate, self.samples = wavfile.read(filename)
            try:
                numsamples, self.channels = self.samples.shape
            except ValueError:
                self.channels = 1

        def write(self, filename):
            wavfile.write(filename, self.samplerate, self.samples)

        def play(self):
            raise NotImplementedError

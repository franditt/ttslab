# -*- coding: utf-8 -*-
"""
    A class to hold and perform operations on a sequence of feature
    vectors (named after Edinburgh Speech Tools class/filetype)...

    DEMITASSE:
       - need to re-examine all methods for consistency (added
         explicit starttime/endtime properties as in Praat "*Tier"
         types)

       - check everything works with reshaped/transposed array (rows =
         frames, columns = channels)

       - have a func to precalc a InterpolatedUnivariateSpline for
         future calls using interpolation, a spline instance should be
         made for each column/channel...

       - many performance issues / suboptimal implementations
         (basically learnt Numpy after the first implementation of
         this)


    OTHER TODO: 
          Track:
             Fix binary loading...
             Fix Praat loading...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import os

import numpy as np
import scipy.io.wavfile

#from trackfile package:
import io.htk

#recognised file extensions:
WAV_EXT = "wav"
EST_EXT = "est"

class FileFormatError(Exception):
    pass

class Track(object):
    """ assert len(self.times) == self.values.shape[0]
    """

    def __init__(self, name=None):
        self.values = np.array([]).reshape((0,0))
        self.times = np.array([])
        if name is not None:
            self._name = name

    def __len__(self):
        return len(self.times)

    def __str__(self):
        return "\n".join(["name:        " + self.name,
                          "numchannels: " + str(self.numchannels),
                          "numframes:   " + str(self.numframes),
                          "starttime:   " + str(self.starttime),
                          "endtime:     " + str(self.endtime)])

    @property
    def name(self):
        try:
            return self._name
        except AttributeError:
            return ""

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def numframes(self):
        return len(self)

    @property
    def numchannels(self):
        numframes, numchannels = self.values.shape
        return numchannels

    @property
    def starttime(self):
        try:
            return self._starttime
        except AttributeError:
            return 0.0

    @starttime.setter
    def starttime(self, starttime):
        self._starttime = starttime

    @property
    def endtime(self):
        try:
            return self._endtime
        except AttributeError:
            return self.times[-1]
        

######################################## FILE IO METHODS

    def load_wave(self, filepath):
        """ loads a RIFF wave file...
        """
        sr, s = scipy.io.wavfile.read(filepath)
        if len(s.shape) == 1:
            self.values = s.reshape(-1, 1)
        else:
            self.values = s
        self.times = np.arange(len(self.values)) * (sr**-1)
        self.name = os.path.basename(filepath)


    def load_binary(self, filepath, numchannels, timestep, dtype='float32'):
        """ loads from binary file...
        """
        self.values = np.fromfile(filepath, dtype=dtype)
        self.values = np.reshape(self.values, (-1, numchannels))
        self.times = np.arange(len(self.values)) * timestep
        self.name = os.path.basename(filepath)

    
    def load_htk(self, filepath, windowsize):
        """ DEMITASSE: I need to review io.htk.HTKFeatureFile
        implementation...
        """
        h = io.htk.HTKFeatureFile(filepath)
        self.times = np.array(map(io.htk.htk_int_to_float, h.central_times(io.htk.float_to_htk_int(windowsize))))
        self.values = np.array(h.observations)
        self.name = os.path.basename(filepath)
        #DEMITASSE remove this when code reviewed:
        assert len(self.values.shape) == 2
        

    def load_track(self, filepath):
        """Reads an Edinburgh Speech Tools ASCII Track file (ignores
        'Breaks')...

        DEMITASSE: need to review this...
        """

        firstline = True
        headerend = False
        breakspresent = False
        breakvals = []
        values = []
        times = []

        with open(filepath) as infh:
            for line in infh:
                if firstline:
                    firstline = False
                    if line.split() != ["EST_File", "Track"]:
                        raise FileFormatError("File is not an EST_Track file...")
                else:
                    if not headerend:
                        linelist = line.split()
                        if linelist[0] == "DataType" and linelist[1] != "ascii":
                            raise FileFormatError("File is not in ASCII format...")
                        if linelist[0] == "NumFrames":
                            numframes = int(linelist[1])
                        if linelist[0] == "NumChannels":
                            numchannels = int(linelist[1])
                        if linelist[0] == "BreaksPresent" and linelist[1].lower() == "true":
                            breakspresent = True
                        if linelist[0] == "EST_Header_End":
                            headerend = True
                    else:
                        linelist = line.split()
                        if breakspresent:
                            time, breakval, vals = float(linelist[0]), float(linelist[1]), map(float, linelist[2:])
                            times.append(time)
                            breakvals.append(breakval)
                            values.append(vals)
                        else:
                            time, vals = float(linelist[0]), map(float, linelist[1:])
                            times.append(time)
                            values.append(vals)

        self.times = np.array(times)
        self.values = np.array(values)
        #sanity check...
        if self.values.shape != (numframes, numchannels):
            raise FileFormatError("Data does not match header info...")  
        self.name = os.path.basename(filepath)
        #DEMITASSE remove this when reviewed:
        assert len(self.values.shape) == 2
        

######################################## EDIT METHODS

    def zero_starttime(self):
        self.times -= self.starttime
        if hasattr(self, "_endtime"):
            self._endtime -= self.starttime
        if hasattr(self, "_starttime"):
            self._starttime = 0.0

    def slice(self, idxa, idxb, copy=True):
        """ returns a new track sliced using provided indices (like
            Python list slicing)... copy=False makes use of Numpy
            views to share data/memory...
        """
        t = Track()
        if copy:
            t.values = self.values[idxa:idxb].copy()
            t.times = self.times[idxa:idxb].copy()
        else:
            t.values = self.values[idxa:idxb]
            t.times = self.times[idxa:idxb]
        return t

    def index_at(self, time, method="round"):
        """ Returns the index of the closest sample to 'time'...
            method in ['round', 'ceil', 'floor']
        """
        diffs = self.times - time        
        if method == "round":
            return np.abs(diffs).argmin()
        elif method == "ceil":
            pdiffi = np.flatnonzero(diffs > 0.0)
            try:
                return pdiffi[0]
            except IndexError:
                return len(diffs)
        elif method == "floor":
            ndiffi = np.flatnonzero(diffs < 0.0)
            try:
                return ndiffi[-1]
            except IndexError:
                return 0
        else:
            raise Exception("Unsupported method: %s" % method)

    # INCLUDE WHEN UNITTESTS IMPLEMENTED
    # def index_at(self, time):
    #     """ Returns the index of the closest sample to time... faster
    #         due to taking into account ordering of time (TEST LATER).
    #     """
    #     from bisect import bisect_left #move out when using this function...
    #     if time < self.starttime:
    #         return 0
    #     elif time > self.endtime:
    #         return len(self) - 1
    #     else:
    #         i = bisect_left(self.times, time)
    #         if self.times[i] - time > 0.5:
    #             i -= 1
    #         return i

    

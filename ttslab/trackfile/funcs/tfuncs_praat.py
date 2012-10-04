#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Provides Track methods to extract features from wavefiles using
    Praat...and manipulate 1-d tracks...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import os
import math
import re

import numpy as np
import subprocess
from tempfile import NamedTemporaryFile
from scipy.interpolate import InterpolatedUnivariateSpline, UnivariateSpline

from .. trackfile import Track

PRAAT_BIN = "praat"
DEF_EXTRACT_MINPITCH = 50   #used when fixocterrs is True
DEF_EXTRACT_MAXPITCH = 600  #used when fixocterrs is True
DEF_MINPITCH = 50
DEF_MAXPITCH = 350
DEF_TIMESTEP = 0.005     #0.0 -> calc from pitch
DEF_BANDWIDTH = 100.0    #Hz (Bandwidth parameter)

PRAAT_GET_F0 = \
"""#
form Fill attributes
   text input_wav_file_name
endform

Read from file... 'input_wav_file_name$'

To Pitch... %(timestep)s %(minpitch)s %(maxpitch)s
%(smoothing)sSmooth... %(smoothingbandwidth)s

starttime = Get start time
endtime = Get end time
steptime= Get time step

printline 'starttime'
printline 'endtime'
printline 'steptime'

num_frames = Get number of frames
for i from 1 to num_frames
        time = Get time from frame number... i
        value = Get value in frame... i Hertz
        printline 'time:7' 'value:7'
endfor
"""

PRAAT_GET_INTENSITY = \
"""#
form Fill attributes
   text input_wav_file_name
endform

Read from file... 'input_wav_file_name$'

To Intensity... %(smoothingbandwidth)s %(timestep)s yes

starttime = Get start time
endtime = Get end time
steptime= Get time step

printline 'starttime'
printline 'endtime'
printline 'steptime'

num_frames = Get number of frames
for i from 1 to num_frames
        time = Get time from frame number... i
        value = Get value in frame... i
        printline 'time:7' 'value:7'
endfor
"""



def get_f0(track, wavfilelocation, minpitch=DEF_MINPITCH, maxpitch=DEF_MAXPITCH, timestep=DEF_TIMESTEP, fixocterrs=False, smoothingbandwidth=None):
    """Use "praat" to extract pitch contour...
    """

    wavfilelocation = os.path.abspath(wavfilelocation)
    if fixocterrs:
        parms = {'minpitch' : DEF_EXTRACT_MINPITCH,
                 'maxpitch' : DEF_EXTRACT_MAXPITCH,
                 'timestep' : timestep}
    else:
        parms = {'minpitch' : minpitch,
                 'maxpitch' : maxpitch,
                 'timestep' : timestep}
    if smoothingbandwidth is None:
        parms["smoothing"] = "#"
    else:
        parms["smoothing"] = ""
    parms["smoothingbandwidth"] = smoothingbandwidth

    #write temp file - Praat script
    tempfh = NamedTemporaryFile()
    tempfh.write(PRAAT_GET_F0 % parms)
    tempfh.flush()

    p = subprocess.Popen([PRAAT_BIN,
                          tempfh.name,
                          wavfilelocation],
                         stdout=subprocess.PIPE)
    stdout_text = p.communicate()[0]
    tempfh.close()

    lines = stdout_text.splitlines()

    starttime = float(lines[0])
    endtime = float(lines[1])
    timestep = float(lines[2])
    times = []
    values = []
    for line in lines[3:]:
        try:
            time, value = line.split()
        except ValueError:
            continue
        try:
            values.append(float(value))
        except ValueError:
            values.append(0.0)
        times.append(float(time))

    track.times = np.array(times)
    track.values = np.array(values).reshape(-1, 1)
    track.praattype = "PitchTier"
    track._starttime = starttime
    track._endtime = endtime
    track.name = ".".join(os.path.basename(wavfilelocation).split(".")[:-1])
    if fixocterrs:
        #try to correct for octave errors:
        track.values[track.values > maxpitch] = track.values[track.values > maxpitch] / 2
        track.values[track.values < minpitch] = track.values[track.values < minpitch] * 2
        

def get_intensity(track, wavfilelocation, timestep=DEF_TIMESTEP, smoothingbandwidth=DEF_BANDWIDTH):
    """Use "praat" to extract intensity contour, bandwidth determines
    smoothing (windowsize I presume)...
    """

    wavfilelocation = os.path.abspath(wavfilelocation)
    parms = {'timestep' : timestep,
             'smoothingbandwidth': smoothingbandwidth}

    #write temp file - Praat script
    tempfh = NamedTemporaryFile()
    tempfh.write(PRAAT_GET_INTENSITY % parms)
    tempfh.flush()

    p = subprocess.Popen([PRAAT_BIN,
                          tempfh.name,
                          wavfilelocation],
                         stdout=subprocess.PIPE)
    stdout_text = p.communicate()[0]
    tempfh.close()

    lines = stdout_text.splitlines()

    starttime = float(lines[0])
    endtime = float(lines[1])
    timestep = float(lines[2])
    times = []
    values = []
    for line in lines[3:]:
        try:
            time, value = line.split()
        except ValueError:
            continue
        try:
            values.append(float(value))
        except ValueError:
            values.append(0.0)
        times.append(float(time))

    track.times = np.array(times)
    track.values = np.array(values).reshape(-1, 1)
    track.praattype = "IntensityTier"
    track._starttime = starttime
    track._endtime = endtime
    track.name = ".".join(os.path.basename(wavfilelocation).split(".")[:-1])


def trim_zeros(track, front=True, back=True):
    if front:
        values = np.trim_zeros(track.values, trim="f")
        times = track.times[len(track) - len(values):]
    else:
        values = track.values
        times = track.times
    if back:
        vallen = len(values)
        values = np.trim_zeros(values, trim="b")
        if vallen != len(values):
            times = times[:len(values) - vallen]

    track.values = values
    track.times = times



def _calc_ispline(track, ignore_zeros=False):
    """ 1-d cubic spline from track...
    """
    if ignore_zeros:
        validindices = np.nonzero(track.values)
        track._ispline_nonzero = InterpolatedUnivariateSpline(track.times[validindices[0]], track.values[validindices])
    else:
        track._ispline = InterpolatedUnivariateSpline(track.times, track.values)


def newtrack_from_ispline(track, times, ignore_zeros=False):
    try:
        if ignore_zeros:
            spline = track._ispline_nonzero
        else:
            spline = track._ispline
    except AttributeError:
        track._calc_ispline(ignore_zeros)
        if ignore_zeros:
            spline = track._ispline_nonzero
        else:
            spline = track._ispline

    t = Track()
    t.times = np.array(times)
    t.values = spline(t.times).reshape(-1, 1)
    return t


def _calc_sspline(track, s, ignore_zeros=False):
    """ 1-d cubic smoothing spline from track...
    """
    if ignore_zeros:
        validindices = np.nonzero(track.values)
        track._sspline_nonzero = UnivariateSpline(track.times[validindices[0]], track.values[validindices], s=s)
    else:
        track._sspline = UnivariateSpline(track.times, track.values, s=s)


def newtrack_from_sspline(track, times, s=500, ignore_zeros=False):
    try:
        if ignore_zeros:
            spline = track._sspline_nonzero
        else:
            spline = track._sspline
    except AttributeError:
        track._calc_sspline(s, ignore_zeros)
        if ignore_zeros:
            spline = track._sspline_nonzero
        else:
            spline = track._sspline

    t = Track()
    t.times = np.array(times)
    t.values = spline(t.times).reshape(-1, 1)
    return t

# def resample_n_1dspline(self, numsamples):
#     """ returns a track representing 'self' with numsamples
#         equally spaced, using 1dspline interpolation...
#     """
#     t = Track()
#     t.name = self.name
#     try:
#         t.starttime = self.starttime
#         t.endtime = self.endtime
#     except AttributeError:
#         t.starttime = self.times[0]
#         t.endtime = self.times[-1]
#     t.times = np.linspace(t.starttime, t.endtime, numsamples)
#     values = []
#     for time in t.times:
#         values.append(self.get_sample_at_inter1dspline(time))
#     t.values = np.array(values).reshape((-1, 1))
#     return t

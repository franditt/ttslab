#!/bin/env python
"""
    Reads and writes to and from HTK format feature files...
"""

__author__      = "Daniel van Niekerk (dvniekerk@csir.co.za)"
__date__        = "2009/01/30 14:13:00"


import os
import sys
import struct
import subprocess
import random

import numpy as N
from math import floor, ceil


def parse_path(fullpath):
    """ Parses "fullpath" to "dirname", "filename", "basename" and "extname"
    """

    dirname = os.path.dirname(fullpath)
    filename = os.path.basename(fullpath)
    
    namelist = filename.split(".")
    if len(namelist) == 1:
        return dirname, filename, namelist[0], ""
    
    basename = ".".join(namelist[:-1])
    extname = namelist[-1]
    
    return dirname, filename, basename, extname


def float_to_htk_int(value):
    """ Converts a floating point value (time in seconds) to an integer
        (time in 100ns units)...
    """
    return int(round(float(value)*10000000))

def htk_int_to_float(value):
    """ Converts an integer value (time in 100ns units) to floating
        point value (time in seconds)...
    """
    return float(value) / 10000000.0


class SuperVecExtractError(Exception):
    pass


class HTKFeatureFile(object):
    """ This class manages the reading and writing (and editing) of
        HTK format feature files (eg. mfc files)
        
        Notes:
                     Endianness: Big endian
                     Number of samples seem to be incorrectly reported in header
                     when CK qualifiers present...

        Limitations:
                     Only uncompressed files without CRC information 
                     containing 4byte float sequences for observation
                     vectors are handled
    """

    #FILE TYPE CLASS CONSTANTS...
    WAVEFORM  = (0, "WAVEFORM")
    LPC       = (1, "LPC")
    LPREFC    = (2, "LPREFC")
    LPCEPSTRA = (3, "LPCEPSTRA")
    LPDELCEP  = (4, "LPDELCEP")
    IREFC     = (5, "IREFC")
    MFCC      = (6, "MFCC")
    FBANK     = (7, "FBANK")
    MELSPEC   = (8, "MELSPEC")
    USER      = (9, "USER")
    DISCRETE  = (10, "DISCRETE")
    BASIC_KINDS = (WAVEFORM, LPC, LPREFC, LPCEPSTRA, LPDELCEP, IREFC, MFCC, FBANK, MELSPEC, USER, DISCRETE)
    _E = (int("000100", 8), "_E")
    _N = (int("000200", 8), "_N")
    _D = (int("000400", 8), "_D")
    _A = (int("001000", 8), "_A")
    _C = (int("002000", 8), "_C")
    _Z = (int("004000", 8), "_Z")
    _K = (int("010000", 8), "_K")
    _0 = (int("020000", 8), "_0")
    QUALIFIERS = (_E, _N, _D, _A, _C, _Z, _K, _0)
    UNSUPPORTED_QUALIFIERS = (_C, _K)

    BYTES_PER_VAL = 4  #Assumes 32bit floating point values in vectors....

    def __init__(self, filepath):
        """ Constructor loads file...
        """

        self.path = filepath
        self.name = parse_path(filepath)[2]
        
        self.nsamples, \
        self.sample_period, \
        self.sample_size, \
        self.parm_kind = self._readheader()
        self.parm_kind_str = self._interpret_kind()

        #Check whether possible to do read:
        for quali in HTKFeatureFile.UNSUPPORTED_QUALIFIERS:
            if quali[1] in self.parm_kind_str:
                print "%s, qualifier unsupported" % (quali[1])
                self.display_headerinfo()
                sys.exit(1)

        self.observations = self._readvectors()
        if len(self.observations) != self.nsamples:
            print "WARNING: Missmatch between number samples read (%s) and header info (%s)...." % \
                  (len(self.observations), self.nsamples)
        self.nsamples = len(self.observations)
        self.dimensions = len(self.observations[0])   #Assuming all vectors are the same size

        #self.componentstats = self._stats_per_component()
        

    def _readheader(self):
        """ Read file header information...
        """
        fh = open(self.path, "rb")
        header = fh.read(12)
        fh.close()

        nsamples, speriod, ssize, pkind  = struct.unpack(">IIHH", header)

        return nsamples, speriod, ssize, pkind

    def _interpret_kind(self):
        """ Interpret kind string...
        """
        basicmask = int("0000000000111111", 2)

        kindstring = ""
        
        for bkind in HTKFeatureFile.BASIC_KINDS:
            if (self.parm_kind & basicmask) == bkind[0]:
                kindstring += bkind[1]

        for quali in HTKFeatureFile.QUALIFIERS:
            if (self.parm_kind & quali[0]):
                kindstring += quali[1]

        return kindstring


    def _readvectors(self):
        """ Reads all observation vectors into a list...
            Assumes 32bit floats....
        """
        fmt = ">" + "f" * (self.sample_size / HTKFeatureFile.BYTES_PER_VAL)

        fh = open(self.path, "rb")
        fh.seek(12 + 0*self.sample_size)

        observations = []

        for i in range(0, self.nsamples):
            rawvector = fh.read(self.sample_size)
            if len(rawvector) != self.sample_size:
                print "Unexpected end of file...."
                sys.exit(1)
            vector = struct.unpack(fmt, rawvector)
            observations.append(list(vector))

        fh.close()

        return observations

    def _stats_per_component(self):
        """ Display some stats per component...
            Assume each vector is complete...
        """

        componentstats = []

        for i in range(self.dimensions):
            templist = []
            for obs in self.observations:
                templist.append(obs[i])
            templist = N.array(templist)
            stats = {}
            stats.update({"mean": templist.mean()})
            stats.update({"std": templist.std()})
            stats.update({"min": templist.min()})
            stats.update({"max": templist.max()})
            stats.update({"range": stats["max"] - stats["min"]})
            componentstats.append(stats)
        
        return componentstats


    def central_times(self, windowsize):
        """ Given the windowsize (HTK format), return the central
            locations in time of each sample...
        """
        
        firstpoint = windowsize / 2
        return N.arange(firstpoint, firstpoint + (self.nsamples * self.sample_period), self.sample_period)


    def append_observations(self, observations):
        """ Takes a list of observations and appends to current
            feature set...

            This is not really useful when one views the feature
            set as a series of observations over time but can
            be useful when building simply a collection of
            observations of one particular type (e.g. phonetype)
        """
        
        for obs in observations:
            assert len(obs) == self.dimensions, "Dimensionality missmatch..."
            for value in obs:
                assert isinstance(value, float), "Value is not a float..."

        self.observations.extend(observations)
        self.nsamples = len(self.observations)
    

    def append_component(self, component):
        """ Takes a list of floating point values (time series)
            and appends each value to existing vectors...

            This is useful when one wants to add a feature
            that is calculate at the same time instants as
            existing points...
        """

        assert len(component) == self.nsamples, "Num samples missmatch..."
        for value in component:
            assert isinstance(value, float), "Value is not a float..."

        for i in range(self.nsamples):
            self.observations[i].append(component[i])

        
        self.sample_size += HTKFeatureFile.BYTES_PER_VAL
        self.parm_kind = 9
        self.parm_kind_str = self._interpret_kind()
        self.dimensions = len(self.observations[0])


    def remove_component(self, index=-1):
        """ Takes an index, removing this component from all
            observation vectors...
        """

        assert (index in range(len(self.observations[0]))) or (index == -1), "Invalid index value..."
        assert len(range(len(self.observations[0]))) > 0, "No observations left..."

        for obs in self.observations:
            obs.pop(index)

        self.sample_size -= HTKFeatureFile.BYTES_PER_VAL
        self.parm_kind = 9
        self.parm_kind_str = self._interpret_kind()
        self.dimensions = len(self.observations[0])
        

    def display_headerinfo(self):
        """ Prints header info...
        """

        print "PATH:", self.path
        print "NAME:", self.name
        print "NUM SAMPLES:", self.nsamples
        print "SAMPLE PERIOD (100ns):", self.sample_period
        print "SAMPLE SIZE (bytes):", self.sample_size
        print "SAMPLE KIND:", self.parm_kind_str
    

    def display_observations(self):
        """ Prints values....
        """

        for i in range(len(self.observations)):
            print str(i).zfill(len(str(len(self.observations)))), ":"
            for val in self.observations[i]:
                sys.stdout.write("%.3f " % (val))
            sys.stdout.write("\n")


    def display_componentstats(self):
        """ Display self.componentstats...
        """

        counter = 0
        for c in self.componentstats:
            print counter, ":"
            print "MEAN:", c["mean"]
            print "STD:", c["std"]
            print "MIN:", c["min"]
            print "MAX:", c["max"]
            print "RANGE:", c["range"]
            counter += 1


    def write(self, outputpath):
        """ Write back to HTK format file...
        """
        
        if self.dimensions == 0:
            print "Isn't it silly to try and write an empty file...?"
            return

        fh = open(outputpath, "wb")
        
        # write header
        header = struct.pack(">IIHH", self.nsamples, self.sample_period, self.sample_size, self.parm_kind)
        fh.write(header)
        
        #write observations
        for obs in self.observations:
            obsstring = ""
            for value in obs:
                obsstring += struct.pack(">f", value)
            fh.write(obsstring)

        fh.close()


    def dump_values(self):
        """ Dump values to stdout, comma seperated floats,
            one vector per line...
        """
        for obs in self.observations:
            print ",".join([str(s) for s in obs])


def extractSuperVec(htkfeatfile, centralpoint, eff_numframes, eff_stepsize, windowsize):
    """Returns a supervector (see Labbook 2008-12-18) around
       'centralpoint' all parms in HTK format...
       Note: 'centralpoint' is floored based on sample_period...
    """

    assert eff_numframes % 2 != 0, "eff_numframes not odd!"

    realcentralpoint = centralpoint - (centralpoint % htkfeatfile.sample_period)
    
    extracttimes = N.arange(realcentralpoint - ((eff_numframes - 1) / 2) * eff_stepsize,
                            realcentralpoint + ((eff_numframes - 1) / 2) * eff_stepsize + eff_stepsize,
                            eff_stepsize)

    filetimes = htkfeatfile.central_times(windowsize)

    assert len(filetimes) == len(htkfeatfile.observations)

    indices = []
    for time in extracttimes:
        try:
            indices.append(filetimes.tolist().index(time))
        except ValueError:
            pass

    if len(indices) != len(extracttimes):
        raise SuperVecExtractError()

    supervector = []
    for obs_index in indices:
        try:
            supervector.extend(htkfeatfile.observations[obs_index])
        except IndexError:
            raise SuperVecExtractError("This should not be possible though....")

    return realcentralpoint, supervector


def extractObservationsInsideRange(htkfeatfile, starttime, endtime, windowsize):
    """Returns sequence of observations with: 
       starttime < centralpoints < endtime
       
    """

    filetimes = htkfeatfile.central_times(windowsize)

    assert len(filetimes) == len(htkfeatfile.observations)

    observations = [obs for ftime, obs in zip(filetimes, htkfeatfile.observations) if ftime > starttime and ftime < endtime]
    times = [ftime for ftime in filetimes if ftime > starttime and ftime < endtime]

    assert len(times) == len(observations)

    return times, observations   
    

def test(inputpath):
    """Tests HTKFeatureFile class functionality....
    """
    
    htkfeatfile = HTKFeatureFile(inputpath)
    #htkfeatfile.display_headerinfo()
    #htkfeatfile.display_observations()
    #htkfeatfile.display_componentstats()
    #htkfeatfile.plotstuff()
    htkfeatfile.dump_values()


if __name__ == "__main__":

    print "import HTKFeatureFile and use...."
    sys.exit(0)

    try:
        test(sys.argv[1])
    except IndexError:
        print "USAGE: htkparmfile2.py [InputFilePath]"

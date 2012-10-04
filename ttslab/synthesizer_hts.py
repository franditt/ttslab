# -*- coding: utf-8 -*-
""" Contains a synthesiser implementation relying on external
    hts_engine binary...

    In future wrap and use API directly?
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import os
import codecs
from tempfile import mkstemp
from collections import OrderedDict

from . uttprocessor import *
from . hts_labels import *
from . waveform import Waveform

class SynthesizerHTS(UttProcessor):
    """ Wraps the necessary methods to achieve synthesis by
        constructing a "full-context label" specification from
        synthesised Utterance and calling the hts_engine (API v 1.05)
        to synthesise from this given the trained model files.

        Utt Requirements:
                           ...
                           ...

        Provides:
                           ...
    """

    # -td tree       : decision tree files for state duration                  [  N/A]
    # -tm tree       : decision tree files for spectrum                        [  N/A]
    # -tf tree       : decision tree files for Log F0                          [  N/A]
    # -tl tree       : decision tree files for low-pass filter                 [  N/A]
    # -md pdf        : model files for state duration                          [  N/A]
    # -mm pdf        : model files for spectrum                                [  N/A]
    # -mf pdf        : model files for Log F0                                  [  N/A]
    # -ml pdf        : model files for low-pass filter                         [  N/A]
    # -dm win        : window files for calculation delta of spectrum          [  N/A]
    # -df win        : window files for calculation delta of Log F0            [  N/A]
    # -dl win        : window files for calculation delta of low-pass filter   [  N/A]
    # -od s          : filename of output label with duration                  [  N/A]
    # -om s          : filename of output spectrum                             [  N/A]
    # -of s          : filename of output Log F0                               [  N/A]
    # -ol s          : filename of output low-pass filter                      [  N/A]
    # -or s          : filename of output raw audio (generated speech)         [  N/A]
    # -ow s          : filename of output wav audio (generated speech)         [  N/A]
    # -ot s          : filename of output trace information                    [  N/A]
    # -qp s          : filename of input Log F0                                [  N/A]
    # -vp            : use phoneme alignment for duration                      [  N/A]
    # -i  i f1 .. fi : enable interpolation & specify number(i),coefficient(f) [    1][   1-- ]
    # -s  i          : sampling frequency                                      [16000][   1--48000]
    # -p  i          : frame period (point)                                    [   80][   1--]
    # -a  f          : all-pass constant                                       [ 0.42][ 0.0--1.0]
    # -g  i          : gamma = -1 / i (if i=0 then gamma=0)                    [    0][   0-- ]
    # -b  f          : postfiltering coefficient                               [  0.0][-0.8--0.8]
    # -l             : regard input as log gain and output linear one (LSP)    [  N/A]
    # -r  f          : speech speed rate                                       [  1.0][ 0.0--10.0]
    # -fm f          : add half-tone                                           [  0.0][-24.0--24.0]
    # -u  f          : voiced/unvoiced threshold                               [  0.5][ 0.0--1.0]
    # -em tree       : decision tree files for GV of spectrum                  [  N/A]
    # -ef tree       : decision tree files for GV of Log F0                    [  N/A]
    # -el tree       : decision tree files for GV of low-pass filter           [  N/A]
    # -cm pdf        : filenames of GV for spectrum                            [  N/A]
    # -cf pdf        : filenames of GV for Log F0                              [  N/A]
    # -cl pdf        : filenames of GV for low-pass filter                     [  N/A]
    # -jm f          : weight of GV for spectrum                               [  1.0][ 0.0--2.0]
    # -jf f          : weight of GV for Log F0                                 [  1.0][ 0.0--2.0]
    # -jl f          : weight of GV for low-pass filter                        [  1.0][ 0.0--2.0]
    # -k  tree       : GV switch                                               [  N/A]
    # -z  i          : audio buffer size                                       [ 1600][   0--48000]


    DEFAULT_PARMS = {"-td" : "%(models_dir)s/tree-dur.inf", 
                     "-tm" : "%(models_dir)s/tree-mgc.inf",
                     "-tf" : "%(models_dir)s/tree-lf0.inf",
                     "-tl" : None,
                     "-md" : "%(models_dir)s/dur.pdf",
                     "-mm" : "%(models_dir)s/mgc.pdf",
                     "-mf" : "%(models_dir)s/lf0.pdf",
                     "-ml" : None,
                     "-dm" : "%(models_dir)s/mgc.win1 -dm %(models_dir)s/mgc.win2 -dm %(models_dir)s/mgc.win3",
                     "-df" : "%(models_dir)s/lf0.win1 -df %(models_dir)s/lf0.win2 -df %(models_dir)s/lf0.win3",
                     "-dl" : None,
                     "-od" : "%(tempolab_file)s",
                     "-om" : None,
                     "-of" : None,
                     "-ol" : None,
                     "-or" : None,
                     "-ow" : "%(tempwav_file)s",
                     "-ot" : None,
                     "-qp" : None,
                     "-vp" : False,
                     "-i"  : None,
                     "-s"  : 16000,
                     "-p"  : 80,
                     "-a"  : 0.42,
                     "-g"  : 0,
                     "-b"  : 0.0,
                     "-l"  : True,
                     "-r"  : 1.0,
                     "-fm" : None,
                     "-u"  : None,
                     "-em" : "%(models_dir)s/tree-gv-mgc.inf",
                     "-ef" : "%(models_dir)s/tree-gv-lf0.inf",
                     "-el" : None,
                     "-cm" : "%(models_dir)s/gv-mgc.pdf",
                     "-cf" : "%(models_dir)s/gv-lf0.pdf",
                     "-cl" : None,
                     "-jm" : None,
                     "-jf" : None,
                     "-jl" : None,
                     "-k"  : "%(models_dir)s/gv-switch.inf",
                     "-z"  : None
                     }


    def __init__(self, voice, models_dir, hts_bin="hts_engine", engine_parms={}):
        UttProcessor.__init__(self, voice=voice)

        self.hts_bin = hts_bin
        self.models_dir = models_dir
        self.engine_parms = SynthesizerHTS.DEFAULT_PARMS.copy()
        self.engine_parms.update(engine_parms)

        self.processes = {"label_and_synth": OrderedDict([("hts_label", None),
                                                          ("hts_synth", None)]),
                          "label_only": OrderedDict([("hts_label", None)]),
                          "synth_only": OrderedDict([("hts_synth", None)])}



    def hts_label(self, utt, processname):
        lab = []

        starttime = 0
        for phone_item in utt.get_relation("Segment"):
            if "end" in phone_item:
                endtime = float_to_htk_int(phone_item["end"])
            else:
                endtime = None
            phlabel = [p(phone_item),
                       a(phone_item),
                       b(phone_item),
                       c(phone_item),
                       d(phone_item),
                       e(phone_item),
                       f(phone_item),
                       g(phone_item),
                       h(phone_item),
                       i(phone_item),
                       j(phone_item)]
            if endtime is not None:
                lab.append("%s %s " % (str(starttime).rjust(10), str(endtime).rjust(10)) + "/".join(phlabel))
            else:
                lab.append("/".join(phlabel))
            starttime = endtime

        utt["hts_label"] = lab
        return utt


    def hts_synth(self, utt, processname):

        htsparms = self.engine_parms.copy()
        if "htsparms" in utt:
            htsparms.update(utt["htsparms"])   #parm overrides for this utt...

        #build command string and execute:
        cmds = self.hts_bin
        for k in htsparms:
            if htsparms[k]:
                if htsparms[k] is True:
                    cmds += " " + k
                else:
                    cmds += " " + k + " " + str(htsparms[k])
        cmds += " %(tempilab_file)s"

        fd1, tempwav_file = mkstemp(prefix="pytts_", suffix=".wav")
        fd2, tempilab_file = mkstemp(prefix="pytts_")
        fd3, tempolab_file = mkstemp(prefix="pytts_")

        cmds = cmds % {'models_dir': self.models_dir,
                       'tempwav_file': tempwav_file,
                       'tempilab_file': tempilab_file,
                       'tempolab_file': tempolab_file}
        #print(cmds)
        with codecs.open(tempilab_file, "w", encoding="utf-8") as outfh:
            outfh.write("\n".join(utt["hts_label"]))

        os.system(cmds)

        #load seg endtimes into utt:
        with open(tempolab_file) as infh:
            lines = infh.readlines()
            segs = utt.get_relation("Segment").as_list()
            assert len(segs) == len(lines)
            for line, seg in zip(lines, segs):
                seg["end"] = htk_int_to_float(line.split()[1])

        #load audio:
        utt["waveform"] = Waveform(tempwav_file)

        #cleanup tempfiles:
        os.close(fd1)
        os.close(fd2)
        os.close(fd3)
        os.remove(tempwav_file)
        os.remove(tempolab_file)
        os.remove(tempilab_file)

        return utt

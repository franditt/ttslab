# -*- coding: utf-8 -*-
""" An utterance processor implements an independent module that can
    be used during synthesis. This leaves two mechanisms whereby a
    voice can manipulate an utterance: methods of the voice itsself or
    utterance processors.
"""
from __future__ import unicode_literals, division, print_function #Py2

from collections import OrderedDict

class ProcessNotDefined(Exception):
    pass

class UttProcessorError(Exception):
    pass

class UttProcessor(object):
    """ This is the base UttProcessor class.. An UttProcessor is
        instantiated at voice instantiation time and subsequently used
        to apply a process (which might be one or a number of methods
        of the object).
    """
    def __init__(self, voice):

        self.voice = voice
        #this should hold process name (e.g. 'text-to-words' or
        #'text-to-wave') with ordered dict of methodnames to be executed in
        #order each time passed the value as processname parameter...
        self.processes = {"default": OrderedDict([("methodname", "processname"),
                                                  ("methodname2", "processname2")])}
        

    def __call__(self, utt, processname):
        """ Apply the pipeline of methods associated with processname
            and return the resulting Utterance...
        """
        if processname in self.processes:
            for procname in self.processes[processname]:
                proc = getattr(self, procname)
                utt = proc(utt, self.processes[processname][procname])
        else:
            raise ProcessNotDefined(processname)

        return utt


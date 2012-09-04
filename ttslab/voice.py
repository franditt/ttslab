# -*- coding: utf-8 -*-
""" This is the abstract Voice class.. The idea is that the whole
    synthesis process is defined within this structure with different
    implementations (for instance for synthesis techniques or language
    specific routines) be derived from this as needed..

    A Voice instance is itsself an UttProcessor and will typically
    contain UttProcessors...

    A Voice instance should stay constant during synthesis and be
    instantiated by loading all the required data.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

from hrg import *
from uttprocessor import *

class Voice(UttProcessor):
    """ Abstract voice class
    """
    def __init__(self):
        UttProcessor.__init__(self, voice=None)

        self.features = {}
    
    def __getitem__(self, featname):
        """ Returns the requested feature from self.features
            This raises KeyError when featname is not available..
        """
        return self.features[featname]
    
    def __setitem__(self, featname, feat):
        """ Sets the specific feature in self.features
        """
        self.features[featname] = feat

    def __delitem__(self, featname):
        """ Deletes the specific feature in self.features
        """
        del self.features[featname]
    
    def __iter__(self):
        """ Iterate over features.
        """
        return self.features.__iter__()

    def __contains__(self, featname):
        """ Contains feature?
        """
        return featname in self.features

    def create_utterance(self):
        """ Create Utterance owned by this Voice...
        """
        return Utterance(self)

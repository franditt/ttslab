# -*- coding: utf-8 -*-
""" This is the abstract Phoneset class...
    Assuming one generally wants to iterate over "phones" and not
    features of the phoneset... etc
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

class Phoneset(object):
    """ Abstract phoneset class
    """
    def __init__(self):
        
        self.features = {}
        self.phones = {}

    def __getitem__(self, phonename):
        """ Returns the requested phone from self.phones
            This raises KeyError when phonename is not available..
        """
        return self.phones[phonename]
    
    def __setitem__(self, phonename, feats):
        """ Sets the specific features in self.phones
        """
        self.phones[phonename] = feats

    def __delitem__(self, phonename):
        """ Deletes the specific features in self.phones
        """
        del self.phones[phonename]

    def __iter__(self):
        """ Iterate over phones...
        """
        return self.phones.__iter__()

    def __contains__(self, phonename):
        """ Contains phone?
        """
        return phonename in self.phones

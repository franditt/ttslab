# -*- coding: utf-8 -*-
""" Functions to create HTS labels for synthesis...
    See: lab_format.pdf in reference HTS training scripts...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

from . hts_labels import *

def k(segitem):
    try:
        k0 = segitem.traverse("R:SylStructure.parent.F:tone")
    except hrg.TraversalError:
        k0 = NONE_STRING
    return "K:%s" % k0

def l(segitem):
    try:
        l0 = segitem.traverse("R:SylStructure.parent.R:Syllable.p.F:tone")
    except hrg.TraversalError:
        l0 = NONE_STRING
    return "L:%s" % l0

def m(segitem):
    try:
        m0 = segitem.traverse("R:SylStructure.parent.R:Syllable.p.p.F:tone")
    except hrg.TraversalError:
        m0 = NONE_STRING
    return "M:%s" % m0

def n(segitem):
    try:
        n0 = segitem.traverse("R:SylStructure.parent.R:Syllable.n.F:tone")
    except hrg.TraversalError:
        n0 = NONE_STRING
    return "N:%s" % n0

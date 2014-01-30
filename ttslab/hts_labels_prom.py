# -*- coding: utf-8 -*-
""" Functions to create HTS labels for synthesis...
    See: lab_format.pdf in reference HTS training scripts...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

from . hts_labels import *

def b(segitem):
    
    try:
        b1 = segitem.traverse("R:SylStructure.parent.F:stress")
    except hrg.TraversalError:
        b1 = 0
    try:
        b2 = segitem.traverse("R:SylStructure.parent.parent.F:prom")
    except hrg.TraversalError:
        b2 = 0
    try:
        b3 = segitem.traverse("R:SylStructure.parent.M:num_daughters()")
    except hrg.TraversalError:
        b3 = 0
    try:
        b4 = segitem.traverse("R:SylStructure.parent.M:sylpos_inword_f()")
    except hrg.TraversalError:
        b4 = 0
    try:
        b5 = segitem.traverse("R:SylStructure.parent.M:sylpos_inword_b()")
    except hrg.TraversalError:
        b5 = 0
    try:
        b6 = segitem.traverse("R:SylStructure.parent.M:sylpos_inphrase_f()")
    except hrg.TraversalError:
        b6 = 0
    try:
        b7 = segitem.traverse("R:SylStructure.parent.M:sylpos_inphrase_b()")
    except hrg.TraversalError:
        b7 = 0
    try:
        b8 = segitem.traverse("R:SylStructure.parent.M:numsylsbeforesyl_inphrase('stress', '1')")
    except hrg.TraversalError:
        b8 = 0
    try:
        b9 = segitem.traverse("R:SylStructure.parent.M:numsylsaftersyl_inphrase('stress', '1')")
    except hrg.TraversalError:
        b9 = 0
    try:
        b10 = segitem.traverse("R:SylStructure.parent.M:numsylsbeforesyl_inphrase('accent', '1')")
    except hrg.TraversalError:
        b10 = 0
    try:
        b11 = segitem.traverse("R:SylStructure.parent.M:numsylsaftersyl_inphrase('accent', '1')")
    except hrg.TraversalError:
        b11 = 0
    try:
        b12 = segitem.traverse("R:SylStructure.parent.M:syldistprev('stress', '1')")
    except hrg.TraversalError:
        b12 = 0
    try:
        b13 = segitem.traverse("R:SylStructure.parent.M:syldistnext('stress', '1')")
    except hrg.TraversalError:
        b13 = 0
    try:
        b14 = segitem.traverse("R:SylStructure.parent.M:syldistprev('accent', '1')")
    except hrg.TraversalError:
        b14 = 0
    try:
        b15 = segitem.traverse("R:SylStructure.parent.M:syldistnext('accent', '1')")
    except hrg.TraversalError:
        b15 = 0

    vowelname = NONE_STRING
    if segitem is not None:
        voice = segitem.relation.utterance.voice
        try:
            vowelnames = [ph for ph in voice.phones if "vowel" in voice.phones[ph]]
            for phname in [ph["name"] for ph in segitem.traverse("R:SylStructure.parent.M:get_daughters()")]:
                if phname in vowelnames:
                    vowelname = voice.phonemap[phname]
                    break
            if vowelname is None: vowelname = NONE_STRING
        except hrg.TraversalError:
            vowelname = NONE_STRING
    b16 = vowelname
    
    return "B:%s-%s-%s@%s-%s&%s-%s#%s-%s$%s-%s!%s-%s;%s-%s|%s" % tuple(map(zero, (b1, b2, b3, b4,
                                                                                  b5, b6, b7, b8,
                                                                                  b9, b10, b11, b12,
                                                                                  b13, b14, b15, b16)))

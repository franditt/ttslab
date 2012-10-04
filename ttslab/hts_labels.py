# -*- coding: utf-8 -*-
""" Functions to create HTS labels for synthesis...
    See: lab_format.pdf in reference HTS training scripts...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import ttslab
import ttslab.hrg as hrg
ttslab.extend(hrg.Item, "ttslab.funcs.ifuncs_hts")

NONE_STRING = "xxx"


def float_to_htk_int(string):
    """ Converts a string representing a floating point number to an
        integer (time in 100ns units)...
    """
    try:
        return int(round(float(string)*10000000))
    except:
        print(string)
        raise

def htk_int_to_float(string):
    """ Converts a string representing an integer (time in 100ns units)
        to floating point value (time in seconds)...
    """
    return float(string) / 10000000.0

def nonestring(s):
    if s is None:
        return NONE_STRING
    return s

def zero(s):
    if s is None:
        return 0
    return s

def p(segitem):
    
    segitem = segitem.get_item_in_relation("Segment")
    voice = segitem.relation.utterance.voice

    try:
        p1 = voice.phonemap[segitem.traverse("p.p.F:name")]
    except hrg.TraversalError:
        p1 = NONE_STRING
    try:
        p2 = voice.phonemap[segitem.traverse("p.F:name")]
    except hrg.TraversalError:
        p2 = NONE_STRING

    #here we allow for symbols to be overridden based on "hts_symbol":
    if "hts_symbol" in segitem:
        p3 = segitem["hts_symbol"]
    else:
        p3 = voice.phonemap[segitem["name"]]

    try:
        p4 = voice.phonemap[segitem.traverse("n.F:name")]
    except hrg.TraversalError:
        p4 = NONE_STRING
    try:
        p5 = voice.phonemap[segitem.traverse("n.n.F:name")]
    except hrg.TraversalError:
        p5 = NONE_STRING
    p6 = segitem.segpos_insyl_f()
    p7 = segitem.segpos_insyl_b()


    return "%s^%s-%s+%s=%s@%s_%s" % tuple(map(nonestring, (p1, p2, p3, p4, p5, p6, p7)))


def a(segitem):

    try:
        a1 = segitem.traverse("R:SylStructure.parent.R:Syllable.p.R:SylStructure.F:stress")
    except hrg.TraversalError:
        a1 = 0
    try:
        a2 = segitem.traverse("R:SylStructure.parent.R:Syllable.p.R:SylStructure.F:accent")
    except hrg.TraversalError:
        a2 = 0
    try:
        a3 = segitem.traverse("R:SylStructure.parent.R:Syllable.p.R:SylStructure.M:num_daughters()")
    except hrg.TraversalError:
        a3 = 0
    
    return "A:%s_%s_%s" % tuple(map(zero, (a1, a2, a3)))


def b(segitem):
    
    try:
        b1 = segitem.traverse("R:SylStructure.parent.F:stress")
    except hrg.TraversalError:
        b1 = 0
    try:
        b2 = segitem.traverse("R:SylStructure.parent.F:accent")
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


def c(segitem):

    try:
        c1 = segitem.traverse("R:SylStructure.parent.R:Syllable.n.R:SylStructure.F:stress")
    except hrg.TraversalError:
        c1 = 0
    try:
        c2 = segitem.traverse("R:SylStructure.parent.R:Syllable.n.R:SylStructure.F:accent")
    except hrg.TraversalError:
        c2 = 0
    try:
        c3 = segitem.traverse("R:SylStructure.parent.R:Syllable.n.R:SylStructure.M:num_daughters()")
    except hrg.TraversalError:
        c3 = 0
    
    return "C:%s+%s+%s" % tuple(map(zero, (c1, c2, c3)))

    

def d(segitem):

    try:
        d1 = segitem.traverse("R:SylStructure.parent.parent.p.F:gpos")
        if d1 is None: d1 = NONE_STRING
    except hrg.TraversalError:
        d1 = NONE_STRING
    try:
        d2 = segitem.traverse("R:SylStructure.parent.parent.p.M:num_daughters()")
        if d2 is None: d2 = 0
    except hrg.TraversalError:
        d2 = 0
    
    return "D:%s_%s" % (d1, d2)


def e(segitem):

    try:
        e1 = segitem.traverse("R:SylStructure.parent.parent.F:gpos")
        if e1 is None: e1 = NONE_STRING
    except hrg.TraversalError:
        e1 = NONE_STRING
    try:
        e2 = segitem.traverse("R:SylStructure.parent.parent.M:num_daughters()")
    except hrg.TraversalError:
        e2 = 0
    try:
        e3 = segitem.traverse("R:SylStructure.parent.parent.M:wordpos_inphrase_f()")
    except hrg.TraversalError:
        e3 = 0
    try:
        e4 = segitem.traverse("R:SylStructure.parent.parent.M:wordpos_inphrase_b()")
    except hrg.TraversalError:
        e4 = 0    
    try:
        e5 = segitem.traverse("R:SylStructure.parent.parent.M:numwordsbeforeword_inphrase('content', '1')")
    except hrg.TraversalError:
        e5 = 0
    try:
        e6 = segitem.traverse("R:SylStructure.parent.parent.M:numwordssafterword_inphrase('content', '1')")
    except hrg.TraversalError:
        e6 = 0
    try:
        e7 = segitem.traverse("R:SylStructure.parent.parent.M:worddistprev('content', '1')")
    except hrg.TraversalError:
        e7 = 0
    try:
        e8 = segitem.traverse("R:SylStructure.parent.parent.M:worddistnext('content', '1')")
    except hrg.TraversalError:
        e8 = 0
    
    return "E:%s+%s@%s+%s&%s+%s#%s+%s" % tuple(map(zero, (e1, e2, e3, e4, e5, e6, e7, e8)))


def f(segitem):

    try:
        f1 = segitem.traverse("R:SylStructure.parent.parent.n.F:gpos")
        if f1 is None: f1 = NONE_STRING
    except hrg.TraversalError:
        f1 = NONE_STRING
    try:
        f2 = segitem.traverse("R:SylStructure.parent.parent.n.M:num_daughters()")
        if f2 is None: f2 = 0
    except hrg.TraversalError:
        f2 = 0
    
    return "F:%s_%s" % (f1, f2)


def g(segitem):

    try:
        g1 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.p.M:numsyls_inphrase()")
    except hrg.TraversalError:
        g1 = 0
    try:
        g2 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.p.M:num_daughters()")
    except hrg.TraversalError:
        g2 = 0

    return "G:%s_%s" % tuple(map(zero, (g1, g2)))


def h(segitem):

    try:
        h1 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.M:numsyls_inphrase()")
    except hrg.TraversalError:
        h1 = 0
    try:
        h2 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.M:num_daughters()")
    except hrg.TraversalError:
        h2 = 0
    try:
        h3 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.M:phrasepos_inutt_f()")
    except hrg.TraversalError:
        h3 = 0
    try:
        h4 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.M:phrasepos_inutt_b()")
    except hrg.TraversalError:
        h4 = 0
    try:
        h5 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.F:tobi")
        if h5 is None: h5 = NONE_STRING
    except hrg.TraversalError:
        h5 = NONE_STRING

    return "H:%s=%s@%s=%s|%s" % tuple(map(zero, (h1, h2, h3, h4, h5)))


def i(segitem):

    try:
        i1 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.n.M:numsyls_inphrase()")
    except hrg.TraversalError:
        i1 = 0
    try:
        i2 = segitem.traverse("R:SylStructure.parent.parent.R:Phrase.parent.n.M:num_daughters()")
    except hrg.TraversalError:
        i2 = 0

    return "I:%s_%s" % tuple(map(zero, (i1, i2)))


def j(segitem):
    
    utt = segitem.relation.utterance
    
    j1 = len(utt.get_relation("Syllable"))
    j2 = len(utt.get_relation("Word"))
    j3 = len(utt.get_relation("Phrase"))

    return "J:%s+%s-%s" % (j1, j2, j3)

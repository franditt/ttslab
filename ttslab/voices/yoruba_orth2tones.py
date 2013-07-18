# -*- coding: utf-8 -*-
""" Determine tones from Yoruba orthography...
"""
from __future__ import unicode_literals, division, print_function #Py2

import sys
import unicodedata

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

BASECHARS = "abcdefghijklmnopqrstuvwxyz"
VOWELS = "aeiou"
NASALS = "mn"
CGRAVE = "\u0300"
CACUTE = "\u0301"
CUNDOT = "\u0323"

def tonelabel(word, i):
    """ Dependent on NFD ordering of combining characters!
    """
    try:
        cnext = word[i+1]
    except IndexError:
        return "M"
    if cnext == CUNDOT:
        try:
            cnext = word[i+2]
        except IndexError:
            return "M"
    #we now have the relevant cnext:
    if cnext == CGRAVE:
        return "L"
    elif cnext == CACUTE:
        return "H"
    else:
        return "M"

def nextbasechar(word, i):
    try:
        bc = word[i+1]
    except IndexError:
        return " "
    if bc not in BASECHARS:
        return nextbasechar(word, i+1)
    else:
        return bc, i+1

def prevbasechar(word, i):
    try:
        bc = word[i-1]
    except IndexError:
        return " ", i-1
    if bc not in BASECHARS:
        return prevbasechar(word, i-1)
    else:
        return bc, i-1

def syllabic(word, i):
    if word[i] in VOWELS:
        return True
    if word[i] == "n":
        pbc, pbci = prevbasechar(word, i)
        if pbc in "eo":
            if word[pbci+1] == CUNDOT:
                return False
        elif pbc in "aiu":
            return False
    if word[i] in NASALS and nextbasechar(word, i)[0] not in VOWELS:
        return True
    return False

def word2tones(word):
    tword = []
    for i in range(len(word)):
        syl = syllabic(word, i)
        if syl:
            tword.append(tonelabel(word, i))
    return "".join(tword)

if __name__ == "__main__":
    words = unicodedata.normalize("NFKD", " ".join(map(lambda x:unicode(x, encoding="utf-8"), sys.argv[1:]))).lower().split()
    for w in words:
        print(w, word2tones(w))

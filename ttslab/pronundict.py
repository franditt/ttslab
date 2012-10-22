# -*- coding: utf-8 -*-
""" Prototype implementation of a pronunciation dictionary.

    TODO:
         - Review entire implementation.
         - Raising KeyError vs returning None?
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import codecs
import copy

class PronunLookupError(Exception):
    def __init__(self, value):
        if value not in ["no_word", "no_pos"]:
            raise Exception
        self.value = value

class Word(object):
    def __init__(self, name, pronun, syltones=None, pos=None):
        """ NB: pronun with syls must be list of lists...
        """
        self.features = {}
        self["name"] = name     #standard word representation (same as in PronunciationDictionary.entries keys)
        if isinstance(pronun, list):
            self["syllables"] = pronun
            self["phones"] = [item for sublist in pronun for item in sublist]
        else:
            self["phones"] = pronun
        if syltones:
            if "syllables" in self:
                if len(syltones) != len(self["syllables"]):
                    print(self["name"])
                    print(syltones)
                    print(self["syllables"])
                    raise Exception("Word.__init__(): len(syltones) != len(syllables)")
            else:
                pass # if syllables not available, ignore test...
            self["syltones"] = syltones  #a string representing stress or tones of syllables
        if pos:
            self["pos"] = pos            #part-of-speech

    def __getitem__(self, featname):
        try:
            return self.features[featname]
        except KeyError:
            return None
    
    def __setitem__(self, featname, feat):
        self.features[featname] = feat

    def __delitem__(self, featname):
        del self.features[featname]
    
    def __iter__(self):
        return self.features.__iter__()

    def __contains__(self, featname):
        return featname in self.features


class PronunciationDictionary(object):
    """ Simple class to contain and provide relevant access to a
        pronunciation dictionary
    """

    def __init__(self):
        self.features = {} #for metadata
        self.entries = {}  #keys are canonical graphemic
                           #representation of words (ttslab convention:
                           #all lowercase) -> Word or [Word, Word, ...]


    def __getitem__(self, word):
        return self.entries[word]
    
    def __setitem__(self, word, entry):
        if word in self:
            try:
                self.entries[word].append(entry)
            except AttributeError:
                self.entries[word] = [self.entries[word], entry]
        else:
            self.entries[word] = entry

    def __delitem__(self, word):
        del self.entries[word]

    def __iter__(self):
        return self.entries.__iter__()

    def __contains__(self, word):
        return word in self.entries
        
    def _consistencycheck(self):
        """checks consistency of features in entries...
        """
        pass

    def totextfile(self, fn, phonemap=None):
        with codecs.open(fn, "w", encoding="utf-8") as outfh:
            for k in sorted(self):
                entry = self[k]
                if not isinstance(entry, list):
                    entry = [entry]
                for word in entry:
                    syllables = word["syllables"]
                    if syllables:
                        try:
                            for syl in syllables: assert len(syl) < 10
                        except AssertionError:
                            print(word["name"])
                            raise
                        syllables = "".join([str(len(syl)) for syl in syllables]) #assuming single digits
                    phones = word["phones"]
                    if phonemap:
                        phones = [phonemap[ph] for ph in phones]
                    outfh.write(" ".join([word["name"], str(word["pos"]), word["syltones"], syllables, " ".join(phones)]) + "\n")

    def fromtextfile(self, fn, phonemap=None, nonestring="None"):
        """ abandon None 010 133 _ b a n d _ n
        """
        with codecs.open(fn, encoding="utf-8") as infh:
            for line in infh:
                elems = line.split()
                word = elems[0]
                if elems[1] != nonestring:
                    pos = elems[1]
                else:
                    pos = None
                if elems[2] != nonestring:
                    syltones = elems[2]
                else:
                    syltones = None
                if phonemap:
                    phones = [phonemap[ph] for ph in elems[4:]]
                else:
                    phones = elems[4:]
                syllables = []
                for s in elems[3]:
                    syllables.append(phones[:int(s)])
                    for i in range(int(s)):
                        phones.pop(0)
                self.add_word(word, syllables, syltones, pos)
        return self

    def _checkagainstphoneset(self):
        """check all dictionary entries are compatible with a specific
        phoneset...
        """
        raise NotImplementedError

    def add_word(self, word, pronun, syltones=None, pos=None):
        entry = Word(word, pronun, syltones, pos)
        self[word] = entry

    def lookup(self, word, pos=None):
        try:
            entry = self[word]
        except KeyError:
            raise PronunLookupError("no_word")
        if not isinstance(entry, list):
            entry = [entry]
        if not pos:
            return copy.deepcopy(entry[0]) #pos not important: return first word
        for word in entry:
            if pos == word["pos"]:
                return copy.deepcopy(word) #first matching word
        raise PronunLookupError("no_pos")

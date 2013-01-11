#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Example voice implementation...
    
    This demonstrates how one can implement a voice by defining
    pipelines of UttProcessors and/or simple methods..

    TODO:
        - Better exception handling
        - Improve phonetizer implementation. Current implementation
          first looks for a PronunciationDictionary object with
          back-off to a simple Python dictionary with words as key to
          a phone list for each entry.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import re
from collections import OrderedDict

import ttslab
from . g2p import G2P_Rewrites_Semicolon, GraphemeNotDefined, NoRuleFound
from . pronundict import PronunLookupError
from . voice import *
from . tokenizers import DefaultTokenizer
from . synthesizer_us import SynthesizerUS

class DefaultVoice(Voice):
    """ Creating this to implement some of the more generic
        functionality required by a Voice in terms of text
        processing.. Hopefully this will be useful enough for most
        languages to inherit from this...
    """
    PHRASING_PUNCTUATION = "!?.,:;"

    def __init__(self):
        #defines empty 'features' dict etc.:
        Voice.__init__(self)

        #define processes for this voice:
        self.processes = {"text-to-words": OrderedDict([("tokenizer", "default"),
                                                        ("normalizer", None),
                                                        ("phrasifier", None)]),
                          "text-to-segments": OrderedDict([("tokenizer", "default"),
                                                           ("normalizer", None),
                                                           ("phrasifier", None),
                                                           ("phonetizer", None),
                                                           ("pauses", None)])}
        
        #setup utterance processors for this voice:
        self.tokenizer = DefaultTokenizer(self)


        #STUBS: these are minimum data requirements for this voice
        #implementation:
        self.phoneset = None
        self.g2p = None
        self.pronundict = None
        self.pronunaddendum = None
    
    #################### Lower level methods...
    def normalizer(self, utt, processname):
        """ Perform "normalization" based on "Tokens" contained in
            Utterance...

            Crude stub... this will be overwritten with language and
            locale specific implementations...
        """
        token_rel = utt.get_relation("Token")
        word_rel = utt.new_relation("Word")
        for token_item in token_rel:
            tokentext = token_item["name"].lower() #lowercase token...
            tokentextlist = tokentext.split("-")   #split tokens on dashes to create multiple words...
            for wordname in tokentextlist:
                if "ﬁ" in wordname:                
                    #HACK: need to implement better mechanism to deal
                    #with ligatures etc.
                    wordname = re.sub("ﬁ", "fi", wordname)
                word_item = word_rel.append_item()
                word_item["name"] = wordname
                token_item.add_daughter(word_item)
        return utt

    def phrasifier(self, utt, processname):
        """ Determine phrases/phrase breaks in the utterance...
        """
        def anycharsin(s, stemplate):
            for c in s:
                if c in stemplate:
                    return True
            return False

        word_rel = utt.get_relation("Word")
        punctuation = self.PHRASING_PUNCTUATION
        phrase_rel = utt.new_relation("Phrase")
        phrase_item = phrase_rel.append_item()
        phrase_item["name"] = "BB"
        for word_item in word_rel:
            phrase_item.add_daughter(word_item)
            token_item = word_item.get_item_in_relation("Token").parent_item
            if word_item.get_item_in_relation("Token") is token_item.last_daughter:
                if "postpunc" in token_item:
                    postpunk = token_item["postpunc"] #postpunk! :-)
                    if word_item is not word_rel.tail_item and anycharsin(postpunk, punctuation):
                        phrase_item = phrase_rel.append_item()
                        phrase_item["name"] = "BB"
        return utt


    def phonetizer(self, utt, processname):
        """ Applies G2P and Syllabification from 'Word' relation...
            DEMITASSE: REWRITE!
        """
        word_rel = utt.get_relation("Word")
        syl_rel = utt.new_relation("Syllable")
        sylstruct_rel = utt.new_relation("SylStructure")
        seg_rel = utt.new_relation("Segment")
        for word_item in word_rel:
            try:
                if word_item["name"] in self.pronunaddendum: raise AttributeError # bad hack - need to rewrite phonetizer
                word = self.pronundict.lookup(word_item["name"], word_item["pos"]) #pos will be None if nonexistant
            except PronunLookupError as e:
                if e.value == "no_pos":
                    word = self.pronundict.lookup(word_item["name"])
                else:
                    word = None
            except AttributeError:
                word = None
            if word:
                if "syllables" in word:
                    syllables = word["syllables"]
                    syltones = word["syltones"]
                    if not syltones:
                        try:
                            syltones = self.phoneset.guess_sylstress(syllables)
                        except AttributeError:
                            syltones = "0" * len(syllables)
                else:
                    phones = word["phones"]
                    syllables = self.phoneset.syllabify(phones)
                    try:
                        syltones = self.phoneset.guess_sylstress(syllables)
                    except AttributeError:
                        syltones = "0" * len(syllables)
            else:
                try:
                    phones = self.pronunaddendum[word_item["name"]] #try addendum
                except KeyError:
                    try:
                        phones = self.pronundict[word_item["name"]] #try old-style dictionary...
                    except:
                        try:
                            phones = self.g2p.predict_word(word_item["name"])
                        except (GraphemeNotDefined, NoRuleFound):
                            print("WARNING: No pronunciation found for '%s'" % word_item["name"])
                            phones = [self.phoneset.features["silence_phone"]]
                syllables = self.phoneset.syllabify(phones)
                try:
                    syltones = self.phoneset.guess_sylstress(syllables)
                except AttributeError:
                    syltones = "0" * len(syllables)

            word_item_in_sylstruct = sylstruct_rel.append_item(word_item)
            for syl, syltone in zip(syllables, syltones):
                syl_item = syl_rel.append_item()
                syl_item["name"] = "syl"
                syl_item["stress"] = syltone #DEMITASSE: fix naming later
                syl_item_in_sylstruct = word_item_in_sylstruct.add_daughter(syl_item)
                
                for phone in syl:
                    seg_item = seg_rel.append_item()
                    seg_item["name"] = phone
                    seg_item_in_sylstruct = syl_item_in_sylstruct.add_daughter(seg_item)
        return utt


    def pauses(self, utt, processname):
        """ Insert pauses in the segment sequence where phrase breaks occur...
        """
        silphone = self.phoneset.features["silence_phone"]
        seg_rel = utt.get_relation("Segment")
        #add pause at start of utterance...
        first_seg = seg_rel.head_item
        pause_item = first_seg.prepend_item()
        pause_item["name"] = silphone
        ###

        phr_rel = utt.get_relation("Phrase")
        if phr_rel is None:
            print("\n".join([self.pauses,
                             "\nError: Utterance needs to have 'Phrase' relation..."]))
            return
        #add pauses at end of each phrase..
        for phr_item in phr_rel:
            try:
                last_seg = phr_item.last_daughter.get_item_in_relation("SylStructure").last_daughter.last_daughter.get_item_in_relation("Segment")
            except:
                print(utt)
                raise
            pause_item = last_seg.append_item()
            pause_item["name"] = silphone
        return utt
            

    #################### Higher level methods...
    def synthesize(self, inputstring, processname="text-to-segments"):
        """ Render the inputstring...
        """
        utt = self.create_utterance()
        utt["text"] = inputstring
        utt = self(utt, processname)
        return utt

    def resynthesize(self, utt, processname="utt-to-wave"):
        """ Apply synth pipeline to existing utt...
        """
        return self(utt, processname)


class LwaziVoice(DefaultVoice):
    """ Implementation of a basic voice with phoneset, pronundict and
        g2p rules...
    """
    def __init__(self, phoneset, g2p, pronundict, pronunaddendum):
        DefaultVoice.__init__(self)
        self.phoneset = phoneset
        self.g2p = g2p
        self.pronundict = pronundict
        self.pronunaddendum = pronunaddendum

        # We make these attributes of the voice directly as
        # multilingual voices have more than one phoneset and we need
        # to collect mappings and present a consistent interface.
        self.phonemap = self.phoneset.map
        self.phones = self.phoneset.phones




class LwaziUSVoice(LwaziVoice):
    """ Voice implementation using unit selection back-end...
    """
    def __init__(self, phoneset, g2p, pronundict, pronunaddendum, unitcatalogue):
        LwaziVoice.__init__(self,
                            phoneset=phoneset,
                            g2p=g2p,
                            pronundict=pronundict,
                            pronunaddendum=pronunaddendum)
        
        self.processes = {"text-to-words": OrderedDict([("tokenizer", "default"),
                                                        ("normalizer", None),
                                                        ("phrasifier", None)]),
                          "text-to-segments": OrderedDict([("tokenizer", "default"),
                                                           ("normalizer", None),
                                                           ("phrasifier", None),
                                                           ("phonetizer", None),
                                                           ("pauses", None)]),
                          "text-to-units": OrderedDict([("tokenizer", "default"),
                                                        ("normalizer", None),
                                                        ("phrasifier", None),
                                                        ("phonetizer", None),
                                                        ("pauses", None),
                                                        ("synthesizer", "targetunits")]),
                          "text-to-wave": OrderedDict([("tokenizer", "default"),
                                                       ("normalizer", None),
                                                       ("phrasifier", None),
                                                       ("phonetizer", None),
                                                       ("pauses", None),
                                                       ("synthesizer", "synth")])}
        self.synthesizer = SynthesizerUS(self, unitcatalogue=unitcatalogue)

    def say(self, inputstring):
        """ Render the inputstring...
        """
        utt = self.synthesize(inputstring, "text-to-wave")
        utt["waveform"].play()
        return utt



class LwaziHTSVoice(LwaziVoice):
    """ Wraps the necessary methods to achieve synthesis by
        constructing a "full-context label" specification from
        synthesised Utterance and calling the hts_engine to synthesise
        from this given the trained model files.
    """
    
    def __init__(self, phoneset, g2p, pronundict, pronunaddendum, synthesizer_hts):
        LwaziVoice.__init__(self,
                            phoneset=phoneset,
                            g2p=g2p,
                            pronundict=pronundict,
                            pronunaddendum=pronunaddendum)
        
        self.processes = {"text-to-words": OrderedDict([("tokenizer", "default"),
                                                        ("normalizer", "default"),
                                                        ("phrasifier", None)]),
                          "text-to-segments": OrderedDict([("tokenizer", "default"),
                                                           ("normalizer", "default"),
                                                           ("phrasifier", None),
                                                           ("phonetizer", None),
                                                           ("pauses", None)]),
                          "text-to-label": OrderedDict([("tokenizer", "default"),
                                                        ("normalizer", "default"),
                                                        ("phrasifier", None),
                                                        ("phonetizer", None),
                                                        ("pauses", None),
                                                        ("synthesizer", "label_only")]),
                          "text-to-wave": OrderedDict([("tokenizer", "default"),
                                                       ("normalizer", "default"),
                                                       ("phrasifier", None),
                                                       ("phonetizer", None),
                                                       ("pauses", None),
                                                       ("synthesizer", "label_and_synth")]),
                          "utt-to-wave": OrderedDict([("synthesizer", "label_and_synth")])}


        #setup uttprocessors:
        self.synthesizer = synthesizer_hts
        self.synthesizer.voice = self

    #################### Voice setup methods...

 

    #################### Lower level methods...
    


    #################### Higher level methods...
    def synthesize(self, inputstring, processname="text-to-segments", htsparms={}):
        """ Render the inputstring...
        """
        utt = self.create_utterance()
        utt["text"] = inputstring
        utt["htsparms"] = htsparms
        utt = self(utt, processname)
        return utt


    def resynthesize(self, utt, processname="utt-to-wave", htsparms=None):
        utt["htsparms"] = htsparms
        return self(utt, processname)


    def say(self, inputstring, htsparms={}):
        """ Render the inputstring...
        """
        utt = self.synthesize(inputstring, "text-to-wave", htsparms=htsparms)
        utt["waveform"].play()
        return utt


class LwaziMultiHTSVoice(LwaziHTSVoice):
    
    def __init__(self, phoneset, g2p, pronundict, pronunaddendum,
                 engphoneset, engg2p, engpronundict, engpronunaddendum,
                 synthesizer_hts):
        LwaziHTSVoice.__init__(self, phoneset=phoneset,
                               g2p=g2p,
                               pronundict=pronundict,
                               pronunaddendum=pronunaddendum,
                               synthesizer_hts=synthesizer_hts)
        
        self.engphoneset = engphoneset
        self.engg2p = engg2p
        self.engpronundict = engpronundict
        self.engpronunaddendum = engpronunaddendum

        self.phonemap = dict(self.phoneset.map)
        self.phonemap.update([("eng_" + k, "eng_" + v) for k, v in self.engphoneset.map.iteritems()])
        self.phones = dict(self.phoneset.phones)
        self.phones.update([("eng_" + k, v) for k, v in self.engphoneset.map.iteritems()])


    def normalizer(self, utt, processname):
        """ words marked with a prepended pipe character "|" will be
            marked as English...
        """
        token_rel = utt.get_relation("Token")
        word_rel = utt.new_relation("Word")
        for token_item in token_rel:
            tokentext = token_item["name"].lower()
            tokentextlist = tokentext.split("-")           #split tokens on dashes to create multiple words...
            for wordname in tokentextlist:
                if "ﬁ" in wordname:
                    wordname = re.sub("ﬁ", "fi", wordname) #HACK to handle common ligature
                word_item = word_rel.append_item()
                if wordname.startswith("|"):
                    word_item["lang"] = "eng"
                    wordname = wordname[1:]
                else:
                    word_item["lang"] = "def" #default language...
                word_item["name"] = wordname
                token_item.add_daughter(word_item)
        return utt


    def phonetizer(self, utt, processname):
        
        def g2p(word, phoneset, pronundict, pronunaddendum, g2p):
            syltones = None
            syllables = None
            if pronunaddendum and word["name"] in pronunaddendum:
                    phones = pronunaddendum[word["name"]]
                    syllables = phoneset.syllabify(phones)
            else:
                try:
                    wordpronun = pronundict.lookup(word["name"], word["pos"])
                except PronunLookupError as e:
                    if e.value == "no_pos":
                        wordpronun = self.pronundict.lookup(word_item["name"])
                    else:
                        wordpronun = None
                except AttributeError:
                    wordpronun = None
                if wordpronun:
                    if "syllables" in wordpronun:
                        syllables = wordpronun["syllables"]
                        syltones = wordpronun["syltones"] #None if doesn't exist
                    else:
                        phones = wordpronun["phones"]
                        syllables = phoneset.syllabify(phones)
                else:
                    try:
                        phones = pronundict[word["name"]]
                    except KeyError:
                        try:
                            phones = g2p.predict_word(word["name"])
                        except (GraphemeNotDefined, NoRuleFound):
                            print("WARNING: No pronunciation found for '%s'" % word["name"])
                            phones = [self.phoneset.features["silence_phone"]]
                    syllables = phoneset.syllabify(phones)
            if not syltones:
                try:
                    syltones = phoneset.guess_sylstress(syllables)
                except AttributeError:
                    syltones = "0" * len(syllables)
            return syllables, syltones

        word_rel = utt.get_relation("Word")
        syl_rel = utt.new_relation("Syllable")
        sylstruct_rel = utt.new_relation("SylStructure")
        seg_rel = utt.new_relation("Segment")
        for word_item in word_rel:
            if word_item["lang"] == "eng":
                syllables, syltones = g2p(word_item, self.engphoneset, self.engpronundict, self.engpronunaddendum, self.engg2p)
                #rename phones:
                for syl in syllables:
                    for i in range(len(syl)):
                        syl[i] = "eng_" + syl[i]
            else:
                syllables, syltones = g2p(word_item, self.phoneset, self.pronundict, self.pronunaddendum, self.g2p)

            word_item_in_sylstruct = sylstruct_rel.append_item(word_item)
            for syl, syltone in zip(syllables, syltones):
                syl_item = syl_rel.append_item()
                syl_item["name"] = "syl"
                syl_item["stress"] = syltone
                syl_item_in_sylstruct = word_item_in_sylstruct.add_daughter(syl_item)
                
                for phone in syl:
                    seg_item = seg_rel.append_item()
                    seg_item["name"] = phone
                    seg_item_in_sylstruct = syl_item_in_sylstruct.add_daughter(seg_item)
        return utt


if __name__ == "__main__":
    v = DefaultVoice()
    u = v.synthesize("Hoe sê mens dit in Afrikaans?", "text-to-words")
    print(u)

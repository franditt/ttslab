# -*- coding: utf-8 -*-
""" Initial phoneset implementation for the Yoruba voice...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys
import os
import re
import codecs
import unicodedata
import string
from tempfile import mkstemp

import numpy as np

from .. phoneset import Phoneset
from .. g2p import G2P_Rewrites_Semicolon, GraphemeNotDefined, NoRuleFound
from .. defaultvoice import LwaziMultiHTSVoice
import ttslab.hts_labels_tone as hts_labels_tone
from .. synthesizer_htsme import SynthesizerHTSME
from . yoruba_orth2tones import word2tones
from ttslab.waveform import Waveform
from ttslab.trackfile import Track
from .. pronundict import PronunLookupError


def anycharsin(s, stemplate):
    for c in s:
        if c in stemplate:
            return True
    return False


class YorubaPhoneset(Phoneset):
    """ Developed for PhD studies, based on Yoruba data received from
        Etienne Barnard...

        DEMITASSE: check again later when the phoneset/language is more familiar!
    """

    def __init__(self):
        Phoneset.__init__(self)

        self.features = {"name": "Yoruba Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "pau_cl"
                         }
        self.phones = {"pau"    : set(["pause"]),
                       "pau_cl" : set(["closure"]),
                       "ʔ"      : set(["glottal-stop"]),
                       #vowels
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "ã"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front", "articulation_nasalized"]),
                       "e"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɛ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɛ̃"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front", "articulation_nasalized"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "ĩ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front", "articulation_nasalized"]),
                       "o"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
#                       "õ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded", "articulation_nasalized"]), 
                       "ɔ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "ɔ̃"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded", "articulation_nasalized"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back"]),
                       "ũ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back", "articulation_nasalized"]),
                       #consonants
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "g"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "gb"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "place_bilabial", "voiced"]),
                       "h"      : set(["consonant", "manner_fricative", "place_glottal"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "dʒ"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "k"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar"]),
                       "l"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "m"      : set(["class_sonorant", "class_syllabic", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "n"      : set(["class_sonorant", "class_syllabic", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "kp"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "place_bilabial"]),
                       "r"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "ʃ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar"]),
                       "t"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"])
                       }
        self.map = {"pau"    : "pau",
                    "pau_cl" : "pau_cl",
                    "ʔ"      : "pau_gs",
                    "a"      : "a",
                    "ã"      : "an",
                    "e"      : "e",
                    "ɛ"      : "E",
                    "ɛ̃"      : "En",
                    "i"      : "i",
                    "ĩ"      : "in",
                    "o"      : "o",
#                    "õ"      : "on",
                    "ɔ"      : "O",
                    "ɔ̃"      : "On",
                    "u"      : "u",
                    "ũ"      : "un",
                    "b"      : "b",
                    "d"      : "d",
                    "dʒ"     : "dZ",
                    "f"      : "f",
                    "g"      : "g",
                    "gb"     : "gb",
                    "h"      : "h",
                    "j"      : "j",
                    "k"      : "k",
                    "kp"     : "kp",
                    "l"      : "l",
                    "m"      : "m",
                    "n"      : "n",
                    "r"      : "r",
                    "s"      : "s",
                    "t"      : "t",
                    "ʃ"      : "S",
                    "w"      : "w"
                    }

    def is_vowel(self, phonename):
        return "vowel" in self.phones[phonename]

    def is_consonant(self, phonename):
        return "consonant" in self.phones[phonename]

    def is_syllabicconsonant(self, phonename):
        return "class_syllabic" in self.phones[phonename] and "consonant" in self.phones[phonename]


    def syllabify(self, phonelist):
        """ Basic syllabification, based on the syllabification scheme
            devised by Etienne Barnard for isiZulu (Nguni language).
        """
        sylls = [[]]
        phlist = list(phonelist)
        while phlist:
            phone = phlist[0]
            try:
                nphone = phlist[1]
                nnphone = phlist[2]
                #Syllabic consonant followed by C:
                if (self.is_syllabicconsonant(phone) and
                    self.is_consonant(nphone)):
                    #sC.C
                    sylls[-1].append(phlist.pop(0))
                    if phlist: sylls.append([])
                    continue
                ##DEMITASSE: Yoruba doesn't seem to have these:
                ##########
                # #If there is a three phone cluster:
                # if (self.is_vowel(phone) and
                #     not self.is_vowel(nphone) and
                #     not self.is_vowel(nnphone)):
                #     #VC.C
                #     sylls[-1].append(phlist.pop(0))#phone
                #     sylls[-1].append(phlist.pop(0))#nphone
                #     if phlist: sylls.append([])
                #     continue
            except IndexError:
                pass
            if self.is_vowel(phone):
                #V.Any
                sylls[-1].append(phlist.pop(0))
                if phlist: sylls.append([])
                continue
            #anything not caught above is added to current syl...
            sylls[-1].append(phlist.pop(0))
        return sylls


class SynthesizerHTSME_Tone(SynthesizerHTSME):
    def hts_label(self, utt, processname):
        lab = []

        starttime = 0
        for phone_item in utt.get_relation("Segment"):
            if "end" in phone_item:
                endtime = hts_labels_tone.float_to_htk_int(phone_item["end"])
            else:
                endtime = None
            phlabel = [hts_labels_tone.p(phone_item),
                       hts_labels_tone.a(phone_item),
                       hts_labels_tone.b(phone_item),
                       hts_labels_tone.c(phone_item),
                       hts_labels_tone.d(phone_item),
                       hts_labels_tone.e(phone_item),
                       hts_labels_tone.f(phone_item),
                       hts_labels_tone.g(phone_item),
                       hts_labels_tone.h(phone_item),
                       hts_labels_tone.i(phone_item),
                       hts_labels_tone.j(phone_item),
                       hts_labels_tone.k(phone_item),
                       hts_labels_tone.l(phone_item),
                       hts_labels_tone.m(phone_item),]
            if endtime is not None:
                lab.append("%s %s " % (str(starttime).rjust(10), str(endtime).rjust(10)) + "/".join(phlabel))
            else:
                lab.append("/".join(phlabel))
            starttime = endtime

        utt["hts_label"] = lab
        return utt

    def hts_synth(self, utt, processname):
        htsparms = self.engine_parms.copy()
        htsparms["-of"] = "%(tempolf0_file)s"
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

        fd1, tempwav_file = mkstemp(prefix="ttslab_", suffix=".wav")
        fd2, tempilab_file = mkstemp(prefix="ttslab_")
        fd3, tempolab_file = mkstemp(prefix="ttslab_")
        fd4, tempolf0_file = mkstemp(prefix="ttslab_")

        cmds = cmds % {'models_dir': self.models_dir,
                       'tempwav_file': tempwav_file,
                       'tempilab_file': tempilab_file,
                       'tempolab_file': tempolab_file,
                       'tempolf0_file': tempolf0_file}
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
                seg["end"] = hts_labels_tone.htk_int_to_float(line.split()[1])

        #load audio:
        utt["waveform"] = Waveform(tempwav_file)

        #load lf0:
        f0 = np.exp(np.fromfile(tempolf0_file, "float32")) #load and lf0 to hertz
        #to semitones relative to 1Hz:
        f0[f0.nonzero()] = 12.0 * np.log2(f0[f0.nonzero()]) # 12 * log2 (F0 / F0reference) where F0reference = 1
        f0t = Track()
        f0t.values = f0
        f0t.times = np.arange(len(f0), dtype=np.float64) * 0.005
        utt["f0"] = f0t

        #cleanup tempfiles:
        os.close(fd1)
        os.close(fd2)
        os.close(fd3)
        os.close(fd4)
        os.remove(tempwav_file)
        os.remove(tempolab_file)
        os.remove(tempilab_file)
        os.remove(tempolf0_file)

        return utt

class SynthesizerHTSME_Tone2(SynthesizerHTSME_Tone):
    def hts_label(self, utt, processname):
        lab = []

        starttime = 0
        for phone_item in utt.get_relation("Segment"):
            if "end" in phone_item:
                endtime = hts_labels_tone.float_to_htk_int(phone_item["end"])
            else:
                endtime = None
            phlabel = [hts_labels_tone.p(phone_item),
                       hts_labels_tone.a(phone_item),
                       hts_labels_tone.b(phone_item),
                       hts_labels_tone.c(phone_item),
                       hts_labels_tone.d(phone_item),
                       hts_labels_tone.e(phone_item),
                       hts_labels_tone.f(phone_item),
                       hts_labels_tone.g(phone_item),
                       hts_labels_tone.h(phone_item),
                       hts_labels_tone.i(phone_item),
                       hts_labels_tone.j(phone_item),
                       hts_labels_tone.k(phone_item),
                       hts_labels_tone.l(phone_item),
                       hts_labels_tone.m(phone_item),
                       hts_labels_tone.n(phone_item)]
            if endtime is not None:
                lab.append("%s %s " % (str(starttime).rjust(10), str(endtime).rjust(10)) + "/".join(phlabel))
            else:
                lab.append("/".join(phlabel))
            starttime = endtime

        utt["hts_label"] = lab
        return utt

class SynthesizerHTSME_Tone_NoTone(SynthesizerHTSME_Tone): #no tone labels but loads generated f0
    def hts_label(self, utt, processname):
        lab = []

        starttime = 0
        for phone_item in utt.get_relation("Segment"):
            if "end" in phone_item:
                endtime = hts_labels_tone.float_to_htk_int(phone_item["end"])
            else:
                endtime = None
            phlabel = [hts_labels_tone.p(phone_item),
                       hts_labels_tone.a(phone_item),
                       hts_labels_tone.b(phone_item),
                       hts_labels_tone.c(phone_item),
                       hts_labels_tone.d(phone_item),
                       hts_labels_tone.e(phone_item),
                       hts_labels_tone.f(phone_item),
                       hts_labels_tone.g(phone_item),
                       hts_labels_tone.h(phone_item),
                       hts_labels_tone.i(phone_item),
                       hts_labels_tone.j(phone_item)]
            if endtime is not None:
                lab.append("%s %s " % (str(starttime).rjust(10), str(endtime).rjust(10)) + "/".join(phlabel))
            else:
                lab.append("/".join(phlabel))
            starttime = endtime

        utt["hts_label"] = lab
        return utt
    

class LwaziYorubaMultiHTSVoice(LwaziMultiHTSVoice):
    CONJUNCTIONS = ["ẹyin", "ati", # both,and
                    "sibẹ-sibẹ", "sibẹsibẹ", "afi", "ṣugbọn", #but
                    "fun", "nitori", "ni", "to", "ri", #for,because
                    "boya", "tabi", "yala", #either/or/nor
                    "pẹlu", "jubẹlọ", "bi", "o", "ti", "lẹ", "jẹ", "pe", #yet,although
                    "lati", "lẹhin", "igbati",  # since
                    "titi", #until
                    "akoko" #while
                    ] #Unicode NFC form
    CGRAVE = "\u0300"
    CACUTE = "\u0301"
    CUNDOT = "\u0323"
    DIACRITICS = [CGRAVE, CACUTE, CUNDOT]
    SMALLGRAPHSET = "abdeẹfghijklmnoọprsṣtuwy"
    ENGWORD_CHARTHRESHOLD = 4 #Only prefer entry in English lexicon for words longer (num chars) than this

    def __init__(self, phoneset, g2p, pronundict, pronunaddendum,
                 engphoneset, engg2p, engpronundict, engpronunaddendum,
                 synthesizer):
        LwaziMultiHTSVoice.__init__(self, phoneset=phoneset, g2p=g2p,
                                    pronundict=pronundict,
                                    pronunaddendum=pronunaddendum,
                                    engphoneset=engphoneset, engg2p=engg2p,
                                    engpronundict=engpronundict,
                                    engpronunaddendum=engpronunaddendum,
                                    synthesizer=synthesizer)

    def __is_allcaps(self, token):
        """ NOTE: single char tokens are never considered ALLCAPS
        """
        token = re.sub(u"[%s%s%s]" % (self.CGRAVE, self.CACUTE, self.CUNDOT), "", token)
        if len(token) > 1:
            return token == token.upper() and anycharsin(token, string.ascii_letters + self.SMALLGRAPHSET + self.SMALLGRAPHSET.upper())
        else:
            return False

    def normalizer(self, utt, processname):
        """ words marked with a prepended pipe character "|" or
            ALLCAPS or if characters in word are not part of standard
            Yoruba orthography and words in the English pronunciation
            dictionary or addendum will be marked as English...
        """
        token_rel = utt.get_relation("Token")
        word_rel = utt.new_relation("Word")
        for token_item in token_rel:
            tokentext = token_item["name"]
            tokentext = tokentext.lower()
            tokentextlist = tokentext.split("-")  #split tokens on dashes to create multiple words...revisit
            for wordname in tokentextlist:
                pronunform = unicodedata.normalize("NFC", re.sub(u"[%s%s]" % (self.CGRAVE, self.CACUTE), "", wordname))
                word_item = word_rel.append_item()
                #try to determine language:
                if wordname.startswith("|"):
                    word_item["lang"] = "eng"
                    wordname = wordname[1:]
                    pronunform = pronunform[1:]
                elif self.__is_allcaps(token_item["name"]): #before lowercase
                    word_item["lang"] = "eng"
                elif (((wordname in self.engpronunaddendum or
                        wordname in self.engpronundict) and
                       len(pronunform) > self.ENGWORD_CHARTHRESHOLD and
                       pronunform not in self.pronunaddendum) or
                      not all([c in self.SMALLGRAPHSET for c in pronunform.lower()])):
                    word_item["lang"] = "eng"
                else:
                    word_item["lang"] = "def" #default language...
                #determine type:
                if re.search("[\d]+", wordname):
                    #TODO: normalisation of digits... at the moment
                    #insert string to make phonetizer fail:
                    pronunform = "1234567890"
                    word_item["type"] = "num"
                    word_item["lang"] = "eng" #will pronounce digits in English...
                else:
                    word_item["type"] = "norm"
                #tokenizer does NFKD... for Yoruba pronunciation
                #resources are in NFC without ACUTE and GRAVE
                #ACCENTS. But we need the ACCENTS to determine tone
                #after syllabification...
                word_item["pronunform"] = pronunform
                word_item["name"] = wordname
                token_item.add_daughter(word_item)
        return utt

    def phonetizer(self, utt, processname):
        
        def g2p(word, phoneset, pronundict, pronunaddendum, g2p):
            syltones = None
            syllables = None
            if pronunaddendum and word["pronunform"] in pronunaddendum:
                    phones = pronunaddendum[word["pronunform"]]
                    syllables = phoneset.syllabify(phones)
            else:
                try:
                    wordpronun = pronundict.lookup(word["pronunform"], word["pos"])
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
                        phones = pronundict[word["pronunform"]]
                    except KeyError:
                        try:
                            phones = g2p.predict_word(word["pronunform"])
                        except (GraphemeNotDefined, NoRuleFound):
                            warns = "WARNING: No pronunciation found for '%s'" % word["name"]
                            print(warns.encode("utf-8"), file=sys.stderr)
                            phones = [self.phoneset.features["silence_phone"]]
                    syllables = phoneset.syllabify(phones)
            if not syltones:
                try:
                    syltones = phoneset.guess_sylstress(syllables)
                except AttributeError:
                    try:
                        syltones = word2tones(word["name"])
                        assert len(syltones) == len(syllables)
                    except AssertionError:
                        #print(word_item["name"], word_item["pronunform"], syllables, syltones)
                        syltones = "N" * len(syllables)
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
                syl_item["tone"] = syltone
                syl_item_in_sylstruct = word_item_in_sylstruct.add_daughter(syl_item)
                
                for phone in syl:
                    seg_item = seg_rel.append_item()
                    seg_item["name"] = phone
                    seg_item_in_sylstruct = syl_item_in_sylstruct.add_daughter(seg_item)
        return utt

    def phrasifier(self, utt, processname):
        """ Determine phrases/phrase breaks in the utterance...
        """

        word_rel = utt.get_relation("Word")
        punctuation = self.PHRASING_PUNCTUATION
        phrase_rel = utt.new_relation("Phrase")
        phrase_item = phrase_rel.append_item()
        phrase_item["name"] = "BB"
        for word_item in word_rel:
            phrase_item.add_daughter(word_item)
            token_item = word_item.get_item_in_relation("Token").parent_item
            if word_item.get_item_in_relation("Token") is token_item.last_daughter:
                if word_item is not word_rel.tail_item:
                    if (("postpunc" in token_item and anycharsin(token_item["postpunc"], punctuation)) or
                        word_item.next_item["pronunform"] in self.CONJUNCTIONS):
                        phrase_item = phrase_rel.append_item()
                        phrase_item["name"] = "BB"
        return utt

# -*- coding: utf-8 -*-
""" This file contains language-specific implementation for a Swati
    voice...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import re
from .. phoneset import Phoneset

class LwaziSwatiPhoneset(Phoneset):
    """ Developed for the Lwazi project...
    """
    def __init__(self):
        #Phoneset.__init__(self)
        self.features = {"name": "Lwazi Swati Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "pau_cl"
                         }
        self.phones = {"pau"    : set(["pause"]),
                       "pau_cl" : set(["closure"]),
                       "ʔ" : set(["glottal-stop"]),
                       "p"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial"]),
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "k"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar"]),
                       "g"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "pʰ"    : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "aspirated"]),
                       "tʼ"    : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "ejective"]),
                       "tʰ"    : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "aspirated"]),
                       "kʰ"    : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "aspirated"]),
                       "ǃ"     : set(["class_consonantal", "consonant", "manner_click", "place_post-alveolar"]),
                       "ǀ"     : set(["class_consonantal", "consonant", "manner_click", "place_dental"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "v"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "z"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar", "voiced"]),
                       "ʃ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar"]),
                       "ɦ"    : set(["consonant", "manner_fricative", "place_glottal", "voiced"]),
                       "h"      : set(["consonant", "manner_fricative", "place_glottal"]),
                       "lʒ"   : set(["class_consonantal", "consonant", "manner_fricative", "manner_lateral", "place_alveolar", "voiced"]),
                       "ɬ"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_lateral", "place_alveolar"]),
                       "m"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "n"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "ŋ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_velar", "voiced"]),
                       "ɲ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced"]),
                       "l"      : set(["class_sonorant", "class_consonantal", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "r"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back", "articulation_rounded"]),
                       "ɛ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɔ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "dʒ"   : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "dz"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "voiced"]),
                       "dβ"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_bilabial", "voiced"]),
                       "tɸ"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_bilabial"]),
                       "tsʼ"   : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "ejective"]),
                       "tsʰ"   : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "aspirated"]),
                       "kɬʼ"   : set(["class_consonantal", "consonant", "manner_affricate", "place_velar", "place_alveolar", "ejective"])
                       }
        self.map = {"pau":"pau",
                    "pau_cl":"pau_cl",
                    "ʔ":"pau_gs",
                    "p":"p",
                    "b":"b",
                    "d":"d",
                    "k":"k",
                    "g":"g",
                    "pʰ":"p_h",
                    "tʼ":"t_e",
                    "tʰ":"t_h",
                    "kʰ":"k_h",
                    "ǃ":"_q",
                    "ǀ":"_c",
                    "f":"f",
                    "v":"v",
                    "s":"s",
                    "z":"z",
                    "ʃ":"S",
                    "ɦ":"h_v",
                    "h":"h",
                    "lʒ":"_lZ_",
                    "ɬ":"K",
                    "m":"m",
                    "n":"n",
                    "ŋ":"N",
                    "ɲ":"J",
                    "l":"l",
                    "r":"r",
                    "j":"j",
                    "w":"w",
                    "u":"u",
                    "ɛ":"E",
                    "ɔ":"O",
                    "i":"i",
                    "a":"a",
                    "dʒ":"d_0Z",
                    "dz":"dz",
                    "dβ":"dB",
                    "tɸ":"t_",
                    "tsʼ":"ts_e",
                    "tsʰ":"ts_h",
                    "kɬʼ":"kK_e"
                    }
        

    def is_vowel(self, phonename):
        return "vowel" in self.phones[phonename]

    def is_syllabicconsonant(self, phonename):
        return "class_syllabic" in self.phones[phonename] and "consonant" in self.phones[phonename]


    def syllabify(self, phonelist):
        """ Basic Swati syllabification, based on the syllabification
            scheme devised by Etienne Barnard for isiZulu (Nguni
            language).
        """
        sylls = [[]]
        phlist = phonelist[:]

        while phlist:
            phone = phlist[0]

            if self.is_syllabicconsonant(phone):
                #sC.Any
                sylls[-1].append(phlist.pop(0))
                if phlist: sylls.append([])
                continue

            try:
                nphone = phlist[1]
                nnphone = phlist[2]
                #If there is a three phone cluster:
                if (self.is_vowel(phone) and
                    not self.is_vowel(nphone) and
                    not self.is_vowel(nnphone)):
                    #VC.C
                    sylls[-1].append(phlist.pop(0))#phone
                    sylls[-1].append(phlist.pop(0))#nphone
                    if phlist: sylls.append([])
                    continue
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

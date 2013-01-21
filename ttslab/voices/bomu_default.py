# -*- coding: utf-8 -*-
""" Initial phoneset implementation for a Bomu voice...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import re
from .. phoneset import Phoneset

class BomuPhoneset(Phoneset):
    """ Based on Bomu description and data received from Stephane
        Boyera...

        DEMITASSE: check again later when the phoneset/language is more familiar!
    """

    def __init__(self):
        Phoneset.__init__(self)

        self.features = {"name": "Bomu Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "pau_cl"
                         }
        self.phones = {"pau"    : set(["pause"]),
                       "pau_cl" : set(["closure"]),
                       #vowels
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "e"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɛ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "o"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back"]),
                       #nasalised
                       "ã"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "ẽ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɛ̃"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ĩ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "õ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "ũ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back"]),
                       #long
                       "aː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "eː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɛː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "iː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "oː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "uː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back"]),
                       #nasalised long
                       "ãː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "ẽː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɛ̃ː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ĩː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "õː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "ũː"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back"]),
                       #consonants
                       "ʔ"      : set(["class_consonantal", "consonant", "manner_plosive", "place_glottal"]),
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "β"      : set(["class_consonantal", "consonant", "manner_fricative", "place_bilabial", "voiced"]),
                       "tʃ"     : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "g"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "h"      : set(["consonant", "manner_fricative", "place_glottal"]),
                       "k"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar"]),
                       "l"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "m"      : set(["class_sonorant", "class_syllabic", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "n"      : set(["class_sonorant", "class_syllabic", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "ɲ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced"]),
                       "p"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial"]),
                       "r"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "t"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar"]),
                       "v"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental", "voiced"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "z"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar", "voiced"])
                       }
        self.map = {"pau"    : "pau",
                    "pau_cl" : "pau_cl",
                    "a"      : "a",
                    "e"      : "e",
                    "ɛ"      : "E",
                    "i"      : "i",
                    "o"      : "o",
                    "u"      : "u",
                    "ã"      : "an", 
                    "ẽ"      : "en", 
                    "ɛ̃"      : "En", 
                    "ĩ"      : "in", 
                    "õ"      : "on", 
                    "ũ"      : "un",
                    "ʔ"      : "pau_gs",
                    "b"      : "b",
                    "β"      : "B",
                    "tʃ"     : "tS",
                    "d"      : "d",
                    "f"      : "f",
                    "g"      : "g",
                    "h"      : "h",
                    "k"      : "k",
                    "l"      : "l",
                    "m"      : "m",
                    "n"      : "n",
                    "ɲ"      : "J",
                    "p"      : "p",
                    "r"      : "r",
                    "s"      : "s",
                    "t"      : "t",
                    "v"      : "v",
                    "w"      : "w",
                    "j"      : "j",
                    "z"      : "z"
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

        

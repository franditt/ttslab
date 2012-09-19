# -*- coding: utf-8 -*-
""" This file contains language-specific implementation for a Venda
    voice.
"""
from __future__ import unicode_literals, division, print_function #Py2

import re
from .. phoneset import Phoneset

class LwaziVendaPhoneset(Phoneset):
    """ Developed for the Lwazi project...
    """
    def __init__(self):
        #Phoneset.__init__(self)
        self.features = {"name": "Lwazi Venda Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "pau_cl"
                         }
        self.phones = {"pau"    : set(["pause"]),
                       "pau_cl" : set(["closure"]),
                       "pau_gs" : set(["glottal-stop"]),
                       "dʒ"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "dz"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "voiced"]),
                       "ɦ"      : set(["consonant", "manner_fricative", "place_glottal", "voiced"]),
                       "ɟ"      : set(["class_consonantal", "consonant", "manner_plosive", "place_palatal", "voiced"]),
                       "kʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "ejective"]),
                       "kʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "aspirated"]),
                       "ɸ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_bilabial"]),
                       "pʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "ejective"]),
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "β"      : set(["class_consonantal", "consonant", "manner_fricative", "place_bilabial", "voiced"]),
                       "pʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "aspirated"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "sw"     : set(["class_consonantal", "consonant", "manner_fricative", "place_alveolar", "place_labial"]),
                       "ɛ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "tʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "ejective"]),
                       "tʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "aspirated"]),
                       "g"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "tsʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "ejective"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "ɲ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced"]),
                       "tsʰ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "aspirated"]),
                       "l"      : set(["class_sonorant", "class_consonantal", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "tʃʰ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "aspirated"]),
                       "m"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "zw"     : set(["class_consonantal", "consonant", "manner_fricative", "place_alveolar", "place_retroflex", "voiced"]),
                       "n"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "ŋ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_velar", "voiced"]),
                       "ɔ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "r"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "ʃ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back", "articulation_rounded"]),
                       "v"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental", "voiced"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"]),
                       "x"      : set(["class_consonantal", "consonant", "manner_fricative", "place_velar"]),
                       "z"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar", "voiced"]),
                       "ʒ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar", "voiced"])
                       }
        self.map = {"pau":"pau",
                    "pau_cl":"pau_cl",
                    "pau_gs":"pau_gs",
                    "dʒ":"d_0Z",
                    "dz":"dz",
                    "ɦ":"h_v",
                    "ɟ":"_dy_",
                    "kʼ":"k_e",
                    "kʰ":"k_h",
                    "ɸ":"p_",
                    "pʼ":"p_e",
                    "a":"a",
                    "b":"b",
                    "β":"B",
                    "pʰ":"p_h",
                    "d":"d",
                    "sw":"sw",
                    "ɛ":"E",
                    "f":"f",
                    "tʼ":"t_e",
                    "tʰ":"t_h",
                    "g":"g",
                    "tsʼ":"ts_e",
                    "i":"i",
                    "j":"j",
                    "ɲ":"J",
                    "tsʰ":"ts_h",
                    "l":"l",
                    "tʃʰ":"tS_h",
                    "m":"m",
                    "zw":"zw",
                    "n":"n",
                    "ŋ":"N",
                    "ɔ":"O",
                    "r":"r",
                    "s":"s",
                    "ʃ":"S",
                    "u":"u",
                    "v":"v",
                    "w":"w",
                    "x":"x",
                    "z":"z",
                    "ʒ":"Z"
                    }


    def is_vowel(self, phonename):
        return "vowel" in self.phones[phonename]

    def is_syllabicconsonant(self, phonename):
        return "class_syllabic" in self.phones[phonename] and "consonant" in self.phones[phonename]


    def syllabify(self, phonelist):
        """ Basic Venda syllabification, based on the syllabification
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

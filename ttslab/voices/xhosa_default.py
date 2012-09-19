# -*- coding: utf-8 -*-
""" This file contains language-specific implementation for a Xhosa
    voice...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import re
from .. phoneset import Phoneset

class LwaziXhosaPhoneset(Phoneset):
    """ Developed for the Lwazi project...
    """
    def __init__(self):
        #Phoneset.__init__(self)
        self.features = {"name": "Lwazi Xhosa Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "pau_cl"
                         }
        self.phones = {"pau"    : set(["pause"]),
                       "pau_cl" : set(["closure"]),
                       "pau_gs" : set(["glottal-stop"]),
                       "ɑ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_back"]),
                       "ɛ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɣ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_velar", "voiced"]),
                       "ɲ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced"]),
                       "ɲʰ"     : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced", "aspirated"]),
                       "ɬ"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_lateral", "place_alveolar"]),
                       "ŋ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_velar", "voiced"]),
                       "ɔ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "ʃ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar"]),
                       "ǀ"      : set(["class_consonantal", "consonant", "manner_click", "place_dental"]),
                       "ǀʰ"     : set(["class_consonantal", "consonant", "manner_click", "place_dental", "aspirated"]),
                       "ǀ̬"      : set(["class_consonantal", "consonant", "manner_click", "place_dental", "voiced"]),
                       "ɟ"      : set(["class_consonantal", "consonant", "manner_plosive", "place_palatal", "voiced"]),
                       "lʒ"     : set(["class_consonantal", "consonant", "manner_fricative", "manner_lateral", "place_alveolar", "voiced"]),
                       "ǃ"      : set(["class_consonantal", "consonant", "manner_click", "place_post-alveolar"]),
                       "ǃʰ"     : set(["class_consonantal", "consonant", "manner_click", "place_post-alveolar", "aspirated"]),
                       "ǃ̬"      : set(["class_consonantal", "consonant", "manner_click", "place_post-alveolar", "voiced"]),
                       "ǁ"      : set(["class_consonantal", "consonant", "manner_click", "manner_lateral", "place_alveolar"]),
                       "ǁʰ"     : set(["class_consonantal", "consonant", "manner_click", "manner_lateral", "place_alveolar", "aspirated"]),
                       "ǁ̬"      : set(["class_consonantal", "consonant", "manner_click", "manner_lateral", "place_alveolar", "voiced"]),
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "ɓ"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced", "implosive"]),
                       "cʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_palatal", "ejective"]),
                       "cʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_palatal", "aspirated"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "dʒ"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "g"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "h"      : set(["consonant", "manner_fricative", "place_glottal"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "kʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "ejective"]),
                       "kʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "aspirated"]),
                       "kxʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "place_velar", "ejective"]),
                       "l"      : set(["class_sonorant", "class_consonantal", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "m"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "mʰ"     : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced", "aspirated"]),
                       "n"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "nʰ"     : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced", "aspirated"]),
                       "pʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "ejective"]),
                       "pʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "aspirated"]),
                       "r"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "tɬʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_lateral", "place_alveolar", "ejective"]),
                       "tʃʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "ejective"]),
                       "tʃʰ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "aspirated"]),
                       "tʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "ejective"]),
                       "tʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "aspirated"]),
                       "tsʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "ejective"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back", "articulation_rounded"]),
                       "v"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental", "voiced"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"]),
                       "z"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar", "voiced"])
                       }
        self.map = {"pau":"pau",
                    "pau_cl":"pau_cl",
                    "pau_gs":"pau_gs",
                    "ɑ":"A",
                    "ɛ":"E",
                    "ɣ":"G",
                    "ɲ":"J",
                    "ɲʰ":"J_h",
                    "ɬ":"K",
                    "ŋ":"N",
                    "ɔ":"O",
                    "ʃ":"S",
                    "ǀ":"_c",
                    "ǀʰ":"_c_h",
                    "ǀ̬":"_c_v",
                    "ɟ":"_dy_",
                    "lʒ":"_lZ_",
                    "ǃ":"_q",
                    "ǃʰ":"_q_h",
                    "ǃ̬":"_q_v",
                    "ǁ":"_x",
                    "ǁʰ":"_x_h",
                    "ǁ̬":"_x_v",
                    "b":"b",
                    "ɓ":"b_E",
                    "cʼ":"c_e",
                    "cʰ":"c_h",
                    "d":"d",
                    "dʒ":"d_0Z",
                    "f":"f",
                    "g":"g",
                    "h":"h",
                    "i":"i",
                    "j":"j",
                    "kʼ":"k_e",
                    "kʰ":"k_h",
                    "kxʼ":"kx_e",
                    "l":"l",
                    "m":"m",
                    "mʰ":"m_h",
                    "n":"n",
                    "nʰ":"n_h",
                    "pʼ":"p_e",
                    "pʰ":"p_h",
                    "r":"r",
                    "s":"s",
                    "tɬʼ":"tK_e",
                    "tʃʼ":"tS_e",
                    "tʃʰ":"tS_h",
                    "tʼ":"t_e",
                    "tʰ":"t_h",
                    "tsʼ":"ts_e",
                    "u":"u",
                    "v":"v",
                    "w":"w",
                    "z":"z"
                    }
        

    def is_vowel(self, phonename):
        return "vowel" in self.phones[phonename]

    def is_syllabicconsonant(self, phonename):
        return "class_syllabic" in self.phones[phonename] and "consonant" in self.phones[phonename]


    def syllabify(self, phonelist):
        """ Basic Xhosa syllabification, based on the syllabification
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

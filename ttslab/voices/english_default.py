# -*- coding: utf-8 -*-
""" This file contains language-specific implementation for a South
    African English voice.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import re
from .. phoneset import Phoneset

class LwaziEnglishPhoneset(Phoneset):
    """ Based on MRPA...
    """
    def __init__(self):
        #Phoneset.__init__(self)

        #syllable_clusters are processed in order, thus a list, not a set...
        self.features = {"name": "Lwazi English Phoneset",
                         "syllable_clusters": ["VCV", "VCCV", "VCCCV", "VCCCCV",
                                                "VCGV", "VCCGV", "VCCCGV", "VV"],
                         "wellformed_plosive_clusters": [["p","l"], ["b","l"], ["k","l"], ["g","l"], ["p","ɹ"],
                                                         ["b","ɹ"], ["t","ɹ"], ["d","ɹ"], ["k","ɹ"], ["g","ɹ"],
                                                         ["t","w"], ["d","w"], ["g","w"], ["k","w"], ["p","j"],
                                                         ["b","j"], ["t","j"], ["d","j"], ["k","j"], ["g","j"]],
                         "wellformed_fricative_clusters": [["f","l"], ["f","ɹ"], ["θ","ɹ"], ["ʃ","ɹ"],
                                                           ["θ","w"], ["h","w"], ["f","j"], ["v","j"],
                                                           ["θ","j"], ["z","j"], ["h","j"]],
                         "wellformed_other_clusters": [["m","j"], ["n","j"], ["l","j"]],
                         "wellformed_s_clusters": [["s","p"], ["s","t"], ["s","k"], ["s","m"], ["s","n"],
                                                   ["s","f"], ["s","w"], ["s","l"], ["s","j"], ["s","p","l"],
                                                   ["s","p","ɹ"], ["s","p","j"], ["s","m","j"], ["s","t","ɹ"],
                                                   ["s","t","j"], ["s","k","l"], ["s","k","ɹ"], ["s","k","w"],
                                                   ["s","k","j"]]
                         }
        self.features["wellformed_clusters"] = (self.features["wellformed_plosive_clusters"] +
                                                self.features["wellformed_fricative_clusters"] +
                                                self.features["wellformed_other_clusters"] +
                                                self.features["wellformed_s_clusters"])
        self.features["silence_phone"] = "pau"
        self.features["closure_phone"] = "pau_cl"
        self.phones = {"pau"    : set(["pause"]),
                       "pau_cl" : set(["closure"]),
                       "ʔ"      : set(["glottal-stop"]),
                       "ə"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_central"]),
                       "ɜ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_mid", "position_central"]),
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "ɑ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_low", "position_back"]),
                       "aɪ"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "aʊ"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "tʃ"     : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "ð"      : set(["class_consonantal", "consonant", "manner_fricative", "place_dental", "voiced"]),
                       "ɛ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ɛə"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "eɪ"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "g"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "h"      : set(["consonant", "manner_fricative", "place_glottal"]),
                       "ɪ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "ɪə"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "dʒ"     : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "k"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar"]),
                       "l"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "m"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "n"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "ŋ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_velar", "voiced"]),
                       "ɒ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_back", "articulation_rounded"]),
                       "ɔɪ"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "ɔ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "əʊ"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "p"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial"]),
                       "ɹ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_approximant", "manner_liquid", "place_alveolar", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "ʃ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar"]),
                       "t"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar"]),
                       "θ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_dental"]),
                       "ʊ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back", "articulation_rounded"]),
                       "ʊə"     : set(["class_sonorant", "class_syllabic", "vowel", "duration_diphthong"]),
                       "ʌ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_long", "height_high", "position_back", "articulation_rounded"]),
                       "v"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental", "voiced"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "z"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar", "voiced"]),
                       "ʒ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar", "voiced"])
                       }
        self.map = {"pau":"pau",
                    "pau_cl":"pau_cl",
                    "ʔ":"pau_gs",
                    "ə":"_",
                    "ɜ":"__",
                    "a":"a",
                    "ɑ":"aa",
                    "aɪ":"ai",
                    "aʊ":"au",
                    "b":"b",
                    "tʃ":"ch",
                    "d":"d",
                    "ð":"dh",
                    "ɛ":"e",
                    "ɛə":"e_",
                    "eɪ":"ei",
                    "f":"f",
                    "g":"g",
                    "h":"h",
                    "ɪ":"i",
                    "ɪə":"i_",
                    "i":"ii",
                    "dʒ":"jh",
                    "k":"k",
                    "l":"l",
                    "m":"m",
                    "n":"n",
                    "ŋ":"ng",
                    "ɒ":"o",
                    "ɔɪ":"oi",
                    "ɔ":"oo",
                    "əʊ":"ou",
                    "p":"p",
                    "ɹ":"r",
                    "s":"s",
                    "ʃ":"sh",
                    "t":"t",
                    "θ":"th",
                    "ʊ":"u",
                    "ʊə":"u_",
                    "ʌ":"uh",
                    "u":"uu",
                    "v":"v",
                    "w":"w",
                    "j":"y",
                    "z":"z",
                    "ʒ":"zh"
                    }
       
    def is_plosive(self, phonename):
        return "manner_plosive" in self.phones[phonename]

    def is_voiced(self, phonename):
        return ("voiced" in self.phones[phonename] or
                "vowel" in self.phones[phonename])

    def is_obstruent(self, phonename):
        return ("class_consonantal" in self.phones[phonename] and
                "class_sonorant" not in self.phones[phonename] and
                "class_syllabic" not in self.phones[phonename])

    def is_vowel(self, phonename):
        return "vowel" in self.phones[phonename]

    def is_glide(self, phonename):
        return "manner_glide" in self.phones[phonename]

    def is_liquid(self, phonename):
        return "manner_liquid" in self.phones[phonename]

    def is_syllabicconsonant(self, phonename):
        return "class_syllabic" in self.phones[phonename] and "consonant" in self.phones[phonename]

    def is_fricative(self, phonename):
        return "manner_fricative" in self.phones[phonename]

    def is_nasal(self, phonename):
        return "manner_nasal" in self.phones[phonename]

    def sonority_level(self, phonename):
        """ Assigns levels of sonority to phones based on their nature...
        """
        
        if self.is_vowel(phonename):
            if "height_low" in self.phones[phonename]:
                return 9
            if "height_mid" in self.phones[phonename]:
                return 8
            if "height_high" in self.phones[phonename]:
                return 7
        if self.is_liquid(phonename):
            return 6
        if self.is_nasal(phonename):
            return 5
        if self.is_fricative(phonename):
            if self.is_voiced(phonename):
                return 4
            else:
                return 3
        if self.is_plosive(phonename):
            if self.is_voiced(phonename):
                return 2
            else:
                return 1
        return 0


    def _process_cluster(self, cluster, phonelist, match):
        """ Break cluster into syllables according to the rules defined by
            T.A. Hall, "English syllabification as the interaction of
            markedness constraints" in Studia Linguistica, vol. 60, 2006,
            pp. 1-33

            Need to refactor the if statements to make clearer/simpler...
        """

        phonecluster = phonelist[match.start() : match.end()]

        if cluster == "VCV":
            #always split -> V.CV:
            return "V.CV"

        if cluster == "VCCV":
            CC = phonecluster[1:3]
            #if CC cluster is Tautosyllabic -> V.CCV:
            if ((CC in self.features["wellformed_clusters"] and
                 self.sonority_level(CC[1]) > self.sonority_level(CC[0])) or
                (CC[0] == "s" and
                 self.is_plosive(CC[1]) and
                 not self.is_voiced(CC[1]))):
                return "V.CCV"
            #if CC cluster is Heterosyllabic -> VC.CV:
            if ((self.sonority_level(CC[1]) < self.sonority_level(CC[0])) or
                (self.sonority_level(CC[1]) == self.sonority_level(CC[0])) or
                (CC not in self.features["wellformed_clusters"] and
                 self.sonority_level(CC[1]) > self.sonority_level(CC[0]))):
                return "VC.CV"

        if cluster == "VCCCV":
            CCC = phonecluster[1:4]
            C2C3 = CCC[1:]
            #if CCC are all obstruents -> VC.CCV:
            if all([self.is_obstruent(C) for C in CCC]):
                return "VC.CCV"
            #if C2C3 are wellformed onsets -> VC.CCV:
            if C2C3 in self.features["wellformed_clusters"]:
                return "VC.CCV"
            else:
                return "VCC.CV"

        if cluster == "VCCCCV":
            #always split -> VC.CCCV:
            return "VC.CCCV"

        if cluster == "VCGV":
            CG = phonecluster[1:3]
            if not self.is_plosive(CG[0]):                   #C not a stop
                return "VC.GV"
            else:
                if CG not in self.features["wellformed_clusters"]: #C a stop and CG not wellformed
                    return "VC.GV"
                else:
                    return "V.CGV"                                 #C a stop and CG wellformed

        if cluster == "VCCGV":
            CCG = phonecluster[1:4]
            if CCG[0] == "s":
                return "V.CCGV"
            else:
                return "VC.CGV"

        if cluster == "VCCCGV":
            return "VC.CCGV"

        if cluster == "VV":   #not described in the Hall paper...
            return "V.V"


    def syllabify(self, phonelist):
        """ Classes:
               C -> Consonant,
               V -> Short/Long Vowel/Syllabic sonorant/Diphthong
               G -> Glide
        """
        #make a copy (to be edited internally)
        plist = list(phonelist)

        #first construct string representing relevant classes...
        classstr = ""
        for phone in plist:
            if self.is_vowel(phone):
                classstr += "V"
            elif self.is_glide(phone):
                classstr += "G"
            else:
                classstr += "C"
        #Begin Aby's hacks:
        # - Change the last phoneclass under certain conditions..
        try:
            if (self.is_syllabicconsonant(plist[-1]) and
                self.is_obstruent(plist[-2])):
                classstr = classstr[:-1] + "V"
            if (self.is_syllabicconsonant(plist[-1]) and
                self.is_nasal(plist[-2])):
                classstr = classstr[:-1] + "V"
        except IndexError:
            pass
        #End Aby's hacks...

        #find syllable_clusters in order and apply syllabification 
        #process on each...this should be redone... FIXME!!!
        for cluster in self.features["syllable_clusters"]:
            match = re.search(cluster, classstr)
            while match:
                #syllabify cluster
                clustersylstr = self._process_cluster(cluster, plist, match)
                #update classstr...
                start, end = match.span()
                classstr = clustersylstr.join([classstr[:start], classstr[end:]])
                plist = (plist[:match.start() + clustersylstr.index(".")] +
                             [""] + plist[match.start() + clustersylstr.index("."):])
                #next match...
                match = re.search(cluster, classstr)

        sylls = [[]]
        index = 0
        for char in classstr:
            if char != ".":
                sylls[-1].append(phonelist[index])
                index += 1
            else:
                sylls.append([])

        return sylls
        
    def guess_sylstress(self, syllables):
        """ Try to guess stress pattern for an unknown word...
        """
        if len(syllables) == 1:
            if "ə" not in syllables[0]:
                return "1"
            else:
                return "0"
        else:
            return "0" * len(syllables) #implement other cases later

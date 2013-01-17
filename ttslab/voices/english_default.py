# -*- coding: utf-8 -*-
""" This file contains language-specific implementations for South
    African English (based on Lwazi) and US English (based on
    CMUdict).
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
                    "ə":"_",     #about
                    "ɜ":"__",    #bird
                    "a":"a",     #bad
                    "ɑ":"aa",    #bard
                    "aɪ":"ai",   #buy
                    "aʊ":"au",   #cow
                    "b":"b",
                    "tʃ":"ch",   #chin
                    "d":"d",
                    "ð":"dh",    #then
                    "ɛ":"e",     #bed
                    "ɛə":"e_",   #bare
                    "eɪ":"ei",   #bay
                    "f":"f",
                    "g":"g",
                    "h":"h",
                    "ɪ":"i",     #bid
                    "ɪə":"i_",   #beer
                    "i":"ii",    #bead
                    "dʒ":"jh",   #edge
                    "k":"k",
                    "l":"l",
                    "m":"m",
                    "n":"n",
                    "ŋ":"ng",    #sing
                    "ɒ":"o",     #pot
                    "ɔɪ":"oi",   #boy
                    "ɔ":"oo",    #port
                    "əʊ":"ou",   #go
                    "p":"p",
                    "ɹ":"r",     #ray
                    "s":"s",
                    "ʃ":"sh",    #she
                    "t":"t",
                    "θ":"th",    #thin
                    "ʊ":"u",     #put
                    "ʊə":"u_",   #poor
                    "ʌ":"uh",    #bud
                    "u":"uu",    #boot
                    "v":"v",
                    "w":"w",
                    "j":"y",     #yes
                    "z":"z",
                    "ʒ":"zh"     #beige
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


class CMUEnglishPhoneset(LwaziEnglishPhoneset):
    """ Based on ARPAbet... see: http://en.wikipedia.org/wiki/Arpabet

        Phoneme Example Translation
        ------- ------- -----------
        AA	odd     AA D
        AE	at	AE T
        AH	hut	HH AH T
        AO	ought	AO T
        AW	cow	K AW
        AY	hide	HH AY D
        B 	be	B IY
        CH	cheese	CH IY Z
        D 	dee	D IY
        DH	thee	DH IY
        EH	Ed	EH D
        ER	hurt	HH ER T
        EY	ate	EY T
        F 	fee	F IY
        G 	green	G R IY N
        HH	he	HH IY
        IH	it	IH T
        IY	eat	IY T
        JH	gee	JH IY
        K 	key	K IY
        L 	lee	L IY
        M 	me	M IY
        N 	knee	N IY
        NG	ping	P IH NG
        OW	oat	OW T
        OY	toy	T OY
        P 	pee	P IY
        R 	read	R IY D
        S 	sea	S IY
        SH	she	SH IY
        T 	tea	T IY
        TH	theta	TH EY T AH
        UH	hood	HH UH D
        UW	two	T UW
        V 	vee	V IY
        W 	we	W IY
        Y 	yield	Y IY L D
        Z 	zee	Z IY
        ZH	seizure	S IY ZH ER
    """
    def __init__(self):
        #Phoneset.__init__(self)

        #syllable_clusters are processed in order, thus a list, not a set...
        self.features = {"name": "CMU English Phoneset",
                         "syllable_clusters": ["VCV", "VCCV", "VCCCV", "VCCCCV",
                                                "VCGV", "VCCGV", "VCCCGV", "VV"],
                         "wellformed_plosive_clusters": [["p","l"], ["b","l"], ["k","l"], ["g","l"], ["p","r"],
                                                         ["b","r"], ["t","r"], ["d","r"], ["k","r"], ["g","r"],
                                                         ["t","w"], ["d","w"], ["g","w"], ["k","w"], ["p","y"],
                                                         ["b","y"], ["t","y"], ["d","y"], ["k","y"], ["g","y"]],
                         "wellformed_fricative_clusters": [["f","l"], ["f","r"], ["th","r"], ["sh","r"],
                                                           ["th","w"], ["hh","w"], ["f","y"], ["v","y"],
                                                           ["th","y"], ["z","y"], ["hh","y"]],
                         "wellformed_other_clusters": [["m","y"], ["n","y"], ["l","y"]],
                         "wellformed_s_clusters": [["s","p"], ["s","t"], ["s","k"], ["s","m"], ["s","n"],
                                                   ["s","f"], ["s","w"], ["s","l"], ["s","y"], ["s","p","l"],
                                                   ["s","p","r"], ["s","p","y"], ["s","m","y"], ["s","t","r"],
                                                   ["s","t","y"], ["s","k","l"], ["s","k","r"], ["s","k","w"],
                                                   ["s","k","y"]]
                         }
        self.features["wellformed_clusters"] = (self.features["wellformed_plosive_clusters"] +
                                                self.features["wellformed_fricative_clusters"] +
                                                self.features["wellformed_other_clusters"] +
                                                self.features["wellformed_s_clusters"])
        self.features["silence_phone"] = "pau"
        self.features["closure_phone"] = "pau_cl"
        self.phones = {"pau"    : set(["pause"]),
                       "pau_cl" : set(["closure"]),
                       "pau_gs" : set(["glottal-stop"]),
                       "aa" : set(["duration_short", "position_back", "height_low", "class_syllabic", "vowel", "class_sonorant"]),
                       "iy" : set(["position_front", "duration_long", "height_high", "class_syllabic", "vowel", "class_sonorant"]),
                       "ch" : set(["place_alveolar", "class_consonantal", "manner_affricate", "consonant", "manner_strident", "place_post-alveolar"]),
                       "ae" : set(["duration_short", "position_front", "height_low", "class_syllabic", "vowel", "class_sonorant"]),
                       "eh" : set(["duration_short", "position_front", "class_syllabic", "vowel", "height_mid", "class_sonorant"]),
                       "ah" : set(["duration_short", "position_back", "class_syllabic", "vowel", "height_mid", "class_sonorant"]),
                       "ao" : set(["duration_long", "articulation_round", "position_back", "class_syllabic", "vowel", "height_mid", "class_sonorant"]),
                       "ih" : set(["duration_short", "position_front", "height_high", "class_syllabic", "vowel", "class_sonorant"]),
                       "ey" : set(["position_front", "duration_diphthong", "class_syllabic", "vowel", "height_mid", "class_sonorant"]),
                       "aw" : set(["position_front", "duration_diphthong", "height_low", "class_syllabic", "vowel", "class_sonorant"]),
                       "ay" : set(["position_front", "duration_diphthong", "height_low", "class_syllabic", "vowel", "class_sonorant"]),
                       "zh" : set(["class_consonantal", "voiced", "manner_fricative", "consonant", "place_post-alveolar"]),
                       "er" : set(["position_central", "duration_short", "class_syllabic", "vowel", "height_mid", "class_sonorant"]),
                       "ng" : set(["class_consonantal", "voiced", "manner_nasal", "place_velar", "consonant", "class_sonorant"]),
                       "r"  : set(["place_alveolar", "class_consonantal", "manner_liquid", "voiced", "manner_approximant", "consonant", "class_sonorant"]),
                       "th" : set(["class_consonantal", "manner_fricative", "consonant", "place_dental"]),
                       "uh" : set(["duration_short", "position_back", "height_high", "class_syllabic", "vowel", "class_sonorant"]),
                       "oy" : set(["duration_diphthong", "articulation_round", "position_back", "class_syllabic", "vowel", "height_mid", "class_sonorant"]),
                       "dh" : set(["class_consonantal", "voiced", "manner_fricative", "consonant", "place_dental"]),
                       "ow" : set(["duration_diphthong", "articulation_round", "position_back", "class_syllabic", "vowel", "height_mid", "class_sonorant"]),
                       "hh" : set(["manner_fricative", "consonant", "place_glottal"]),
                       "jh" : set(["place_alveolar", "class_consonantal", "manner_affricate", "voiced", "consonant", "manner_strident", "place_post-alveolar"]),
                       "b"  : set(["class_consonantal", "place_bilabial", "voiced", "manner_plosive", "consonant"]),
                       "d"  : set(["place_alveolar", "class_consonantal", "voiced", "manner_plosive", "consonant"]),
                       "g"  : set(["class_consonantal", "voiced", "place_velar", "manner_plosive", "consonant"]),
                       "f"  : set(["class_consonantal", "manner_fricative", "consonant", "manner_strident", "place_labiodental"]),
                       "uw" : set(["duration_long", "articulation_round", "position_back", "height_high", "class_syllabic", "vowel", "class_sonorant"]),
                       "m"  : set(["class_consonantal", "voiced", "manner_nasal", "consonant", "place_labial", "class_sonorant"]),
                       "l"  : set(["place_alveolar", "class_consonantal", "manner_liquid", "voiced", "manner_approximant", "consonant", "manner_lateral", "class_sonorant"]),
                       "n"  : set(["place_alveolar", "class_consonantal", "voiced", "manner_nasal", "consonant", "class_sonorant"]),
                       "p"  : set(["class_consonantal", "place_bilabial", "manner_plosive", "consonant"]),
                       "s"  : set(["place_alveolar", "class_consonantal", "manner_fricative", "consonant", "manner_strident"]),
                       "sh" : set(["class_consonantal", "manner_fricative", "consonant", "place_post-alveolar"]),
                       "t"  : set(["place_alveolar", "class_consonantal", "manner_plosive", "consonant"]),
                       "w"  : set(["voiced", "place_velar", "manner_approximant", "manner_glide", "consonant", "place_labial", "class_sonorant"]),
                       "v"  : set(["class_consonantal", "voiced", "manner_fricative", "consonant", "manner_strident", "place_labiodental"]),
                       "y"  : set(["voiced", "place_palatal", "manner_approximant", "manner_glide", "consonant", "class_sonorant"]),
                       "z"  : set(["place_alveolar", "class_consonantal", "voiced", "manner_fricative", "consonant", "manner_strident"]),
                       "k"  : set(["class_consonantal", "place_velar", "manner_plosive", "consonant"])
                       }        
        self.map = dict((k, k) for k in self.phones) # redundant mapping

    def guess_sylstress(self, syllables):
        """ Try to guess stress pattern for an unknown word...
        """
        if len(syllables) == 1:
            if "ah" not in syllables[0]: #schwa
                return "1"
            else:
                return "0"
        else:
            return "0" * len(syllables) #implement other cases later

# -*- coding: utf-8 -*-
""" This file contains language-specific implementation for a Zulu
    voice...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import re
import unicodedata
from .. phoneset import Phoneset
from .. defaultvoice import LwaziMultiHTSVoice

class LwaziZuluPhoneset(Phoneset):
    """ Developed for the Lwazi project...
    """
    def __init__(self):
        #Phoneset.__init__(self)
        self.features = {"name": "Lwazi Zulu Phoneset",
                         "silence_phone": "pau",
                         "closure_phone": "pau_cl"
                         }
        self.phones = {"pau"    : set(["pause"]),
                       "pau_cl" : set(["closure"]),
                       "ʔ"      : set(["glottal-stop"]),
                       "pʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "ejective"]),
                       "pʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "aspirated"]),
                       "ɓ"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced", "implosive"]),
                       "tʼ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "ejective"]),
                       "tʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "aspirated"]),
                       "lʒ"     : set(["class_consonantal", "consonant", "manner_fricative", "manner_lateral", "place_alveolar", "voiced"]),
                       "tsʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "ejective"]),
                       "tʃʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "manner_strident", "place_alveolar", "place_post-alveolar", "ejective"]),
                       "dʒ"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "place_post-alveolar", "voiced"]),
                       "a"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_low", "position_front"]),
                       "kʰ"     : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "aspirated"]),
                       "b"      : set(["class_consonantal", "consonant", "manner_plosive", "place_bilabial", "voiced"]),
                       "kɬʼ"    : set(["class_consonantal", "consonant", "manner_affricate", "place_velar", "place_alveolar", "ejective"]),
                       "ɦ"      : set(["consonant", "manner_fricative", "place_glottal", "voiced"]),
                       "ǀ"      : set(["class_consonantal", "consonant", "manner_click", "place_dental"]),
                       "d"      : set(["class_consonantal", "consonant", "manner_plosive", "place_alveolar", "voiced"]),
                       "ǃ"      : set(["class_consonantal", "consonant", "manner_click", "place_post-alveolar"]),
                       "ɛ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_front"]),
                       "ǁ"      : set(["class_consonantal", "consonant", "manner_click", "manner_lateral", "place_alveolar"]),
                       "f"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental"]),
                       "g"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar", "voiced"]),
                       "ǀʰ"     : set(["class_consonantal", "consonant", "manner_click", "place_dental", "aspirated"]),
                       "h"      : set(["consonant", "manner_fricative", "place_glottal"]),
                       "ǃʰ"     : set(["class_consonantal", "consonant", "manner_click", "place_post-alveolar", "aspirated"]),
                       "ǁʰ"     : set(["class_consonantal", "consonant", "manner_click", "manner_lateral", "place_alveolar", "aspirated"]),
                       "i"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_front"]),
                       "j"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_palatal", "voiced"]),
                       "ɲ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_palatal", "voiced"]),
                       "k"      : set(["class_consonantal", "consonant", "manner_plosive", "place_velar"]),
                       "ɬ"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_lateral", "place_alveolar"]),
                       "ǀ̬"      : set(["class_consonantal", "consonant", "manner_click", "place_dental", "voiced"]),
                       "l"      : set(["class_sonorant", "class_consonantal", "manner_approximant", "manner_liquid", "manner_lateral", "place_alveolar", "voiced"]),
                       "ǃ̬"      : set(["class_consonantal", "consonant", "manner_click", "place_post-alveolar", "voiced"]),
                       "m"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_bilabial", "voiced"]),
                       "n"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_alveolar", "voiced"]),
                       "ŋ"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_nasal", "place_velar", "voiced"]),
                       "ǁ̬"      : set(["class_consonantal", "consonant", "manner_click", "manner_lateral", "place_alveolar", "voiced"]),
                       "ɔ"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_mid", "position_back", "articulation_rounded"]),
                       "dz"     : set(["class_consonantal", "consonant", "manner_affricate", "place_alveolar", "voiced"]),
                       "r"      : set(["class_sonorant", "class_consonantal", "consonant", "manner_trill", "place_alveolar", "voiced"]),
                       "s"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar"]),
                       "ʃ"      : set(["class_consonantal", "consonant", "manner_fricative", "place_post-alveolar"]),
                       "u"      : set(["class_sonorant", "class_syllabic", "vowel", "duration_short", "height_high", "position_back", "articulation_rounded"]),
                       "v"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_labiodental", "voiced"]),
                       "w"      : set(["class_sonorant", "consonant", "manner_approximant", "manner_glide", "place_labial", "place_velar", "voiced"]),
                       "z"      : set(["class_consonantal", "consonant", "manner_fricative", "manner_strident", "place_alveolar", "voiced"])
                       }
        self.map = {"pau":"pau",
                    "pau_cl":"pau_cl",
                    "ʔ":"pau_gs",
                    "pʼ":"p_e",
                    "pʰ":"p_h",
                    "ɓ":"b_E",
                    "tʼ":"t_e",
                    "tʰ":"t_h",
                    "lʒ":"_lZ_",
                    "tsʼ":"ts_e",
                    "tʃʼ":"tS_e",
                    "dʒ":"d_0Z",
                    "a":"a",
                    "kʰ":"k_h",
                    "b":"b",
                    "kɬʼ":"kK_e",
                    "ɦ":"h_v",
                    "ǀ":"_c",
                    "d":"d",
                    "ǃ":"_q",
                    "ɛ":"E",
                    "ǁ":"_x",
                    "f":"f",
                    "g":"g",
                    "ǀʰ":"_c_h",
                    "h":"h",
                    "ǃʰ":"_q_h",
                    "ǁʰ":"_x_h",
                    "i":"i",
                    "j":"j",
                    "ɲ":"J",
                    "k":"k",
                    "ɬ":"K",
                    "ǀ̬":"_c_v",
                    "l":"l",
                    "ǃ̬":"_q_v",
                    "m":"m",
                    "n":"n",
                    "ŋ":"N",
                    "ǁ̬":"_x_v",
                    "ɔ":"O",
                    "dz":"dz",
                    "r":"r",
                    "s":"s",
                    "ʃ":"S",
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
        """ Basic Zulu syllabification, based on the syllabification
            scheme by Etienne Barnard for Zulu (Nguni language).
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


class LwaziZuluMultiHTSVoice(LwaziMultiHTSVoice):
    #These are not all strictly conjunctions (some are motivated by
    #simple analysis of pauses between breath groups in the Lwazi2 TTS
    #corpus).
    CONJUNCTIONS = ["ukuti", #that, in order that
                    "kuko", "kumbe", #or either
                    "nokuba", "nakuba", #whether
                    "noko", "kantinoko", #yet, however, notwithstanding, still,
                    "kepa", #but
                    "funa", #lest
                    "ngokuba", #for, because
                    "nxa", "inxa", "umauxa", #if
                    "ngako", #therefore
                    "njengoba", #because; since
                    "kube", "ukube" #that; so that; in order that; if
                    "sase", #and then
                    # the following added based on stats from the Lwazi2 TTS corpus:
                    "noma", #or either (38%)
                    "bese", #and then (65%)
                    "uma", #if (18%)
                    "kufanele", # -fanele + sjnc. or inf. must; need to; have to; ought to; should (40%)
                    "ukuze", #so that; in order that (40%)
                    "futhi", #and (24%)
                    "kanye", #once (34%)
                    "kumele", #represent; stand for (30%)
                    "kodwa", #only, excepting that (50%)
                    "ukuthi", #so that; in order that (3%)
                    "ngoba", #for, because (35%)
                    "kanti", #whereas (50%)
                    "ngaphandle", # ~ kwa-/kuka- apart from; besides; except; without; unless
                                  # ~ kwalokho apart from that; besides; otherwise (32%)
                    "ngaphambi", #ahead; before; in front (33%)
                    "lapho", #when, where (11%)
                    "ukuba", #that; so that; in order that; if (12%)
                    "nokuthi", #and; also; even to say (44%)
                    "ikakhulukazi", "kakhulukazi" #especially; particularly; in particular (60%)
                    "kuze", #so that; in order that (38%)
                    "naye", #and him; and her; even he/him; even she/her; he too; she too; with him; with her (27%)
                    "ngenxa" #~ ya- because of; on behalf of (21%)
                    ]

    def normalizer(self, utt, processname):
        """ words marked with a prepended pipe character "|" and words
            in the English pronunciation dictionary or addendum will
            be marked as English...
        """
        token_rel = utt.get_relation("Token")
        word_rel = utt.new_relation("Word")
        for token_item in token_rel:
            tokentext = token_item["name"]
             #crude morph decomposition based on uppercase in word,
             #inserts dashes (e.g. KwaZulu --> Kwa-Zulu):
            if tokentext.upper() != tokentext and not "-" in tokentext:
                tokentext = re.sub(r'(?<=.)([A-Z])', r'-\1', tokentext)
            tokentext = tokentext.lower()
            #print(tokentext)
            tokentextlist = tokentext.split("-")           #split tokens on dashes to create multiple words...
            for wordname in tokentextlist:
                #tokenizer does NFKD and all pronun resources are in
                #NFC:
                wordname = unicodedata.normalize("NFC", wordname) 
                word_item = word_rel.append_item()
                if wordname.startswith("|"):
                    word_item["lang"] = "eng"
                    wordname = wordname[1:]
                elif (wordname in self.engpronunaddendum or wordname in self.engpronundict) and len(wordname) > 2 and wordname not in self.pronunaddendum:
                    word_item["lang"] = "eng"
                else:
                    word_item["lang"] = "def" #default language...
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
                if word_item is not word_rel.tail_item:
                    if (("postpunc" in token_item and anycharsin(token_item["postpunc"], punctuation)) or
                        word_item.next_item["name"] in LwaziZuluMultiHTSVoice.CONJUNCTIONS):
                        phrase_item = phrase_rel.append_item()
                        phrase_item["name"] = "BB"
        return utt

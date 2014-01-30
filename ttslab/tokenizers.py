# -*- coding: utf-8 -*-
""" Contains tokenizer UttProcessor implementations...

    Think about ways of documenting requirements properly...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import re
import unicodedata
from collections import OrderedDict

from uttprocessor import *


def anycharsin(s, stemplate):
    for c in s:
        if c in stemplate:
            return True
    return False


class DefaultTokenizer(UttProcessor):
    """ Perform basic "tokenization" based on "text" contained in
        Utterance...

        Utt Requirements:
                           Relations: None
                           Features: text

        Provides:
                           Relations: Token
    """
    
    DEFAULT_PUNCTUATION = '"`.,:;!?(){}[]-'

    def __init__(self, voice, punctuation=None):
        UttProcessor.__init__(self, voice=voice)
        
        if punctuation is not None:
            self.punctuation = punctuation
        else:
            self.punctuation = DefaultTokenizer.DEFAULT_PUNCTUATION

        self.processes = {"default": OrderedDict([("checkinput", None),
                                                  ("tokenizer", None)])}

    def checkinput(self, utt, processname):
        if not "text" in utt:
            raise UttProcessorError("Utterance needs to have 'text' feature...")
        return utt

    def tokenizer(self, utt, processname):
        text = utt["text"]
        rawtokens = text.split()  #simply splitting on whitespace...
        token_rel = utt.new_relation("Token")
        for rawtoken in rawtokens: 
            #adding only single char to pre- or post-punctuation...
            if rawtoken[0] in self.punctuation:
                prepunctuation = rawtoken[0]
            else:
                prepunctuation = None
            if rawtoken[-1] in self.punctuation:
                postpunctuation = rawtoken[-1]
            else:
                postpunctuation = None
            #strip all punctuation...
            rawtoken = rawtoken.strip(self.punctuation)
            #if anything left, add to token_rel:
            if rawtoken:
                item = token_rel.append_item()
                item["name"] = rawtoken
                if prepunctuation:
                    item["prepunc"] = prepunctuation
                if postpunctuation:
                    item["postpunc"] = postpunctuation
        return utt



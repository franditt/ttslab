# -*- coding: utf-8 -*-
""" Implements a number of functions used to produce the contextual
    information necessary to create HTS labels for synthesis...
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"


def itempos_inparent_f(item, relation):
    item = item.get_item_in_relation(relation)
    if item is None:
        return 0
    else:
        return item.parent_item.get_daughters().index(item) + 1

def itempos_inparent_b(item, relation):
    item = item.get_item_in_relation(relation)
    if item is None:
        return 0
    else:
        l = item.parent_item.get_daughters()
        return len(l) - l.index(item)


def syllistsylstructrel_inphrase(phraseitem):
    l = []
    for worditem in phraseitem.get_daughters():
        worditem = worditem.get_item_in_relation("SylStructure")
        for sylitem in worditem.get_daughters():
            l.append(sylitem)
    return l

def numsyls_inphrase(phraseitem):
    return len(syllistsylstructrel_inphrase(phraseitem))


def segpos_insyl_f(segitem):
    """ position of the segment in the syllable (forward)
    """
    return itempos_inparent_f(segitem, "SylStructure")

def segpos_insyl_b(segitem):
    """ position of the segment in the syllable (backward)
    """
    return itempos_inparent_b(segitem, "SylStructure")

def sylpos_inword_f(sylitem):
    """ position of the current syllable in the current word (forward)
    """
    return itempos_inparent_f(sylitem, "SylStructure")

def sylpos_inword_b(sylitem):
    """ position of the current syllable in the current word (backward)
    """
    return itempos_inparent_b(sylitem, "SylStructure")


def sylpos_inphrase_f(sylitem):
    """ position of the current syllable in the current phrase (forward)
    """
    sylitem = sylitem.get_item_in_relation("SylStructure")
    try:
        phraseitem = sylitem.traverse("parent.R:Phrase.parent")
    except TraversalError:
        return 0
    syllist = syllistsylstructrel_inphrase(phraseitem)
    return syllist.index(sylitem) + 1


def sylpos_inphrase_b(sylitem):
    """ position of the current syllable in the current phrase (backward)
    """
    sylitem = sylitem.get_item_in_relation("SylStructure")
    try:
        phraseitem = sylitem.traverse("parent.R:Phrase.parent")
    except TraversalError:
        return 0
    syllist = syllistsylstructrel_inphrase(phraseitem)
    return len(syllist) - syllist.index(sylitem)


def numsylsbeforesyl_inphrase(sylitem, feat, featvalue):
    """ the number of syllables before the current syllable in the
        current phrase with 'feat' = 'featvalue'
    """
    sylitem = sylitem.get_item_in_relation("SylStructure")
    try:
        phraseitem = sylitem.traverse("parent.R:Phrase.parent")
    except TraversalError:
        return 0
    syllist = syllistsylstructrel_inphrase(phraseitem)
    idx = syllist.index(sylitem)
    return len([syl for syl in syllist[:idx] if syl[feat] == featvalue])


def numsylsaftersyl_inphrase(sylitem, feat, featvalue):
    """ the number of syllables after the current syllable in the
        current phrase with 'feat' = 'featvalue'
    """
    sylitem = sylitem.get_item_in_relation("SylStructure")
    try:
        phraseitem = sylitem.traverse("parent.R:Phrase.parent")
    except TraversalError:
        return 0
    syllist = syllistsylstructrel_inphrase(phraseitem)
    idx = syllist.index(sylitem)
    return len([syl for syl in syllist[idx+1:] if syl[feat] == featvalue])


def syldistprev(sylitem, feat, featvalue):
    """ the number of syllables from the current syllable to the
        previous syllable with 'feat' = 'featvalue'
    """
    sylitem = sylitem.get_item_in_relation("Syllable")
    count = 1
    nextsyl = sylitem.prev_item 
    while nextsyl:
        if feat in nextsyl:
            if nextsyl[feat] == featvalue:
                return count
        count += 1
        nextsyl = nextsyl.prev_item
    return 0

def syldistnext(sylitem, feat, featvalue):
    """ the number of syllables from the current syllable to the
        next syllable with 'feat' = 'featvalue'
    """
    sylitem = sylitem.get_item_in_relation("Syllable")
    count = 1
    nextsyl = sylitem.next_item 
    while nextsyl:
        if feat in nextsyl:
            if nextsyl[feat] == featvalue:
                return count
        count += 1
        nextsyl = nextsyl.next_item
    return 0


def wordpos_inphrase_f(worditem):
    """ position of the current word in the current phrase (forward)
    """
    worditem = worditem.get_item_in_relation("Phrase")
    phraseitem = worditem.parent_item
    wordlist = phraseitem.get_daughters()
    return wordlist.index(worditem) + 1


def wordpos_inphrase_b(worditem):
    """ position of the current word in the current phrase (backward)
    """
    worditem = worditem.get_item_in_relation("Phrase")
    phraseitem = worditem.parent_item
    wordlist = phraseitem.get_daughters()
    return len(wordlist) - wordlist.index(worditem)


def numwordsbeforeword_inphrase(worditem, feat, featvalue):
    """ the number of words before the current word in the
        current phrase with 'feat' = 'featvalue'
    """
    worditem = worditem.get_item_in_relation("Phrase")
    phraseitem = worditem.parent_item
    wordlist = phraseitem.get_daughters()

    idx = wordlist.index(worditem)
    return len([word for word in wordlist[:idx] if word[feat] == featvalue])


def numsylsaftersyl_inphrase(worditem, feat, featvalue):
    """ the number of words after the current word in the
        current phrase with 'feat' = 'featvalue'
    """
    worditem = worditem.get_item_in_relation("Phrase")
    phraseitem = worditem.parent_item
    wordlist = phraseitem.get_daughters()

    idx = wordlist.index(worditem)
    return len([word for word in wordlist[idx+1:] if word[feat] == featvalue])


def worddistprev(worditem, feat, featvalue):
    """ the number of words from the current words to the
        previous word with 'feat' = 'featvalue'
    """
    worditem = worditem.get_item_in_relation("Word")
    count = 1
    nextword = worditem.prev_item 
    while nextword:
        if feat in nextword:
            if nextword[feat] == featvalue:
                return count
        count += 1
        nextword = nextword.prev_item
    return 0


def worddistnext(worditem, feat, featvalue):
    """ the number of words from the current words to the
        next word with 'feat' = 'featvalue'
    """
    worditem = worditem.get_item_in_relation("Word")
    count = 1
    nextword = worditem.next_item 
    while nextword:
        if feat in nextword:
            if nextword[feat] == featvalue:
                return count
        count += 1
        nextword = nextword.next_item
    return 0


def phrasepos_inutt_f(phraseitem):
    """ position of the current phrase in utterence (forward)
    """
    phraselist = phraseitem.relation.utterance.get_relation("Phrase").as_list()
    return phraselist.index(phraseitem) + 1


def phrasepos_inutt_b(phraseitem):
    """ position of the current phrase in utterence (backward)
    """
    phraselist = phraseitem.relation.utterance.get_relation("Phrase").as_list()
    return len(phraselist) - phraselist.index(phraseitem)



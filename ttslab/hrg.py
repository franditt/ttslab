#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Implementation of the HRG structure....
    Stick to returning None vs. raising Exceptions for the HRG...
"""
from __future__ import unicode_literals, division, print_function #Py2


class DuplicateItemInRelation(Exception):
    pass

class TraversalError(Exception):
    pass


class ItemContent(object):
    """ Stores the actual features of an Item and keeps track of Items
        belonging to specific Relations...

        This class essentially exists so that actual content referred
        to by Items can be shared by Items in different Relations.
    """

    def __init__(self):

        self.features = {}
        self.relations = {}

    
    def add_item_relation(self, item):
        """ Adds the given item to the set of relations. Whenever an
            Item is added to a Relation, it should add the name and
            the Item reference to this set of name/item mappings. This
            allows an Item to find out the set of all Relations that
            it is contained in.
        """
        relationname = item.relation.name
        #two items sharing content are not allowed in the same relation
        if relationname in self.relations:
            raise DuplicateItemInRelation

        self.relations[relationname] = item


    def remove_item(self, item):
        """ Removes Item and deletes self if this was the last Item
            referencing this content...
        """
        del self.relations[item.relation.name]


    def remove(self, remove_dependent_content=False):
        """ This function will remove the ItemContent and all
            dependent Items...
        """
        for relationname in self.relations.keys():
            self.relations[relationname].remove(remove_dependent_content)


    def __str__(self):
        """ Method to sensibly convert object to string lines that can
            be used to print HRG structure from higher levels...
        """
        return "\n".join([repr(self), str(self.features)])



class Item(object):
    """ Represents a node in a Relation...
    """

    def __init__(self, relation, itemcontent):

        self.relation = relation
        self.content = itemcontent
        #update ItemContent to be aware of item in this relation:
        self.content.add_item_relation(self)
        
        self.next_item = None
        self.prev_item = None
        self.parent_item = None

        self.first_daughter = None
        self.last_daughter = None
        
        
    def __eq__(self, item):
        """ Determines if the shared contents of the two items are the
            same.
        """
        return self.content is item.content


    def __ne__(self, item):
        return not self.__eq__(item)


    def __getitem__(self, featname):
        """ Returns the requested feature from itemcontent.
            This raises KeyError when featname is not available..
        """
        return self.content.features[featname]

    
    def __setitem__(self, featname, feat):
        """ Sets the specific feature in itemcontent.
        """
        self.content.features[featname] = feat


    def __delitem__(self, featname):
        """ Deletes the specific feature in itemcontent.
        """
        del self.content.features[featname]

    
    def __iter__(self):
        """ Iterate over features.
        """
        return self.content.features.__iter__()

    def __contains__(self, featname):
        """ Contains feature?
        """
        return featname in self.content.features


    def remove(self, remove_dependent_content=False):
        """ This function serves to remove (delete) the current Item
            and the corresponding ItemContent if no other Items are
            referencing it....
        """

        #fix pointers:
        if self.relation.head_item is self:
            self.relation.head_item = self.next_item
        if self.relation.tail_item is self:
            self.relation.tail_item = self.prev_item

        if self.parent_item:
            if self.parent_item.first_daughter is self:
                self.parent_item.first_daughter = self.next_item
            if self.parent_item.last_daughter is self:
                self.parent_item.last_daughter = self.prev_item

        if self.next_item:
            self.next_item.prev_item = self.prev_item
        if self.prev_item:
            self.prev_item.next_item = self.next_item
        
        #remove daughters:
        for d in self.get_daughters():
            if remove_dependent_content:
                d.remove_content(remove_dependent_content)
            else:
                d.remove()

        #update/remove ItemContent:
        self.content.remove_item(self)



    def remove_content(self, remove_dependent_content=True):
        """ This function will remove the ItemContent and all Items
            sharing...
        """
        self.content.remove(remove_dependent_content)


    def keys(self):
        """ Returns the set of feature keys of this item.
        """
        return self.content.features.keys()


    def _create_related_item(self, item=None):
        """ Create new Item related to self..
        """
        if item is None:
            newitem = Item(self.relation, ItemContent())
        else:
            #create new Item sharing content...
            newitem = Item(self.relation, item.content)

        return newitem


    def add_daughter(self, item=None):
        """ Add the given item as a daughter to this item..
            if item is None then creates new ItemContent...
        """
        newitem = self._create_related_item(item)

        #if first daughter...
        if self.first_daughter is None:
            newitem.prev_item = None
            self.first_daughter = newitem
        else:
            newitem.prev_item = self.last_daughter
            self.last_daughter.next_item = newitem
            
        newitem.parent_item = self
        newitem.next_item = None
        self.last_daughter = newitem

        return newitem


    def append_item(self, item=None):
        """ Appends an item in this list after this item.
        """
        if self.next_item is None:                  #then is last item in containing list...
            if self.parent_item is not None:        #then is daughter..
                newitem = self.parent_item.add_daughter(item)
            else:                                   #then is in relation directly 
                newitem = self.relation.append_item(item)
        else:                                       #is inserted in the middle of list...
            newitem = self._create_related_item(item)

            self.next_item.prev_item = newitem
            newitem.next_item = self.next_item
            self.next_item = newitem
            newitem.prev_item = self
            newitem.parent_item = self.parent_item

        return newitem

    def prepend_item(self, item=None):
        """ Prepends an item in this list before this item.
        """
        newitem = self._create_related_item(item)
                
        if self.prev_item is None:                  #then is first item in containing list...            
            if self.parent_item is not None:        #then is daughter..
                self.parent_item.first_daughter = newitem
            else:                                   #then is in relation directly 
                self.relation.head_item = newitem
        else:                                       #is inserted in the middle of list...            
            self.prev_item.next_item = newitem

        newitem.next_item = self
        newitem.prev_item = self.prev_item          #can be None...
        self.prev_item = newitem
        newitem.parent_item = self.parent_item

        return newitem

    
    def get_item_in_relation(self, relationname):
        """ Finds the item in the given relation that has the same
            shared contents.
        """
        try:
            return self.content.relations[relationname]
        except KeyError:
            return None


    def in_relation(self, relationname):
        """ Returns true if this item has shared contents linked to an
            item in 'relationname'.
        """
        return relationname in self.content.relations

####
# This function originally implemented based on similar function in
# EST/Festival, however 'get_daughters' provides comparable utility
# and I think it might be a good idea to diverge from EST/Festival
# convention of indexing from 1 here anyway.
#
# Might revive this function with indexing from 0 if we want an
# implementation that does not create a new list...
####
    # def get_daughter(self, n=1):
    #     """ Retrieves the nth daughter of this item.
    #     """
    #     if n < 0:
    #         i = 1
    #         item = self.last_daughter
    #         while item is not None:
    #             if n == -i:
    #                 return item
    #             else:
    #                 i += 1
    #                 item = item.prev_item
    #     elif n > 0:
    #         i = 1
    #         item = self.first_daughter
    #         while item is not None:
    #             if n == i:
    #                 return item
    #             else:
    #                 i += 1
    #                 item = item.next_item
    #     else:
    #         return None
    #     return None


    def get_daughters(item):
        """ Constructs a list of daughters of the current Item and
            returns this...
        """
        l = []
        daughter_item = item.first_daughter
        while daughter_item is not None:
            l.append(daughter_item)
            daughter_item = daughter_item.next_item
        return l


    def get_utterance(self):
        """ Returns the utterance associated with this item.
        """
        return self.relation.utterance

    
    def has_daughters(self):
        """ Determines if this item has daughters.
        """
        return bool(self.first_daughter)


    def __str__(self):
        """ A method to sensibly convert object to string lines that
            can be used to print HRG structure from higher levels...
        """
        lines = [repr(self)] + ["\t" + line for line in str(self.content).splitlines()]

        #using get_daughters might actually be faster (because of
        #string concatenation here...
        daughter = self.first_daughter
        while daughter is not None:
            lines.append("\tDaughter:")
            lines += ["\t" + line for line in str(daughter).splitlines()]
            daughter = daughter.next_item

        return "\n".join(lines)


class Relation(object):
    """ Represents an ordered set of Items and their associated
        children.
    """

    def __init__(self, utterance, relationname):

        self.name = relationname
        self.utterance = utterance
        
        self.head_item = None
        self.tail_item = None


    def __iter__(self):
        self.iterstart = True
        return self

    def __next__(self):
        if self.iterstart:
            self.curr_item = self.head_item
            self.iterstart = False
        else:
            self.curr_item = self.curr_item.next_item
        if self.curr_item is None:
            self.iterstart = True
            raise StopIteration
        return self.curr_item

    def __len__(self):
        c = 0
        for i in self:
            c += 1
        return c

### PYTHON2 ###
    def next(self):
        return self.__next__()
### PYTHON2 ###
        
    def append_item(self, item=None):
        """ Adds a new item to this relation.
        """
        if item is None:
            newitem = Item(self, ItemContent())
        else:
            #create new Item sharing content...
            newitem = Item(self, item.content)

        #if head item...
        if self.head_item is None:
            newitem.prev_item = None
            self.head_item = newitem
        else:
            newitem.prev_item = self.tail_item
            self.tail_item.next_item = newitem
            
        newitem.next_item = None
        self.tail_item = newitem

        return newitem


    #we could still implement a prepend_item


    def as_list(self):
        """ Creates a list of Items in this Relation and returns
            this..
        """
        return list(self)


    def __str__(self):
        """ A method to sensibly convert object to string lines that
            can be used to print HRG structure from higher levels...
        """
        lines = [repr(self)]

        item = self.head_item
        
        while item is not None:
            lines.append("\tItem:")
            lines += ["\t" + line for line in str(item).splitlines()]
            item = item.next_item

        return "\n".join(lines)


class Utterance(object):
    """ An Utterance contains a set of Features (essentially a set of
        properties) and a set of Relations.
    """

    def __init__(self, voice=None):
        """ Creates a new, empty utterance.
        """
        self.voice = voice

        self.features = {}
        self.relations = {}

    
    def __getstate__(self):
        """ When pickling, we sever the link to the voice...
        """
        return (self.features, self.relations)

    
    def __setstate__(self, state):
        self.voice = None
        (self.features,
         self.relations) = state

        
    def __getitem__(self, featname):
        """ Returns the requested feature.
            This raises KeyError when featname is not available..
        """
        return self.features[featname]

    
    def __setitem__(self, featname, feat):
        """ Sets the specific feature.
        """
        self.features[featname] = feat


    def __delitem__(self, featname):
        """ Deletes the specific feature.
        """
        del self.features[featname]

    
    def __iter__(self):
        """ Iterate over features.
        """
        return self.features.__iter__()

    def __contains__(self, featname):
        """ Contains feature?
        """
        return featname in self.features


    def new_relation(self, relationname):
        """ Creates a new relation with the given name and adds it to
            this utterance.
        """
        newrelation = Relation(self, relationname)

        self.relations[relationname] = newrelation

        return newrelation
        

    def get_relation(self, relationname):
        """ Retrieves a relation from this utterance.
        """
        try:
            return self.relations[relationname]
        except KeyError:
            return None

   
    def __str__(self):
        """ This is a temporary method to sensibly convert object to
            string lines that can be used to print HRG structure...
        """
        lines = [repr(self), str(self.features)]

        for relationname in self.relations:
            lines.append("\tRelation %s:" % (relationname))
            lines += ["\t" + line for line in str(self.get_relation(relationname)).splitlines()]

        return "\n".join(lines)


# Convenience functions for HRG traversal... should be moved to
# ifuncs.py once pytts.extend has been improved...
############################################################

def first_item(item):
    """ Returns the first item in the list of items linked to
        'item'...
    """
    if item.prev_item:
        return first_item(item.prev_item)
    else:
        return item

def last_item(item):
    """ Returns the last item in the list of items linked to
        'item'...
    """
    if item.next_item:
        return last_item(item.next_item)
    else:
        return item


def traverse(item, pathstring):
    """ pathstring e.g.
        "n.R:SylStructure.parent.p.daughter.last.daughtern.first.F:name"

        TO BE IMPROVED!!! DEMITASSE: this seems to break with special strings (unicode issue...)
    """
    mapping = {"n": ".next_item",
               "p": ".prev_item",
               "parent": ".parent_item",
               "daughter": ".first_daughter",
               "daughtern": ".last_daughter",
               "first": ".first_item()",
               "last": ".last_item()",
               "R": ".get_item_in_relation('%s')",
               "F": "['%s']",
               "M": ".%s"
               }

    pathlist = pathstring.split(".")
    cmdstring = "item"
    for step in pathlist:
        if step.startswith("R:") or step.startswith("F:") or step.startswith("M:"):
            a, b = step.split(":")
            cmdstring += mapping[a] % b
        else:
            cmdstring += mapping[step]

    try:
        return eval(cmdstring)
    except (TypeError, AttributeError, KeyError):
        raise TraversalError


def num_daughters(item):
    count = 0
    daughter_item = item.first_daughter
    while daughter_item is not None:
        count += 1
        daughter_item = daughter_item.next_item
    return count


#extend Item:
#########################
Item.first_item = first_item
Item.last_item = last_item
Item.traverse = traverse
Item.num_daughters = num_daughters


#HRG method shorthand forms:
#############################
#This exists to make interactive work easier (not intended to be used in serious code)..
Item.ad = Item.add_daughter
Item.gd = Item.get_daughters
Item.ai = Item.append_item
Item.pi = Item.prepend_item
Item.ir = Item.in_relation
Item.gir = Item.get_item_in_relation

Relation.al = Relation.as_list
Relation.ai = Relation.append_item

Utterance.gr = Utterance.get_relation


if __name__ == "__main__":
    import hrg
    utt = hrg.Utterance()
    utt["text"] = "mathematics is easy"

    word1 = [['m', 'ae', 'th'], ['ax'], ['m', 'ae'], ['t', 'ih', 'k', 's']]
    word2 = [['ih', 'z']]
    word3 = [['ii'], ['z', 'ih']]

    all_words = [word1, word2, word3]

    wordrel = utt.new_relation("Words")
    sylrel = utt.new_relation("Syllable")
    segmentrel = utt.new_relation("Segment")
    sylstructrel = utt.new_relation("SylStructure")


    # add words
    for word in utt["text"].split():
        tmpitem = wordrel.append_item()
        tmpitem["name"] = word

    # iterate over words
    for i, wordrel_worditem in enumerate(wordrel):
        sylstructrel_worditem = sylstructrel.append_item(wordrel_worditem)
        word = all_words[i]
        for syl in word:
            sylrel_sylitem = sylrel.append_item()
            sylrel_sylitem["name"] = "syl"
            sylstructrel_sylitem = sylstructrel_worditem.add_daughter(sylrel_sylitem)
            for seg in syl:
                segmentrel_segmentitem = segmentrel.append_item()
                segmentrel_segmentitem["name"] = seg
                sylrel_segmentitem = sylstructrel_sylitem.add_daughter(segmentrel_segmentitem)

    print("'name' in tmpitem: ", "name" in tmpitem)
    print("'blah' in tmpitem: ", "blah" in tmpitem)
    print("iterate over featnames in tmpitem:")
    for featname in tmpitem:
        print("\t" + featname + ": " + tmpitem[featname])
    print("deleting 'name'")
    del tmpitem["name"]
    print("'name' in tmpitem: ", "name" in tmpitem)
    print("")
    print(utt)

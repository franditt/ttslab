# -*- coding: utf-8 -*-
"""
    Utilities used by ttslab...
"""
from __future__ import unicode_literals, division, print_function #Py2

try:
    import cPickle as pickle  #Py2
except ImportError:
    import pickle


def extend(cls, module_name):
    exec("import " + module_name)
    funclist = [name for name in eval("dir(%s)" % module_name)
                if eval("str(getattr(%s, '%s'))" % (module_name, name)).startswith("<function ")]
    for funcname in funclist:
        setattr(cls, funcname, eval("getattr(%s, '%s')" % (module_name, funcname)))

def fromfile(fname):
    with open(fname) as infh:
        return pickle.load(infh)

def tofile(obj, fname):
    with open(fname, "w") as outfh:
        pickle.dump(obj, outfh, protocol=2)

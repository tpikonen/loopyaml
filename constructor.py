import types
from yaml.constructor import *
from loopdict import *


def construct_loopdict(self, node):
    yd = SafeConstructor.construct_mapping(self, node, deep=True)
    if yd.has_key('=loop') and yd.has_key('=cols'):
        lvars = yd.pop('=cols')
        ncols = len(lvars)
        P = len(yd['=loop'])
        assert((P % ncols) == 0)
        for i in xrange(ncols):
            ll = [ yd['=loop'][k] for k in xrange(i, P, ncols) ]
            yd[lvars[i]] = ll
        yd.pop('=loop')
        attributes = []
        for k in yd.keys():
            if k.startswith('='):
                if type(yd[k]) == types.ListType and len(yd[k]) == len(lvars):
                    vals = yd.pop(k)
                    attname = k[1:]
                    attributes.append(attname)
                    for i in xrange(len(lvars)):
                        yd[lvars[i]+attname] = vals[i]
        return Loopdict(yd, lvars, attributes)
    else:
        return yd

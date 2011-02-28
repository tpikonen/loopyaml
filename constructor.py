from yaml.constructor import *
from loopdict import *


def construct_loopdict(self, node):
    yd = SafeConstructor.construct_mapping(self, node, deep=True)
    if yd.has_key('=loop') and yd.has_key('=cols'):
        lvars = yd['=cols']
        ncols = len(lvars)
        P = len(yd['=loop'])
        assert((P % ncols) == 0)
        for i in xrange(ncols):
            ll = [ yd['=loop'][k] for k in xrange(i, P, ncols) ]
            yd[lvars[i]] = ll
        yd.pop('=loop')
        yd.pop('=cols')
        return Loopdict(yd, lvars)
    else:
        return yd

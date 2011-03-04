import types
from yaml.constructor import *
from loopdict import *


class LoopConstructor(Constructor):

    def __init__(self):
        Constructor.__init__(self)


def construct_loopdict(self, node):
    yd = SafeConstructor.construct_mapping(self, node, deep=True)
    looped = False
    try:
        looped = yd['=loops='][0].has_key('$cols') \
            and yd['=loops='][0].has_key('~vals')
    except KeyError:
        pass
    except TypeError:
        pass
    if not looped:
        return yd

    lseq = yd.pop('=loops=')
    loops = []
    for loop in lseq:
        try:
            lvars = loop.pop('$cols')
            vals = loop.pop('~vals')
            ncols = len(lvars)
            P = len(vals)
            assert((P % ncols) == 0)
            for i in xrange(ncols):
                ll = [ vals[k] for k in xrange(i, P, ncols) ]
                yd[lvars[i]] = ll
            attributes = []
            for k in loop.keys():
                if k.startswith('+'):
                    if type(loop[k]) == types.ListType and \
                        len(loop[k]) == len(lvars):
                        vals = loop.pop(k)
                        attname = k[1:]
                        attributes.append(attname)
                        for i in xrange(len(lvars)):
                            yd[lvars[i]+attname] = vals[i]
            loops.append((lvars, attributes))
        except KeyError:
            yd['=loops='] = loop['=loops=.orig']
    return Loopdict(yd, loops=loops)


LoopConstructor.add_constructor(
        u'tag:yaml.org,2002:map',
        construct_loopdict)

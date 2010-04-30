import types

class Loopdict(dict):
    """Dictionary which can be serialized with YAML loop notation.

    The looped keys are given in the loopvars list. The values
    of the looped keys must be lists of equal length.
    """
    def __init__(self, d, loopvars=[]):
        for k in loopvars:
            if not d.has_key(k) or not type(d[k]) is types.ListType:
                raise ValueError
        if loopvars:
            l0 = len(d[loopvars[0]])
            for k in loopvars:
                if len(d[k]) != l0:
                    raise ValueError
        self.loopvars = loopvars
        dict.__init__(self, d)
    def __repr__(self):
        return "Loopdict(%s, loopvars=%s)" % \
            (dict.__repr__(self), self.loopvars.__repr__())

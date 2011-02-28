import types

class Loopdict(dict):
    """A dictionary which can be serialized with YAML loop notation.

    The looped keys are given in the list `loopvars`. The values
    of the looped keys must be lists of floats of equal length.

    `attributes` is a list of extensions to `loopvars` variable names.
    Variable names of the form `loopvars[i]`+`attributes[j]` (for all
    i and j) in the dictionary are written to lists keyed by the
    attribute.

    The elements of `loopvars` and `attributes` lists must be strings.
    """
    def __init__(self, d, loopvars=[], attributes=[]):
        for k in loopvars:
            assert(type(k) == types.StringType)
            if not d.has_key(k) or not type(d[k]) is types.ListType:
                raise ValueError
        if loopvars:
            l0 = len(d[loopvars[0]])
            for k in loopvars:
                if len(d[k]) != l0:
                    raise ValueError("Looping variables must be lists of equal lenght.")
        for att in attributes:
            assert(type(att) == types.StringType)
        self.loopvars = loopvars
        self.attributes = attributes
        dict.__init__(self, d)
    def __repr__(self):
        return "Loopdict(%s, loopvars=%s, attributes=%s)" % \
            (dict.__repr__(self), self.loopvars.__repr__(), \
            self.attributes.__repr__())

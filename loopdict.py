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
    def __init__(self, d, loopvars=[], attributes=[], loops=[]):
        dict.__init__(self)
        self.loops = []
        self.update(d, loopvars, attributes)
        for loop in loops:
            self.update({}, loop[0], loop[1])


    def __repr__(self):
        return "Loopdict(%s, loops=%s)" % \
            (dict.__repr__(self), self.loops.__repr__())


    def update(self, d, *args, **kwargs):
        dict.update(self, d, **kwargs)
        loopvars = args[0]
        attributes = args[1]
        for k in loopvars:
            assert(type(k) == types.StringType)
            if not self.has_key(k):
                raise ValueError("Value for key '%s' not found." % k)
            if not type(self[k]) is types.ListType:
                raise ValueError("Looping variable values must be lists.")
        if loopvars:
            l0 = len(self[loopvars[0]])
            for k in loopvars:
                if len(self[k]) != l0:
                    raise ValueError("Looping variables must be lists of equal length.")
        for att in attributes:
            assert(type(att) == types.StringType)
        if loopvars:
            self.loops.append((loopvars, attributes))

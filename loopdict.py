import types

class Loopdict(dict):
    """A dictionary which can be serialized with YAML loop notation.

    The looped keys and attributes are given either in the keyword
    arguments `loopvars` and `attributes` as lists, or, if more
    than one loop is desired, in the keyword argument `loops` as a
    list of 2-tuples which contain the loopvars and attributes lists
    (e.g. loops=[(loopvars1, attrs1), (loopvars1, attrs2)]).

    The `loopvars` list gives the keys in the dictionary which
    are looped in the YAML output. The values of the looped keys
    must be lists of floats of equal length.

    The `attributes` list contains extensions to `loopvars`
    variable names, which are output as scalar attributes in the
    tabular output. Keys of the form `loopvars[i]`+`attributes[j]`
    (for all i and j) should exist in the dictionary.

    The elements of `loopvars` and `attributes` lists must be strings
    (i.e. other allowed types for Dict keys such as floats will not
    work.)
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

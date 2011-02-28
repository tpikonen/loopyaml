import yaml.constructor
from yaml import *
from dumper import LoopDumper
from loopdict import *
from constructor import construct_loopdict


# Fix functions imported from yaml to use the LoopDumper class.
def replace_dumper(f):
    def repfun(*args, **kwargs):
        if not kwargs.has_key("Dumper"):
            kwargs['Dumper'] = LoopDumper
        return f(*args, **kwargs)
    repfun.__doc__ = f.__doc__
    return repfun


emit                  = replace_dumper(emit)
serialize_all         = replace_dumper(serialize_all)
serialize             = replace_dumper(serialize)
dump_all              = replace_dumper(dump_all)
dump                  = replace_dumper(dump)
add_implicit_resolver = replace_dumper(add_implicit_resolver)
add_path_resolver     = replace_dumper(add_path_resolver)
add_representer       = replace_dumper(add_representer)
add_multi_representer = replace_dumper(add_multi_representer)


yaml.constructor.Constructor.add_constructor(
        u'tag:yaml.org,2002:map',
        construct_loopdict)

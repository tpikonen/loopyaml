from yaml.reader import *
from yaml.scanner import *
from yaml.parser import *
from yaml.composer import *
from yaml.resolver import *
from constructor import *

class LoopLoader(Reader, Scanner, Parser, Composer, LoopConstructor, Resolver):

    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        LoopConstructor.__init__(self)
        Resolver.__init__(self)


import loopyaml

def test_multiloop():
    dd = {
        'I': [2.0, 2.0],
        'Ierr': [3.0, 3.0],
        'q': [1.0, 1.0],
        'I~unit' : 'arb.',
        'Ierr~unit' : 'arb.',
        'q~unit' : '1/nm',
        'bI': [2.0, 2.0],
        'bIerr': [3.0, 3.0],
        'bq': [1.0, 1.0],
        'bI~unit' : 'arb.',
        'bIerr~unit' : 'arb.',
        'bq~unit' : '1/nm'
        }
    lvars = ['q', 'I', 'Ierr']
    attrs = ['~unit']
    blvars = ['bq', 'bI', 'bIerr']
    battrs = ['~unit']
    ld = loopyaml.Loopdict(dd, loops=[(lvars, attrs), (blvars, battrs), (lvars, attrs)])
    ss = loopyaml.dump(ld)
#    print(ss)
    lread = loopyaml.load(ss)
#    print(lread)
    assert(ld == lread) # FIXME: Is this really recursive value equality test?


def test_loops_key():
    dd = {
        'I': [2.0, 2.0],
        'Ierr': [3.0, 3.0],
        'q': [1.0, 1.0],
        '=loops=' : "true",
    }
    lvars = ['q', 'I', 'Ierr']
    ld = loopyaml.Loopdict(dd, lvars)
    ss = loopyaml.dump(ld)
#    print(ss)
    lread = loopyaml.load(ss)
    assert(ld == lread) # FIXME: Is this really recursive value equality test?


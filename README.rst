LoopYAML
========

Introduction
------------

LoopYAML is a Python module which adds the concept of looped data
arrays to the YAML_ data serialization format. Looped arrays are in
practice tabular arrays, where rows group together values of different
types found in columns. The concept was inspired by the STAR_ file
format and it's implementation in Crystallographic_Information_File_.

The implementation of this module is more than a little bit hackish,
importing the loopyaml module causes the import of the yaml module
(PyYAML_, to be exact), which is then monkey patched to serialize the
Python class LoopDict in a tabular format in the output YAML file.

The LoopDict object inherits from Dict and is serialized like YAML
map, except for the keys which are marked to belong to a loop. See
the LoopDict docstring for details.

.. _YAML: http://yaml.org
.. _STAR: http://pubs.acs.org/doi/abs/10.1021/ci00002a020
.. _Crystallographic_Information_File: http://www.iucr.org/__data/iucr/cif/standard/cifstd4.html
.. _PyYAML: http://pyyaml.org/

Example usage
-------------

 >>> import loopyaml as ly
 >>> dd = { 'Date': '2011-01-01', 'I': [2.0, 2.0], 'Ierr': [3.0, 3.0], 'q': [1.0, 1.0], 'I~unit' : 'arb.', 'Ierr~unit' : 'arb.', 'q~unit' : '1/nm'}
 >>> loopd = ly.Loopdict(dd, loopvars=['q', 'I', 'Ierr'], attributes=['~unit'])
 >>> print(ly.dump(loopd))
 Date: '2011-01-01'
 =loops=:
 - $cols: [q, I, Ierr]
   +~unit: [1/nm, arb., arb.]
   ~vals: !!seq [
     1.0000000000e+00, 2.0000000000e+00, 3.0000000000e+00,
     1.0000000000e+00, 2.0000000000e+00, 3.0000000000e+00,
   ]
 <BLANKLINE>

License
-------

LoopYAML is based on PyYAML, which is copyright by Kirill Simonov.
Like PyYAML, LoopYAML is licensed under the MIT license:

Copyright © 2010-2011 Paul Scherrer Institute (http://www.psi.ch/)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Author
------

Teemu Ikonen <tpikonen@gmail.com>.

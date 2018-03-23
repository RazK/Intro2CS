from autotest import TestSet

from importlib import import_module
import sys
from io import StringIO

import testrunners

def null_print_runner(modulename, fname, args=[], kwargs={}, options={},tname=''):
    try:
        _stdout = sys.stdout
        tmpout = StringIO()
        sys.stdout = tmpout
        import_module(modulename) # sHould print output
        res = tmpout.getvalue()
        return None,res
    finally:
        sys.stdout = _stdout

defaults = {'modulename':'hello',
            'fname':None,
            'runner':null_print_runner,
        }

cases = {'hello':{'ans':['Hello World!\n'],
              },
     }

tsets = {'ex0':TestSet({},cases),
}

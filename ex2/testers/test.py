#!/usr/bin/env python3

from sys import argv
from importlib import import_module
import operator as op

from autotest import mp_test,res_code,TestSet
import autotest as at
import testrunners

# Setting levels:
# Global
# Exercise
# Set
# Test

class FakeException(Exception):
    pass

def diff_str(intro,exp,act):
    return "\n".join([intro+":",
                      "expected: "+str(exp),
                      "actual:   "+str(act)])

global_defaults = {'timeout':4,
                   'comparemethod':op.eq,
                   'runner':testrunners.import_runner,
                   'args':[],
                   'kwargs':{},
                   'ans':[None],
                   'options':{},
               }
def run_all_tests(testfile):
    testmodule = import_module(testfile)
    defaults = global_defaults.copy()
    defaults.update(testmodule.defaults)

    for name,data in testmodule.tsets.items():
        test_sets(name, data, defaults)

def test_sets(name, data, moddefaults):
    defaults = moddefaults.copy()
    defaults.update(data.defaults)

    def getarg(key):
        try:
            return val[key]
        except KeyError:
            return defaults[key]

    correct=0
    for key,val in data.testcases.items():
        tname = '_'.join([name,str(key)])

        try:
            runner = getarg('runner')
            timeout = getarg('timeout')
            modulename = getarg('modulename')
            fname = getarg('fname')
            args = getarg('args')
            ans = getarg('ans')
            comparemethod = getarg('comparemethod')
            kwargs = getarg('kwargs')
            options = getarg('options')
            code,res = mp_test(runner,[modulename,fname,args,kwargs,options],{"tname":tname}, timeout=timeout)

            if code:
                res_code(tname, code, res)
                continue
            if any(comparemethod(a, res) for a in ans):
                correct+=1
                continue
            else:
                res_code(tname, "wrong",diff_str("Wrong result, input: "+str(args),ans[0],res))

        except at.Error as e:
            res_code(tname, e.code, e.message)
            continue
        except Exception as e:
            res_code(tname, "testingFailed", e.__repr__())
            continue

    res_code(name, str(correct))
                                                            
if __name__=="__main__":

    run_all_tests(argv[1])

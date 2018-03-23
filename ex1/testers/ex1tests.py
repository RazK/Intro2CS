from autotest import TestSet

import testrunners

defaults = {'modulename':'math_print',}

cases = {'golden':{'fname':'golden_ratio',
               'runner':testrunners.print_runner,
               'ans':["1.618033988749895\n"],
           },
         'square5':{'fname':'square_five',
               'runner':testrunners.print_runner,
               'ans':["25\n",
                      "25.0\n",],
           },
         'hypot':{'fname':'hypotenuse',
               'runner':testrunners.print_runner,
               'ans':["6.4031242374328485\n",
                      "6.403124237432849\n",],
           },
         'pi':{'fname':'pi',
               'runner':testrunners.print_runner,
               'ans':["3.141592653589793\n"],
           },
         'e':{'fname':'e',
               'runner':testrunners.print_runner,
               'ans':["2.718281828459045\n"],
           },
         'areas':{'fname':'squares_area',
               'runner':testrunners.print_runner,
               'ans':["1 4 9 16 25 36 49 64 81 100\n",
                      "1.0 4.0 9.0 16.0 25.0 36.0 49.0 64.0 81.0 100.0\n",],
           },
     }

tsets = {'ex1':TestSet({},cases),
}

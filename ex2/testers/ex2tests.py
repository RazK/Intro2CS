from autotest import TestSet

import testrunners

defaults = {}

p1 = {'spooncup':{'modulename':'convert_spoon_to_cup',
                  'fname':'convert_spoon_to_cup',
                  'args':[7],'ans':[2.0],
              },
      'bmi1':{'modulename':'bmi',
              'fname':'is_normal_bmi',
              'args':[65,1.7],'ans':[True],
          },
      'bmi2':{'modulename':'bmi',
              'fname':'is_normal_bmi',
              'args':[75,1.7],'ans':[False],
          }
  }


c1_def = {'modulename':'calculate_mathematical_expression',
          'fname':'calculate_mathematical_expression',}
c1 = {'add_6_5':{'args':[6,5,'+'],'ans':[11],},
      'sub_10_6':{'args':[10,6,'-'],'ans':[4],},
      'mult_6_5':{'args':[6,5,'*'],'ans':[30],},
      'div_5_4':{'args':[5,4,'/'],'ans':[1.25],},
      'div_10_2':{'args':[10,2,'/'],'ans':[5.0],},
      'div_1_0':{'args':[1,0,'/'],'ans':[None],},
      'mod_6_4':{'args':[6,4,'%'],'ans':[None],},
  }

c2_def = {'modulename':'calculate_mathematical_expression',
          'fname':'calculate_from_string',}
c2 = {'sub_2_7':{'args':['2 - 7'],'ans':[-5.0],},
      'sub_7_2':{'args':['7 - 2'],'ans':[5.0],},
      'sub_4_10':{'args':['4 / 10'],'ans':[0.4],},
      'sub_10_4':{'args':['10 / 4'],'ans':[2.5],},
  }

ls_def = {'modulename':'largest_and_smallest',
          'fname':'largest_and_smallest',}

ls = {'ls_1_5_10':{'args':[1,5,10],'ans':[(10,1)],},
      'ls_10_1_5':{'args':[10,1,5],'ans':[(10,1)],},
      'ls_1_1_2':{'args':[1,1,2],'ans':[(2,1)],},
      'ls_0_0_0':{'args':[0,0,0],'ans':[(0,0)],},
  }

qu_def = {'modulename':'quadratic_equation',}


qu = {'qu2':{'fname':'quadratic_equation',
             'args':[1,1.5,-1],'ans':[(-2,0.5),(0.5,-2)],},
      'qu1':{'fname':'quadratic_equation',
             'args':[1,-8,16],'ans':[(4,None)],},
      'qu0':{'fname':'quadratic_equation',
             'args':[1,-2,34.5],'ans':[(None,None)],},
      'quui2':{'fname':'quadratic_equation_user_input',
               'runner':testrunners.print_runner,
               'options':{'input':'1 -8 15\n'},
               'ans':["Insert coefficients a, b, and c: The equation has 2 solutions: 5.0 and 3.0\n",
                      "Insert coefficients a, b, and c: The equation has 2 solutions: 3.0 and 5.0\n",],
           },
      'quui1':{'fname':'quadratic_equation_user_input',
               'runner':testrunners.print_runner,
               'options':{'input':'1 -8 16\n'},
               'ans':["Insert coefficients a, b, and c: The equation has 1 solution: 4.0\n"],
           },
      'quui0':{'fname':'quadratic_equation_user_input',
               'runner':testrunners.print_runner,
               'options':{'input':'1 1 1\n'},
               'ans':["Insert coefficients a, b, and c: The equation has no solutions\n"],
           },
      }

sh_output='Choose shape (1=circle, 2=rectangle, 3=trapezoid): '

sh_def = {'modulename':'shapes',
          'fname':'shape_area',}
sh = {'circ':{'options':{'input':'1\n5\n','output':sh_output},
              'ans':[78.53981633974483],
          },
      'rect':{'options':{'input':'2\n5\n6\n','output':sh_output},
              'ans':[30.0],
          },
      'trap':{'options':{'input':'3\n9\n11\n10\n','output':sh_output},
              'ans':[100.0],
          },
      'none':{'options':{'input':'4\n','output':sh_output},
              'ans':[None],
          },
  }


tsets = {'conv':TestSet({},p1),
         'calcmath':TestSet(c1_def,c1),
         'calcstr':TestSet(c2_def,c2),
         'maxmin':TestSet(ls_def,ls),
         'quad':TestSet(qu_def,qu),
         'shape':TestSet(sh_def,sh),
     }

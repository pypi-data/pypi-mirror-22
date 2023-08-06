from unittest import TestCase
import unittest
from collections import OrderedDict
import numpy as np
from ScoreCardModel.feature_selection.weight_of_evidence import Woe
from ScoreCardModel.utils.discretization.sharing import discrete


X = np.array([[91, 91, 91],
                  [16, 16, 16],
                  [43, 43, 43],
                  [13, 13, 13],
                  [81, 81, 81],
                  [91, 91, 91],
                  [90, 90, 90],
                  [4,  4,  4],
                  [28, 28, 28],
                  [63, 63, 63],
                  [87, 87, 87],
                  [36, 36, 36],
                  [33, 33, 33],
                  [96, 96, 96],
                  [23, 23, 23],
                  [74, 74, 74],
                  [64, 64, 64],
                  [33, 33, 33],
                  [84, 84, 84],
                  [99, 99, 99],
                  [89, 89, 89],
                  [48, 48, 48],
                  [9,  9,  9],
                  [8,  8,  8],
                  [34, 34, 34],
                  [17, 17, 17],
                  [31, 31, 31],
                  [39, 39, 39],
                  [65, 65, 65],
                  [98, 98, 98],
                  [90, 90, 90],
                  [36, 36, 36],
                  [41, 41, 41],
                  [57, 57, 57],
                  [29, 29, 29],
                  [83, 83, 83],
                  [79, 79, 79],
                  [85, 85, 85],
                  [56, 56, 56],
                  [40, 40, 40],
                  [12, 12, 12],
                  [95, 95, 95],
                  [59, 59, 59],
                  [26, 26, 26],
                  [38, 38, 38],
                  [88, 88, 88],
                  [5,  5,  5],
                  [53, 53, 53],
                  [20, 20, 20],
                  [86, 86, 86],
                  [50, 50, 50],
                  [36, 36, 36],
                  [74, 74, 74],
                  [51, 51, 51],
                  [10, 10, 10],
                  [63, 63, 63],
                  [17, 17, 17],
                  [11, 11, 11],
                  [47, 47, 47],
                  [15, 15, 15],
                  [47, 47, 47],
                  [88, 88, 88],
                  [34, 34, 34],
                  [46, 46, 46],
                  [1,  1,  1],
                  [52, 52, 52],
                  [71, 71, 71],
                  [22, 22, 22],
                  [49, 49, 49],
                  [67, 67, 67],
                  [93, 93, 93],
                  [11, 11, 11],
                  [71, 71, 71],
                  [2,  2,  2],
                  [90, 90, 90],
                  [68, 68, 68],
                  [25, 25, 25],
                  [52, 52, 52],
                  [3,  3,  3],
                  [79, 79, 79],
                  [50, 50, 50],
                  [33, 33, 33],
                  [35, 35, 35],
                  [2,  2,  2],
                  [42, 42, 42],
                  [37, 37, 37],
                  [69, 69, 69],
                  [24, 24, 24],
                  [52, 52, 52],
                  [29, 29, 29],
                  [43, 43, 43],
                  [38, 38, 38],
                  [71, 71, 71],
                  [99, 99, 99],
                  [50, 50, 50],
                  [41, 41, 41],
                  [84, 84, 84],
                  [27, 27, 27],
                  [80, 80, 80],
                  [17, 17, 17]])
tag = np.array([False,  True, False, False, False,  True, False, False,  True,
                    True, False,  True, False, False,  True,  True,  True,  True,
                    False,  True,  True,  True,  True, False,  True, False,  True,
                    True,  True,  True, False,  True,  True, False, False,  True,
                    False, False, False, False, False,  True,  True,  True, False,
                    False, False,  True,  True, False,  True, False,  True, False,
                    False, False,  True,  True, False, False,  True,  True, False,
                    True,  True,  True, False,  True,  True,  True,  True, False,
                    True,  True, False,  True, False,  True,  True, False, False,
                    True, False, False, False,  True, False, False, False,  True,
                    False, False,  True, False, False, False, False,  True, False, False])
woe = {'0': {1: -0.040037373059837185,
                 2: 0.040005334613699206,
                 3: 0.44547044272186359,
                 4: -0.42999829463203643},
           '1': {1: -0.040037373059837185,
                 2: 0.040005334613699206,
                 3: 0.44547044272186359,
                 4: -0.42999829463203643},
           '2': {1: -0.040037373059837185,
                 2: 0.040005334613699206,
                 3: 0.44547044272186359,
                 4: -0.42999829463203643}}
iv = OrderedDict([('0', 0.096952767841102516),
                      ('1', 0.096952767841102516),
                      ('2', 0.096952767841102516)])

call = OrderedDict([('0',
                         {'iv': 0.096952767841102516,
                          'woe': {1: -0.040037373059837185,
                                  2: 0.040005334613699206,
                                  3: 0.44547044272186359,
                                  4: -0.42999829463203643}}),
                        ('1',
                         {'iv': 0.096952767841102516,
                          'woe': {1: -0.040037373059837185,
                                  2: 0.040005334613699206,
                                  3: 0.44547044272186359,
                                  4: -0.42999829463203643}}),
                        ('2',
                         {'iv': 0.096952767841102516,
                          'woe': {1: -0.040037373059837185,
                                  2: 0.040005334613699206,
                                  3: 0.44547044272186359,
                                  4: -0.42999829463203643}})])

class TestWoe_invalid(TestCase):

    #@unittest.skip
    def test_invalid_label_len(self):
        with self.assertRaisesRegex(AttributeError,r"label must have the same len with the features' number"):
            woe = Woe(X,tag,label = ["a","b"])
    #@unittest.skip
    def test_invalid_discrete_len(self):
        with self.assertRaisesRegex(AttributeError,r"discrete method list must have the same len with the features' number"):
            woe = Woe(X,tag, discrete = [(discrete,),(discrete,)])
    #@unittest.skip
    def test_invalid_discrete_args_len(self):
        with self.assertRaisesRegex(AttributeError,r"discrete argument must a tuple of the objects :func,args"):
            woe = Woe(X,tag,discrete = (discrete,{"n":4},2))
            woe.iv



class TestWoe(TestCase):

    def test_iv(self):
        woe1 = Woe(X,tag,discrete = (discrete,{'n':4}))

        for i,v in iv.items():
            self.assertAlmostEquals(woe1.iv.get(i),v, places = 4)


    def test_woe(self):
        woe1 = Woe(X,tag,discrete = (discrete,{'n':4}))
        for i,v in woe.items():
            for j,k in v.items():
                self.assertAlmostEquals(woe1.woe.get(i).get(j),k, places = 4)

    def test_call(self):
        woe1 = Woe(X,tag,discrete = (discrete,{'n':4}))
        ca = woe1()
        for i,v in call.items():
            set(v.keys()) == set(ca.get(i).keys())

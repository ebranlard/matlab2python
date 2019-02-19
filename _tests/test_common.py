import unittest
import sys
import os
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from matlabparser import *
from matlabparser.parser import TestParser
from matlabparser.parsing_tools import TestParsingTools
from matlabparser.parser import matlablines2python

class TestCommon(unittest.TestCase):
    pass
   # def test_common(self):
   #     print('hi')
    #def assertEqual(self, first, second, msg=None):
    #    #print('>',first,'<',' >',second,'<')
    #    super(TestCommon, self).assertEqual(first, second, msg)
    #
    #def test_unit(self):
    #    self.assertEqual(unit   ('speed [m/s]'),'m/s'  )
    #    self.assertEqual(unit   ('speed [m/s' ),'m/s'  ) # ...
    #    self.assertEqual(no_unit('speed [m/s]'),'speed')
    #
    #def test_ellude(self):
    #    self.assertListEqual(ellude_common(['AAA','ABA']),['A','B'])

    #    # unit test for #25
    #    S=ellude_common(['A.txt','A_.txt'])
    #    if any([len(s)<=1 for s in S]):
    #        raise Exception('[FAIL] ellude common with underscore difference, Bug #25')

# --------------------------------------------------------------------------------}
# ---  
# --------------------------------------------------------------------------------{
class TestMatlab2Python(unittest.TestCase):

    def ExecAsserX(self, Lines, Expected, msg=None):
        #print('>',first,'<',' >',second,'<')
        A=matlablines2python(Lines)
        print(A)
        d={}
        exec(A,d)
        np.testing.assert_array_equal(d['x'], Expected)

    def test_string(self):
        # strings
        self.ExecAsserX("""x=strrep('foo','o','a')"""  ,'faa')

    def test_numpy(self):
        # simple
        self.ExecAsserX("""x=1""",1)
        self.ExecAsserX("""x=ceil(0.5)""",1)
        # linspace
        self.ExecAsserX("""x=linspace(0,1,2)""",[0,1])
        self.ExecAsserX("""x=linspace(0,1,3)""",[0,0.5,1])
        #zeros, ones, nan
        self.ExecAsserX("""x=zeros(3,2)""",np.zeros((3,2)))
        self.ExecAsserX("""x=ones(3)"""   ,np.ones((3,3)))
        self.ExecAsserX("""x=nan(3,2)"""  ,np.full([3,2],np.nan))
        #reshape,eye
        self.ExecAsserX("""x=reshape(eye(1,2),[2,1])"""  ,np.array([[1],[0]]))
        #repmat
        self.ExecAsserX("""x=repmat([1,2],1,2)"""  ,np.array([[1,2,1,2]]))
        #sum
        self.ExecAsserX("""x=sum([1,2])"""  ,3)
        self.ExecAsserX("""x=sum(eye(1,2),2)""",1)
        self.ExecAsserX("""x=sum(eye(1,2),1)""",[1,0])

        print('>>>>>>>>>>')
        print('>>>>>>>>>>')
        #self.Eval(""" """)
 
if __name__ == '__main__':
    unittest.main()

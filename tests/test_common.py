import unittest
import sys
import os
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from matlabparser import *
from matlabparser.parser import matlablines2python

# --------------------------------------------------------------------------------}
# ---  
# --------------------------------------------------------------------------------{
class TestMatlab2Python(unittest.TestCase):

    def ExecAsserX(self, Lines, Expected, msg=None):
        #print('>',first,'<',' >',second,'<')
        A=matlablines2python(Lines)
        #print('')
        #print('Matlab:',Lines)
        #print('Python:',A)
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
        self.ExecAsserX("""x=floor(10/2)""",5)
        self.ExecAsserX("""x=floor(11/2)""",5)
        self.ExecAsserX("""x=floor(12/2)""",6)
        # linspace
        self.ExecAsserX("""x=linspace(0,1,2)""",[0,1])
        self.ExecAsserX("""x=linspace(0,1,3)""",[0,0.5,1])
        self.ExecAsserX("""x=0:0.5:1""",[0,0.5,1])
        self.ExecAsserX("""x=0:3""",[0,1,2,3])
        self.ExecAsserX("""x=3:-1:1""",[3,2,1])
        self.ExecAsserX("""x=1:-0.5:0""",[1,0.5,0])
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

        #print('>>>>>>>>>>')
        #print('>>>>>>>>>>')
        #self.Eval(""" """)
 
if __name__ == '__main__':
    unittest.main()

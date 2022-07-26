import unittest
import sys
import os
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from matlabparser import *
from matlabparser import parser as mparser

# --------------------------------------------------------------------------------}
# --- Convert matlab files to python files
# --------------------------------------------------------------------------------{

class options:
    def __init__(self,output=None):
        self.numbers=False
        self.no_comments=False
        self.no_resolve=False
        self.smop=False
        self.output=output


def remove(pyFile):
    try:
        os.remove(pyFile)
    except:
        pass

def convert(mfile, prefix='_'):
    """
    Convert the input file mfile to a python file. 
    The python file is placed in the same directory as the mfile, but with an underscore before.
    The underscore ensures that the file is ignored by git.
    """
    pyFilename = os.path.join(os.path.dirname(mfile),prefix+os.path.basename(mfile).replace('.m','.py'))
    opts = options(pyFilename)
    #print('>>>>>> Converting:',mfile, opts)
    #     opts.smop=True
    mparser.matlab2python(mfile,opts)

    return pyFilename

class TestMatlab2Python(unittest.TestCase):

    def test_runfile(self):
        pyFilename = convert('tests/files/run_all.m')
        remove(pyFilename)

    def test_spectrum(self):
        # Convert to python
        pyFilename = convert('tests/files/fSpectrum.m')

        # Open the file generated 
        from tests.files._fSpectrum import fSpectrum 
        dt = 0.1
        t = np.arange(0,1+dt,dt)
        y = np.sin(t)
        # TODO does not work yet
        #S,f = fSpectrum(y,len(y),1 / dt)
        S_ref = np.array([0.2285364,0.0258482,0.0066528,0.0033719,0.0023203,0.0019575])
        f_ref = np.array([0.0,0.90909,1.81818,2.72727,3.63636,4.54545])
        #print(S-S_ref)
        #print(f-f_ref)

        # Clean up
        remove(pyFilename)

    def test_class(self):
        # Convert to python
        pyFilename = convert('tests/files/test_class1.m')

        # Open the file generated and test the class
        from tests.files._test_class1 import MyClass

        obj = MyClass()
        self.assertEqual(obj.prop_priv, -1)

        obj.read(value=12)
        self.assertEqual(obj.prop_pub, 12)
        self.assertEqual(obj.prop_priv, 3)

        # Clean up
        remove(pyFilename)
 
if __name__ == '__main__':
    unittest.main()

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

def convert(mfile):
    opts = options(mfile.replace('.m','.py'))
    #print('>>>>>>')
    #print('>>>>>> Converting:',mfile)
    #     opts.smop=True
    mparser.matlab2python(mfile,opts)

def compare_to_ref(mfile):
    opts = options(mfile.replace('.m','.py'))
    ref_output =mfile.replace('.m','_ref.py')
    #print('>>>>>> Converting:',mfile)
    mparser.matlab2python(mfile,opts)
    #print('>>>>>>')

class TestMatlab2Python(unittest.TestCase):


    def test_spectrum(self):
        convert('_tests/files/run_all.m')
        compare_to_ref('_tests/files/fSpectrum.m')


# --------------------------------------------------------------------------------}
# --- Try to run the converted files  
# --------------------------------------------------------------------------------{

class TestZAllConverted(unittest.TestCase):
    def test_Zspectrum(self):
        import _tests.files
        from _tests.files.fSpectrum import fSpectrum 
        dt = 0.1
        t = np.arange(0,1+dt,dt)
        y = np.sin(t)
        #S,f = fSpectrum(y,len(y),1 / dt)
        S_ref = np.array([0.2285364,0.0258482,0.0066528,0.0033719,0.0023203,0.0019575])
        f_ref = np.array([0.0,0.90909,1.81818,2.72727,3.63636,4.54545])
        #print(S-S_ref)
        #print(f-f_ref)



 
if __name__ == '__main__':
    unittest.main()

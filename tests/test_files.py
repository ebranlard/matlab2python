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
    output = os.path.join(os.path.dirname(mfile),'_'+os.path.basename(mfile).replace('.m','.py'))
    opts = options(output)
    #print('>>>>>> Converting:',mfile, opts)
    #     opts.smop=True
    mparser.matlab2python(mfile,opts)

def compare_to_ref(mfile):
    output = os.path.join(os.path.dirname(mfile),'_'+os.path.basename(mfile).replace('.m','.py'))
    opts = options(output)
    #print('>>>>>> Converting:',mfile, opts)
    mparser.matlab2python(mfile,opts)
    #print('>>>>>>')

class TestMatlab2Python(unittest.TestCase):


    def test_spectrum(self):
        convert('tests/files/run_all.m')
        compare_to_ref('tests/files/fSpectrum.m')


# --------------------------------------------------------------------------------}
# --- Try to run the converted files  
# --------------------------------------------------------------------------------{

class TestZAllConverted(unittest.TestCase):
    def test_Zspectrum(self):
        import tests.files
        from tests.files._fSpectrum import fSpectrum 
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

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
    #print('>>>>>> Converting:',mfile, pyFilename)
    mparser.matlab2python(mfile, output=pyFilename)
    # Sleep to allow for IO time
    import time
    time.sleep(0.3)

    return pyFilename

class TestMatlab2Python(unittest.TestCase):

    def test_runfile(self):
        test_file = 'tests/files/run_all.m'
        with FileTestContextManager(temp_files=[tf.replace(".m", ".py") for tf in [test_file,]]):
            convert(test_file)

    def test_spectrum(self):
        test_file = 'tests/files/fSpectrum.m'
        with FileTestContextManager(temp_files=[tf.replace(".m", ".py") for tf in [test_file,]]):
            # Convert to python
            convert(test_file)

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

    def test_class(self):

        with FileTestContextManager(temp_files=["TestClass.py", "ChildClass.py"],
                                    test_file_dir="./tests/files/"):
        
            # Convert base class to python
            pyFilename_parent = convert('TestClass.m', prefix="")


            # Open the file generated and test the class
            from TestClass import TestClass

            obj = TestClass()
            self.assertEqual(obj.prop_priv, -1)

            obj.read(value=12)
            self.assertEqual(obj.prop_pub, 12)
            self.assertEqual(obj.prop_priv, 3)
        
            # Convert to child class to python
            pyFilename_child = convert('ChildClass.m', prefix="")

            # Test it
            from tests.files.ChildClass import ChildClass

            child_obj = ChildClass()
            
            self.assertEqual(child_obj.parse("Class"), "ChildClass")

            child_obj.read("Class")
            self.assertEqual(child_obj.prop_pub, "ChildClass")


class FileTestContextManager:
    def __init__(self, temp_files=[], test_file_dir=None):
        self.__project_dir = os.getcwd()
        self.__test_file_dir=test_file_dir
        self.__temp_files=temp_files
        
    def __enter__(self):
        if self.__test_file_dir is not None:
            os.chdir(self.__test_file_dir)
            
            sys.path.append(
                os.path.join(self.__project_dir,
                             self.__test_file_dir)
            )
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        for tfile in self.__temp_files:
            remove(tfile)

        os.chdir(self.__project_dir)


if __name__ == '__main__':
    unittest.main()

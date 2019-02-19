# SMOP compiler runtime support library
# Copyright 2014 Victor Leikehman

# MIT license

import __builtin__
# inf
from numpy.fft import fft2
from numpy.linalg import inv
from numpy.linalg import qr  as _qr 
try:
    from scipy.linalg import schur as _schur
except ImportError:
    pass

import os,sys,copy,time
from sys import stdin,stdout,stderr


class end(object):
    def __add__(self,n):
        self.n = n
        return self
    def __sub__(self,n):
        self.n = -n
        return self
class char(matlabarray):
    """
    class char is a rectangular string matrix, which
    inherits from matlabarray all its features except
    dtype.
    """

    def __new__(cls, a=""):
        if not isinstance(a,str):
            a = "".join([chr(c) for c in a])
        obj = np.array(list(a),
                       dtype='|S1',
                       copy=False,
                       order="F",
                       ndmin=2).view(cls).copy(order="F")
        if obj.size == 0:
            obj.shape = (0,0)
        return obj

    def __getitem__(self,index): 
        return self.get(index)

    def __str__(self):
        if self.ndim == 0:
            return ""
        if self.ndim == 1:
            return "".join(s for s in self)
        if self.ndim == 2:
            return "\n".join("".join(s) for s in self)
        raise NotImplementedError

class struct(object):
    def __init__(self,*args):
        for i in range(0,len(args),2):
            setattr(self,str(args[i]),args[i+1])

NA = numpy.NaN


def arange(start,stop,step=1,**kwargs):
    """
    >>> a=arange(1,10) # 1:10
    >>> size(a)
    matlabarray([[ 1, 10]])
    """
    expand_value = 1 if step > 0 else -1
    return matlabarray(np.arange(start,
                                 stop+expand_value,
                                 step,
                                 **kwargs).reshape(1,-1),**kwargs)
def concat(args):
    """
    >>> concat([1,2,3,4,5] , [1,2,3,4,5]])
    [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
    """
    import pdb
    pdb.set_trace()
    t = [matlabarray(a) for a in args]
    return np.concatenate(t)

def cell(*args):
    if len(args) == 1:
        args += args
    return cellarray(np.zeros(args,dtype=object,order="F"))

def copy(a):
    return matlabarray(np.asanyarray(a).copy(order="F"))

def deal(a,**kwargs):
    #import pdb; pdb.set_trace()
    return tuple([ai for ai in a.flat])


def eig(a):
    u,v = np.linalg.eig(a)
    return u.T


def exist(a,b):
    if str(b) == 'builtin':
        return str(a) in globals()
    if str(b) == 'file':
        return os.path.exists(str(a))
    raise NotImplementedError

def false(*args):
    if not args:
        return False # or matlabarray(False) ???
    if len(args) == 1: 
        args += args
    return np.zeros(args,dtype=bool,order="F")

def find(a,n=None,d=None,nargout=1):
    if d:
        raise NotImplementedError

    # there is no promise that nonzero or flatnonzero
    # use or will use indexing of the argument without
    # converting it to array first.  So we use asarray
    # instead of asanyarray
    if nargout == 1:
        i = np.flatnonzero(np.asarray(a)).reshape(1,-1)+1
        if n is not None:
            i = i.take(n)
        return matlabarray(i)
    if nargout == 2:
        i,j = np.nonzero(np.asarray(a))
        if n is not None:
            i = i.take(n)
            j = j.take(n)
        return (matlabarray((i+1).reshape(-1,1)),
                matlabarray((j+1).reshape(-1,1)))
    raise NotImplementedError

def fflush(fp):
    fp.flush()

def fprintf(fp,fmt,*args):
    if not isinstance(fp,file):
        fp = stdout
    fp.write(str(fmt) % args)

def fullfile(*args):
    return os.path.join(*args)

def iscellstr(a):
    # TODO return isinstance(a,cellarray) and all(ischar(t) for t in a.flat)
    return isinstance(a,cellarray) and all(isinstance(t,str) for t in a.flat)

def ischar(a):
    try:
        return a.dtype == "|S1"
    except AttributeError:
        return False

def isequal(a,b):
    return np.array_equal(np.asanyarray(a), np.asanyarray(b))
                          
def isfield(a,b):
    return str(b) in a.__dict__.keys()

def isnumeric(a):
    return np.asarray(a).dtype in (int,float)

def assert_(a,b=None,c=None):
    if c:
        if c >= 0:
            assert (abs(a-b) < c).all()
        else:
            assert (abs(a-b) < abs(b*c)).all()
    elif b is None:
        assert a
    else:
        #assert isequal(a,b),(a,b)
        #assert not any(a-b == 0)
        assert (a==b).all()

def size_equal(a,b):
    if a.size != b.size:
        return False
    for i in range(len(a.shape)):
        if a.shape[i] != b.shape[i]:
            return False
    return True


def strread(s, format="", nargout=1):
    if format == "":
        a = [float(x) for x in s.split()]
        return tuple(a) if nargout > 1 else np.asanyarray([a])
    raise NotImplementedError


def toupper(a):
    return char(str(a.data).upper())

true = True

def tic():
    return time.clock()

def toc(t):
    return time.clock()-t

def true(*args):
    if len(args) == 1:
        args += args
    return matlabarray(np.ones(args,dtype=bool,order="F"))

def zeros(*args,**kwargs):
    if not args:
        return 0.0
    if len(args) == 1:
        args += args
    return matlabarray(np.zeros(args,**kwargs))

eps = np.finfo(float).eps
#print(np.finfo(np.float32).eps)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

# vim:et:sw=4:si:tw=60

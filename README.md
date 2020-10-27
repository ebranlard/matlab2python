[![Build Status](https://travis-ci.com/ebranlard/matlab2python.svg?branch=master)](https://travis-ci.com/ebranlard/matlab2python)
<a href="https://www.buymeacoffee.com/hTpOQGl" rel="nofollow"><img alt="Donate just a small amount, buy me a coffee!" src="https://warehouse-camo.cmh1.psfhosted.org/1c939ba1227996b87bb03cf029c14821eab9ad91/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4275792532306d6525323061253230636f666665652d79656c6c6f77677265656e2e737667"></a>

# matlab2python

A python script to convert matlab files or lines of matlab code to python. This project is in alpha phase. 
This implementation relies heavily on the project [SMOP](http://github.com/victorlei/smop/) by Victor Leikehman. 
The current implementation wraps around SMOP, with the following differences: 

- It attempts to produce code that does not rely on `libsmop`, but only on usual python modules such as `numpy`.
- It uses typical shortcuts such as `np` instead of `numpy`.
- It attemps to reindex arrays and loops, starting from 0 instead of 1.
- It doesn't use the external classes `matlabarray` and `cellarray` from `libsmop`
- Basic support for Matlab classes is added. The properties declared in the body of the class are initialized in the constructor.
- As a consequenc of all the above, the resulting code is "less safe" but maybe slightly closer to what a user would write.

This implementation is made straightforward, since it basically use another backend script than the one used by SMOP, here called `smop\backend_m2py.py`. 
Some function replacements were added directly there. 
Additional support for classes, import modules and other fine-tuning replacements (or hacks...) are done in the file `matlabparser\parser.py`.


## Install
The code is written in python, you can access it as follows:
```bash
git clone https://github.com/ebranlard/matlab2python
cd matlab2python
python -m pip install --user -r requirements.txt
```

## Usage
The main script at the root of the repository is executable and has a couple of command line flags (some of them taken directly from SMOP). 
To convert the file `file.m` to `file.py`, simply type:
```bash
python matlab2python.py file.m -o file.py
```
The python package can also be used directly to perform conversion of files or lines of code.


## Should I use this

If you need a script that performs the obvious conversions from matlab to python, `matlab2python` will hopefully work for you.
These conversions are for instance: 

- syntax (`def`, `if`, `for`, `__init__`, no more `end`)
- indentation
- parenthesis to brackets
- simple builtin functions replacements (`fprintf`, `disp`, `error`, `fopen`)
- simple numpy replacements like `zeros(3,4)` to `np.zeros((3,4))`, or `cosd(x)`, to `np.cosd(np.pi/180 x)`
- other misc functions like `strcmp`, `strrep`, `reshape` replaced by their python , 
- etc

As mentioned above, [SMOP](http://github.com/victorlei/smop/) does a great job to produce safe code.
Yet, neither `SMOP` nor `matlab2python` will generate code that is production-ready (it might in some cases). 
Most of the time, the user will have to go through the code and perform adjustements and some rewritting. 
In fact, `matlab2python` will likely be slightly worse than SMOP in producing a code that works out of the box.
But at the end, the code produced by `matlab2python` should require less refactoring and help the user in its conversion.
As mentioned by the author of SMOP, it is difficult not to hide the matlab flavor from the code that is generated and it's also difficult to fully convert the code without introducing wrapped classes such that `matlabarray`. The implemenation of `matlab2python` attempts to do that, at the price of less safety.

I've written this wrapper script for my own needs. I was ready to convert manually a bunch of matlab scripts, but I thought I could have a script to automate some of the simple conversions and formatting. I started a quick and dirty implementation before discovering `SMOP`. At the end, I merged my quick and dirty implemenation with the more powerful parsing framework used by SMOP. Hopefully this can be useful to someone else! If so, feel free to contribute. 



# Contributing
Any contributions to this project are welcome! If you find this project useful, you can also buy me a coffee (donate a small amount) with the link below:


<a href="https://www.buymeacoffee.com/hTpOQGl" rel="nofollow"><img alt="Donate just a small amount, buy me a coffee!" src="https://warehouse-camo.cmh1.psfhosted.org/1c939ba1227996b87bb03cf029c14821eab9ad91/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4275792532306d6525323061253230636f666665652d79656c6c6f77677265656e2e737667"></a>


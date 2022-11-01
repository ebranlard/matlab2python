"""
Difficulties
 A = [ 1 2 3  % comment
      4 5 5]
 A = { 1 2 3  % comment
      4 5 5}

 A = 

"""
import os
import smop
from smop.main import parse_matlab_lines

from . import parsing_tools as PT

def strfind(s,c):
    return [pos for pos, char in enumerate(s) if char == c]

CHARSET_BEFORE_TRANSPOSE=r'[a-zA-Z0-9_\}\]\)\.\']'
CHARSET_BEFORE_TRANSPOSE_NONVAR=   r'[\}\]\)\.]'
CHARSET_VAR=r'[a-zA-Z0-9_]'


def find_strings(line):
    
    strings=[]
    i=0
    bUnfinished=False
    while i<len(line):
        c=line[i]
        if c=='\'':
            # Finding if it's a string start
            c_prev=line[i-1:i]
            if len(c_prev)==0:
                # for sure, it's a string start
                bStringStart=True
            elif PT.string_contains_charset(c_prev,CHARSET_BEFORE_TRANSPOSE):
                # for sure, it's a transpose
                bStringStart=False
            elif c_prev==' ':
                # that's tricky, let's see what's really before
                c_prev=PT.previous_nonspace_char(line,i)
                if len(c_prev)==0:
                    # for sure, it's a string start
                    bStringStart=True
                elif PT.string_contains_charset(c_prev,CHARSET_BEFORE_TRANSPOSE_NONVAR):
                    # for sure, it's a transpose
                    bStringStart=False
                elif PT.string_contains_charset(c_prev,CHARSET_VAR):
                    # That's the worse case, if you allow a space before a transpose: 
                    #   for instance [a ' ; b '] : is this a string concatenation? 
                    #       or concatenation of two transposed variables?
                    #print('>>> Potential problematic line, assuming string start:'+line)
                    bStringStart=True
                else:
                    # We could check for some syntax error here, but we can safely assume it's a string start
                    bStringStart=True
            else:
                bStringStart=True
            #
            if bStringStart:
                s = PT.extract_quotedstring(line[i:])
                if len(s)==len(line[i:])-1:
                    bUnfinished=True
                strings.append((i,s))
                i=i+1+len(s)
        i=i+1;



    return strings,bUnfinished

def replace_at_pos(s,pos,new):
    sout=s[0:pos]
    sout+=new
    sout+=s[pos+len(new):]
    return sout


def separate_comment(line):
    line_backup=line
    SI,bLastOK=find_strings(line)
    # Replacing strings with dummy 'X'
    for si in SI:
        line=replace_at_pos(line,si[0],'X'*(len(si[1])+2))
    pos=PT.find_pos(line,'%')
    if len(pos)==0:
        statement =line_backup
        comment =''
    else:
        comment   = line_backup[(pos[0]):]
        statement = line_backup[:(pos[0])]

    return statement, comment

def parse_function_def(stmt):
    stmt=stmt[8:].strip()
    name=''
    args_out=[]
    args_in=[]
    # Output arguments
    ieq=stmt.find('=')
    if ieq>0:
        sArgs_out=stmt[:ieq]
        sArgs_out=sArgs_out.replace('[','').replace(']','').replace(',',' ')
        args_out=[a.strip() for a in sArgs_out.split() if len(a)>0]
    # Declaration
    ieq = max(ieq+1,0)
    sDecl=stmt[ieq:].strip()
    # Function name
    io =sDecl.find('(')
    isc =sDecl.find(';')
    if io>0:
        name=sDecl[:io].strip()
    elif isc>0:
        name=sDecl[:isc].strip()
    else:
        name=sDecl.strip()
    # Arguments
    ic =sDecl.find(')')
    if io>0:
        args_in=[a.strip() for a in sDecl[io+1:ic].split(',') if len(a.strip())>0]
    return name, args_out, args_in

def parse_class_def(stmt):
    stmt=stmt[9:].strip().replace(';','');
    if len(stmt)==0:
        raise Exception('Wrong classdef definition')
    name=''
    children=[]
    im=stmt.find('<')
    if im>0:
        name=stmt[:im].strip()
        children=[a.strip() for a in stmt[im+1:].split(',') if len(a.strip())>0]
    else:
        name=stmt
    return name, children

def merge_lines(LC):
    LC_new=[]
    i=0
    while i<len(LC):
        lc=LC[i]
        stmt=lc[0].strip()
        if len(stmt)>0 and stmt[-1]=='\\':
            lc_next=LC[i+1]
            LC[i+1]=(stmt[:-1]+lc_next[0], lc[1]+lc_next[1])
        else:
            LC_new.append(lc)
        i+=1
    return LC_new




class line():
    def __init__(self):
        self.statement=[]
        self.comment=[]

    def __init__(self,l):
        self.statement,self.comment = separate_comment(l)
# __all__  = ['parse']


# --------------------------------------------------------------------------------}
# --- Matlab File 
# --------------------------------------------------------------------------------{
class MatlabFile:
    def __init__(self,filename=None,lines=None):

        self.FileType=None #
        self.Properties=[] #
        self.Methods=[] #
        self.Header=[] #
        self.Corpus=[] #
        self.Name='' #
        self.ClassChildren='' #
        self.ArgsIn='' #
        self.ArgsOut='' #

        if filename is not None:
            with open(filename, 'r', errors='ignore') as f:
                self.raw_lines=f.readlines()
        elif lines is not None:
            if isinstance(lines,list):
                self.raw_lines=lines
            else:
                self.raw_lines=lines.split('\n')
        else:
            raise Exception('Provide filename or lines')
        self.read()

    def read(self):
        # --- Separate lines and comments
        lines_comment=[]
        for l in self.raw_lines:
            lc=separate_comment(l.strip())
            lines_comment.append(lc)
        # --- Merging lines with explicit line continuation \
        lines_comment = merge_lines(lines_comment)
        #for lc in lines_comment:
        #    print('>',lc[0])

        # --- detecting main file type and splitting into corpus and header
        self.Header=[]
        for lc in lines_comment:
            if self.FileType is None: 
                stmt=lc[0].strip().lower()
                if len(stmt)==0:
                    self.Header.append(lc)
                else:
                    if stmt.find('classdef')==0:
                        self.FileType='class'
                        self.Name = parse_class_def(lc[0])[0]
                        self.Corpus.append(lc)
                    elif stmt.find('function')==0:
                        self.FileType='function'
                        self.Name = parse_function_def(lc[0])[0]
                        self.Corpus.append(lc)
                    else:
                        self.FileType='script'
                        self.Corpus.append(lc)
            else:
                self.Corpus.append(lc)
        # --- For classes we detect properties and methods
        def remove_last_end(lc):
            if len(lc)>0:
                bEndFound=False
                i=len(lc)-1
                while not bEndFound and i>=0:
                    words = lc[i][0].strip().lower().split(';')
                    if 'end' in words:
                        bEndFound=True
                        lc[i]=(';'.join([w for w in words if w!='end']),lc[i][1])
                    i-=1
            return lc
        if self.FileType=='class':
            bIsInProp=False
            bIsInMeth=False
            lProp=[]
            lMeth=[]
            OldCorpus = remove_last_end(self.Corpus) # removing end class
            self.Corpus=[]
            for lc in OldCorpus:
                stmt=lc[0].strip().lower()
                if stmt.find('properties')==0:
                    bIsInProp=True
                    bIsInMeth=False
                    lProp=remove_last_end(lProp)
                elif stmt.find('methods')==0:
                    bIsInProp=False
                    bIsInMeth=True
                    lMeth=remove_last_end(lMeth)
                elif bIsInProp:
                    lProp.append(lc)
                elif bIsInMeth:
                    lMeth.append(lc)
                else:
                    self.Corpus.append(lc)
                    #self.Header.append(lc)
            lMeth = remove_last_end(lMeth)
            lProp = remove_last_end(lProp)
            self.Methods=[lc for lc in lMeth if ((len(lc[0].strip())>0) or ( len(lc[1].strip())>0))]
            self.Properties=[lc for lc in lProp if ((len(lc[0].strip())>0) or ( len(lc[1].strip())>0))]

    def toString(self):
        s=''
        s+='\n'.join([lc[0]+lc[1] for lc in self.Header])
        if len(self.Header)>0:
            s+='\n'
        s+='\n'.join([lc[0]+lc[1] for lc in self.Corpus])
        if self.FileType=='class':
            if len(self.Properties)>0:
                s+='\nproperties\n'
                s+='\n'.join(['    '+lc[0]+lc[1] for lc in self.Properties])
                s+='\nend\n'
            if len(self.Methods)>0:
                s+='\nmethods\n'
                s+='\n'.join(['    '+lc[0]+lc[1] for lc in self.Methods])
                s+='\nend\n'
            s+='end\n'
        return s

            
    def toPython(self,backend='m2py'):
        def postpro(s):
            IMPORTS=[]
            def add_import(ll,sfind,sadd):
                if ll.find(sfind)>=0:
                    if sadd not in IMPORTS:
                        IMPORTS.append(sadd)
            def get_indent(s):
                sind=''
                for c in s:
                    if c==' ':
                        sind+=' '
                    else:
                        break
                return sind
            def parse_fclose(l):
                ps=l.find('fclose')
                if ps>0:
                    pe=l.find(')')
                    sind=get_indent(l)
                    fid=l[ps+7:pe]
                    l=sind+fid+'.close()'+l[pe+1:]
                return l
#             def parse_LHS(l):
#                 ps=l.find('=')


            lines=[]
            if backend=='m2py':
                for l in s.split('\n'):
                    ll=l.lower().strip()
                    if ll=='clc':
                        continue
                    add_import(ll,'np.','import numpy as np')
                    add_import(ll,'np.matlib','import numpy.matlib')
                    add_import(ll,'os.','import os')
                    add_import(ll,'warnings.','import warnings')
                    add_import(ll,'plt.','import matplotlib.pyplot as plt')
                    add_import(ll,'scipy.special.','import scipy.special')
                    add_import(ll,'__builtin__.','import __builtin__')
                    l=parse_fclose(l)
                    lines.append(l)
                return '\n'.join(IMPORTS+lines)
            else:
                return s

        s=''
        s+='\n'.join([lc[0]+lc[1].replace('%','#') for lc in self.Header])
        if len(self.Header)>0:
            s+='\n'
        if self.FileType=='script':
            stmp='\n'.join([lc[0]+lc[1] for lc in self.Corpus])
            stmp=parse_matlab_lines(stmp,backend)
            if len(stmp)>5 and stmp[0:5]=='\n    ':
                stmp=stmp.replace('\n    ','\n')
            if stmp[0]=='\n':
                stmp=stmp[1:] # somehow first character is new line
            s+=postpro(stmp)

        elif self.FileType=='function':
            fName,args_out,args_in = parse_function_def(self.Corpus[0][0])
            stmp='\n'.join([lc[0]+lc[1] for lc in self.Corpus])
            #print(stmp)
            stmp=parse_matlab_lines(stmp,backend)
            if stmp[0]=='\n':
                stmp=stmp[1:] # somehow first character is new line
            if len(args_out)>0:
                stmp+='\n    return '+','.join(args_out)
            s+=postpro(stmp)

        elif self.FileType=='class':
            fName,children= parse_class_def(self.Corpus[0][0])
            children = [c for c in children if c!='handle']
            if len(children)>=0:
                for c in children:
                    s+='from '+c +' import '+c+'\n'
                s+='\n'+'class '+fName.strip()+'('+','.join(children)+'):\n'
            else:
                s+='\n'+'class '+fName.strip()+'():\n'

            s+=''.join(['    '+lc[0]+lc[1].replace('%','#')+'\n' for lc in self.Corpus[1:]])
            if len(self.Methods)>0:
                #s+='\nmethods\n'
                #s+='\n'.join(['    '+lc[0]+lc[1] for lc in self.Methods])
                #s+='\nend\n'
                lMeth=[]
                # we look for the constructor
                bConstructorFound=False
                for lc in self.Methods:
                    if lc[0].find(fName)>=0 and lc[0].lower().find('function')==0:
                        bConstructorFound=True
                        fName,args_out,args_in = parse_function_def(lc[0])
                        #print('>>>>>>',lc[0])
                        if len(args_out)!=1:
                            raise Exception('Class constructor should return only one value')
                        #print('>>>>>>',fName,args_out,args_in)
                        lc=('function __init__('+','.join(args_out+args_in)+')',lc[1])
                        #print('>>>>>>',lc[0])
                        lMeth.append(lc)
                        # Adding properties initialization
                        for lcp in self.Properties:
                            if lcp[0].find('=')>=0:
                                lMeth.append((args_out[0]+'.'+lcp[0].strip(),lcp[1]))
                                
                    else:
                        if lc[0].find('@') >= 0:
                            if lc[0].find("this@") >= 0:
                                # Call to a super constructor
                                super_call = lc[0].split("@")[-1].strip(".")
                                super_split = super_call.split("(")
                                pylc = super_split[0]+".__init__(self,"+super_split[1]
                            else:
                                pylc = lc[0]
                                
                            if pylc.find("@this") >= 0:
                                # This is just a property, just remove the @
                                pylc = pylc.replace("@this", "self")
                                
                            if pylc.find(" @") >= 0 or pylc.find(",@") >= 0:
                                # This is also a static property
                                for (f, r) in [(" @", " "), (",@", ", ")]:
                                    if pylc.find(f) >= 0 :
                                        pylc = pylc.replace(f, r)
                                        
                            if pylc.split("@")[0] == "":
                                # Last case of static property
                                pylc = pylc[1:]
                                
                            if pylc.find("@") >= 0:
                                if len(pylc.split("@")) == 2:
                                    # Should be a static method
                                    method_name, rest = pylc.split("@")
                                    # Might have a return value though
                                    if method_name.find("=") >= 0:
                                        lhs, method_name = method_name.split("=")
                                        lhs = lhs.strip(" ")
                                        method_name = method_name.strip(" ")
                                    else:
                                        lhs = None
                                    def split_first(string, token):
                                        split = string.split(token)
                                        if len(split) > 2:
                                            split = [split[0], string[len(split[0])+1:-1]]
                                        return split
                                    class_name, params = split_first(rest, "(")
                                    pylc = class_name + "." + method_name + "(" + params
                                    if lhs is not None:
                                        pylc = lhs + " = " + pylc
                                
                                else:
                                    raise Exception("Can't parse '@' statement: " + lc[0])
                                
                            lMeth.append(("", pylc))
                                
                        else:
                            lMeth.append(lc)
                if not bConstructorFound:
                    raise Exception('Constructor not found in class')

                stmp='\n'.join([lc[0]+lc[1] for lc in lMeth])
                stmp=stmp.replace("this", "self") # TODO: Shouldn't really happen in comments. 
                #print(stmp)
                stmp=parse_matlab_lines(stmp,backend)
                stmp=stmp.replace('\n','\n    ')
                s+=stmp
                s=postpro(s)
        return s




def parse(filename):
    # Looping through files if a list provided
    if isinstance(filename,list):
        for f in filename:
            parse(f)
        return
    # Parsing
    #print('Parsing: {}'.format(filename))
    if not os.path.exists(filename):
        raise Exception('FileNotFound:'+filename)
    MF=MatlabFile(filename=filename)
    #print(lines)

def setSMOPOptions(linenumbers=False, no_comments=False, no_resolve=False, filename='', **kwargs):
    """ Set options of SMOP module
    NOTE: these are global...
    """
    #options.debug=opts.debug
    smop.options.filename    = filename
    smop.options.no_numbers  = not linenumbers # show a comment with original line number
    smop.options.no_comments = no_comments
    smop.options.no_resolve  = no_resolve

def matlab2python(filename, output=None, backend='m2py', **kwargs):
    """ 
    Convert a matlab file (defined by `filename`) to python. 
    The result is returned to stdout, or a file if `output` is provided.

    INPUTS:
     - filename: matlab filename, string
     - output: python filename to be written. If `output`='stdout' the outputs are printed to screen.
     - backend: 'm2py' or 'smop': which backend to use for the conversion. 
                'm2py' relies on smop, but performs additional conversions
     - kwargs: Dictionary of SMOP options
         - no_comments: if true, strip out comment lines from the output
         - linenumbers: if true, show a comment with original line number
         - no_resolve:  omit name resolution 
    """
    # Passing options to smop module
    setSMOPOptions(filename=output, **kwargs)
    # Looping through files if a list provided
    if isinstance(filename,list):
        for f in filename:
            matlab2python(f, output=output, backend=backend, **kwargs)
        return
    if not os.path.exists(filename):
        raise Exception('FileNotFound:'+filename)
    # Create an instance of MatlabFile and convert to python
    MF = MatlabFile(filename = filename)
    PY = MF.toPython(backend = backend)
    # Return result to user, stdout, or file
    if output is None:
        pass
    elif output == 'stdout':
        print(PY)
    else:
        with open(output, 'w') as f:
            f.write(PY)
    return PY

def matlablines2python(lines, output=None, backend='m2py', **kwargs):
    # Passing options to smop module
    setSMOPOptions(**kwargs)
    # Create an instance of MatlabFile and convert to python
    MF = MatlabFile(lines = lines)
    PY = MF.toPython(backend=backend)
    # Return result to user or stdout
    if output == 'stdout':
        print(PY)
    return PY

    




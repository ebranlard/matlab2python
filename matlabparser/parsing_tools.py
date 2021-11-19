import re


# --------------------------------------------------------------------------------}
# --- String functions 
# --------------------------------------------------------------------------------{
def string_contains_charset(s,charset):
    return bool(re.search(charset, s))

def previous_nonspace_pos(s,i):
    j=i-1
    while j>=0 and s[j:j+1]==' ':
        j=j-1
    return j
def previous_nonspace_char(s,i):
    j=previous_nonspace_pos(s,i)
    if j>=0:
        return s[j:j+1]
    else:
        return ''
def find_pos(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]



# Extracted from fissurroundedby developed for matlab2fortran
# looks if character s(p) is surrounded by the characters c1 and c2 
# returns a boolean , and the postion of these charactesrs
# [b p1 p2]=fissurroundedby('function [a b c]=issur([,])',10,'[',']')
# [b p1 p2]=fissurroundedby('function [a b c]=issur([,])',11,'[',']')
# [b p1 p2]=fissurroundedby('function [a b c]=issur([,])',10,'[',']')
# [b p1 p2]=fissurroundedby('function [''a b c'']=issur([,])',10,'''','''')
# [b p1 p2]=fissurroundedby('function [''a b c'']=issur([,])',12,'''','''')
# [b p1 p2]=fissurroundedby('(),()',4,'(',')')
def is_surrounded_by(s,p,c1,c2):
    p1=0;
    p2=0;
    ## stupid whiles
    # look backward
    notfound=True;
    i=p-1;
    while i>=0 and notfound:
        if c1!=c2 :
            # then if c2 is encountered we should break
            if s[i]==c2:
                break
        if s[i]==c1:
            notfound=False;
            p1=i;
        i=i-1;

    # look forward
    notfound=True;
    i=p+1;
    while i<len(s) and notfound:
        if c1!=c2 :
            # then if c1 is encountered we should break
            if s[i]==c1:
                break
        if s[i]==c2:
            notfound=False;
            p2=i;
        i=i+1;


    if p1==0 or p2==0:
        b=False; # not surrounded
    else:
        b=True;
    return(b,p1,p2)

def is_in_quotes(s,p):
    # Checks whether the position p in string s is wihtin some quotes
    # Returns false if you are on a starting or closing quote
    # Quick and really dirty
    bInSingle=False
    bInDouble=False
    # We look before
    for i in range(p):
        #print(s[i])
        if s[i]=='\'':
            if bInSingle:
                bInSingle=False # That's a closing
            elif bInDouble:
                # We are in double, ignore
                pass
            else:
                # That's an opening
                bInSingle=True
        if s[i]=='"':
            if bInDouble:
                # That's a closing
                bInDouble=False
            elif bInSingle:
                # We are in single, ignore double quotes
                pass
            else:
                # That's an opening
                bInDouble=True
    return(bInSingle or bInDouble)

def replace_inquotes(s,c):
    # replace the string s 
    s=s.replace("""''""",c+c) # first replace double quotes

    # Quick and really dirty
    bInSingle=False
    bInDouble=False
    sout=''
    for i,C in enumerate(s):
        if C=='\'':
            sout+=c
            if bInSingle:
                bInSingle=False # That's a closing
            elif bInDouble:
                # We are in double, ignore
                pass
            else:
                # That's an opening
                bInSingle=True
        elif C=='"':
            sout+=c
            if bInDouble:
                # That's a closing
                bInDouble=False
            elif bInSingle:
                # We are in single, ignore double quotes
                pass
            else:
                # That's an opening
                bInDouble=True
        elif bInDouble or bInSingle:
            sout+=c
        else:
            sout+=C
    return sout


def extract_quotedstring(s):
    s_backup=s
    if s=="""''""":
        return ''
    elif s=='""':
        return ''
    s=s.replace("""''""",'XX') # first replace double quotes
    if s.find('XX')==0:
        return ''

    bInSingle = s[0]=='\''
    bInDouble = s[0]=='"'
    i=1
    bEndQuote=False
    while i<len(s):
        c=s[i]
        if c=='\'':
            if bInSingle:
                bEndQuote=True
                bInSingle=False # That's a closing
                break
            elif bInDouble:
                pass # We are in double, ignore
            else:
                raise Exception('Opening single quote found, should not happen!')
        elif c=='"':
            if bInDouble:
                # That's a closing
                bEndQuote=True
                bInDouble=False
                break
            elif bInSingle:
                pass # We are in single, ignore double quotes
            else:
                raise Exception('Opening double quote found, should not happen!')
        i=i+1
    if not bEndQuote:
        #print('NO END OF QUOTE FOUND!')
        return s_backup[1:]
    else:
        return s_backup[1:i]



if __name__ == "__main__":
    print(is_in_quotes("""0'""2'""",4))
#     (b,p1,p2)=is_surrounded_by(r'function [\'a b c\']=issur([,])',11,r'\'',r'\'')
#     print(b,p1,p2)
#     (b,p1,p2)=is_surrounded_by('dsfk[ & ] sdlkfj',6,'[',']')
#     print(b,p1,p2)
#     (b,p1,p2)=is_surrounded_by('function [a b c]=issur([,])',10,'[',']')
#     print(b,p1,p2)
#     (b,p1,p2)=is_surrounded_by('function [a b c]=issur([,])',11,'[',']')
#     print(b,p1,p2)
#     (b,p1,p2)=is_surrounded_by('function [a b c]=issur([,])',10,'[',']')
#     print(b,p1,p2)
#     (b,p1,p2)=is_surrounded_by('function [''a b c'']=issur([,])',12,r'\'',r'\'')
#     print(b,p1,p2)
#     (b,p1,p2)=is_surrounded_by('(),()',4,'(',')')
#     print(b,p1,p2)





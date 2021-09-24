import os

# this function catalogs the declared functions in a directory that's path is determined by the
# the file names that passed in, if the name includes a path it will go there and look for function
# declarations
# this function returns a 2-d list where the fist index in each row is the name of the source file
# and the rest of that row are the functions within that soruce file
def catalog_functions(argv):
    # first element of every row is the file name
    # declaring the 
    catalog = []

    # this splits each directory in the path inputted into a element in a list
    path_components = argv[0].split('/')
    
    # removing the file name from the list created above
    path_components.pop(len(path_components) - 1)

    # essentially if just a file name was passed then there was no path and the directory to for function declarations is this
    # directory
    if len(path_components) == 0:
        # setting to this directory
        file_path = '.'
    
    else:
        # essentially if a path was provided then the path is set to where functions will be looked for
        file_path = ""

        # collapsing the list into a string that is a path
        for item in path_components:
            # adding a directory name
            file_path+=item

            # adding the character that separates directories in a path
            file_path+="/"
      

    # iterating throught the list of file in the directory that contains the functions    
    for file in os.listdir(file_path):
        # filtering out matlab source files
        if file.count('.m') != 0 and file.count('.md') == 0:
            # adding the matlab file name that contains functions to a list, but changing the extension to python
            names_line = [file.replace(".m", ".py")]

            f = open(file, 'r')
            lines = f.readlines()
            f.close()

            look = False

            function_line = ""

            for line in lines:
                if line.count('%') == 0 and line.count('function') != 0:
                    look = True
                
                if look:
                    for char in line:
                        if char != '(':
                            function_line+=char
                        else:
                            #print(function_line)
                            for i in range(len(function_line) - 1, 0, -1):
                                if function_line[i] == '=':
                                    names_line.append(function_line[i + 1:len(function_line)].replace('...\n', '').strip())
                                    break
                            
                            look = False
                            function_line = ""
                            break
                        

            catalog.append(names_line)
            
    #print("Catalog: ", catalog)
    return catalog

#  function that adds the import statement to the file if it comes across a function call from the catalog
def adding_imports(file_name, catalog=None, modules=None):
    if modules is None:
        #print(catalog)
        # changing the file to python
        file_name = file_name.replace('.m', '.py')
        
        lines = []
        
        # opening python file
        f = open(file_name, 'r')

        # iterating through the lines of the file
        for line in f:
            # adding the line to the list
            lines.append(line)

            # iterating through the catalog of function declarations
            for item in catalog:
                # looking through the function declarations from each file
                for i in range(1, len(item)):
                    # if the line contains a function call this is from the file in the catalog and the current file is not the file in
                    # the catalog then add the import string to the beginning of the python file
                    if line.count(item[i]) != 0 and item[0] != file_name:
                        lines.insert(0, "from " + item[0].replace('.py', '') + " import " + item[i] + "\n")
                        item.remove(item[i])

        f.close()
        #print(lines)

        # writing lines back to the file
        f = open(file_name, 'w')
        for line in lines:
            f.write(line)
        
        f.close()
    
    else:
        f = open(file_name, 'r')
        lines = f.readlines()
        f.close()
        
        #print("LOOKING FOR THESE:", modules,  "IN:", file_name)

        for module in modules:
            j = 0
            insert = True
            while lines[j].count('import') != 0:
                if lines[j].count(module) != 0:
                    insert = False
                    break
                j+=1
            
            if insert:
                #print("INSERTING:", module, "IN:", file_name)
                lines.insert(0, "import " + module + "\n")

        f = open(file_name, 'w')
        for line in lines:
            f.write(line)

        f.close()

# looks for functions that come with matlab and changes them to a python equivalent  
def replace_keywords_in_line(argv):
    # setting the name of the python file this is looking in to a variable
    file_name = argv[len(argv) - 1]    

    # setting the matlab methods to look for
    look_for_these = ["int2str", "num2str", "int64", "factorial", "polyval", "pi", "median", "pause", "display"]

    # setting the python equivalent to matlab function that must share the same index
    replace_with_these = ["str", "str", "int", "math.factorial", "np.polyval", "np.pi", "np.median", "time.sleep(1)", "print"]

    # list for the lines in the file
    new_lines = []

    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()

    modules = []
    # iterating through the lines of the file
    for line in lines:
        # looking for the matlab methods in the file
        for i in range(len(look_for_these)):
            # replacing the matlab method with the python version
            if line.count(look_for_these[i]) != 0:
                if replace_with_these[i].count('.') != 0:
                    #print("this is what is being added to modules:", replace_with_these[i][replace_with_these[i].find('=') + 1:replace_with_these[i].find('.')].replace('(', ''))
                    modules.append(replace_with_these[i][replace_with_these[i].find('=') + 1:replace_with_these[i].find('.')].replace('(', ''))
                    
                    
                    '''
                    print("MODULE:", module)
                    for check_line in lines:
                        if check_line.count('import') != 0:
                            if check_line.count(module) != 0:
                                #print("Already has module")
                                break
                            
                            
                        else:
                            new_lines.insert(0, "import " + module + "\n")
                            break
                    '''

                line = line.replace(look_for_these[i], replace_with_these[i])

        # adding the changed line to the list that contains the lines for the file
        new_lines.append(line)


    # writing the lines back to the file
    f = open(file_name, 'w')
    for line in new_lines:
        f.write(line)
                
    f.close()

    adding_imports(file_name, modules=modules)

# this removes the second return statement generated by the rest of the code
def remove_return(argv):
    # setting the name of the python file that this looking through
    file_name = argv[len(argv) - 1]

    lines = []
    look = False
    conditional = False

    # iterating throught the lines of the file
    f = open(file_name, 'r')
    for line in f:
        # if the line contains a return statement that hasn't already been found
        if line.count("return") != 0 and look:
            # if the return statement is not in a conditional structure then this return is not added to the new lines
            # for the file
            if not conditional:
                continue
        
        elif line.count("return") != 0:
            # if this is the first return statement that this has come across then a bool is set to indicate this
            look = True
        
        lines.append(line)

        # if the code is looking for a return statement this checks if there is a conditional statement encapuslating the returns
        if look:
            if line.count('if')  != 0 or line.count('elif') != 0 or line.count('else') != 0:
                conditional = True

    f.close()

    # writing the lines back to the file
    f = open(file_name, 'w')   
    for line in lines:
        f.write(line)

    f.close()
#********************************************************
#
#  Author:       Caleb Myers
#
#  Class:        CS 3200
#
#  Project:      Project 3 -- BPL Interpreter
#
#  Date:         March 24, 2017
#
#  Description:  This file contains the functions used to
#                scan and create tokens of lines of BPL 
#                programs.
#
#********************************************************

#************************************************
#
# Function: scan
#
# Parameters: line - a line from the program
#
# Purpose:  create a list out of line then send
#           the list to the right function to
#           scan it. Returns a list of tokens
#
# Calls: string function split
#        function scanDouble
#        function scanString
#        function scanRead
#        function scanPrint
#        function scanAssingment
#
#************************************************
def scan(line):
    firstWord = line.split()[0]
    if firstWord == 'double' or firstWord == 'string':
        return scanDeclaration(line, firstWord)
    elif firstWord == 'read':
        return scanRead(line)
    elif firstWord == 'print':
        return scanPrint(line)
    else:
        return scanAssignment(line)


            

#************************************************
#
# Function: scanDeclaration
#
# Parameters: line - a declaration line from the
#                    program
#
# Purpose:  create and returns a list of tokens
#           from line
#
# Calls: string function split
#        string function replace
#        list function append
#
#************************************************
def scanDeclaration(line, firstWord):
    tokens = [('TYPE', firstWord.upper())]
    variables = line.replace(',',' , ').replace(';',' ;').split()[1:]
    for variable in variables:
        if variable == ',':
            tokens.append(('COMMA',','))
        elif variable == ';':
            tokens.append(('SEMI',';'))
        else:
            tokens.append(('VAR',variable.replace(',','')))
    return tokens

#************************************************
#
# Function: scanRead
#
# Parameters: line - a read line from the program
#
# Purpose:  create and returns a list of tokens
#           from line
#
# Calls: string function split
#        string function replace
#        list function append
#
#************************************************
def scanRead(line):
    tokens = [('FUNCTION', 'read')]
    variables = line.replace(',',' , ').replace(';',' ;').split()[1:]
    for variable in variables:
        if variable == ',':
            tokens.append(('COMMA',','))
        elif variable == ';':
            tokens.append(('SEMI',';'))
        else:
            tokens.append(('VAR',variable.replace(',','')))
    return tokens


#************************************************
#
# Function: scanPrint
#
# Parameters: line - a read line from the program
#
# Purpose:  create and returns a list of tokens
#           from line
#
# Calls: string function replace
#        list function append
#        string function find
#        function len
#        function overlap
#        function isFloat
#
#************************************************
def scanPrint(line):
    tokens = [('FUNCTION', 'print')]
    line = line.replace('print ','')
    operators = ['(', ')', '+', '-', '*', '/']
    i = 0;
    while i < len(line):
        temp = ''
        if line[i].find('"') != -1:
            i += 1
            temp = line[i:]
            temp = temp[:temp.find('"')]
            tokens.append(('STRING',temp))
            i += len(temp)
        elif line[i] == ',':
            tokens.append(('COMMA',','))
        elif line[i] == ';':
            tokens.append(('SEMI',';'))
        elif line[i] != ' ':
            temp = line[i:]
            if temp.find(',') != 0: temp = temp[:temp.find(',')].strip()
            else: temp = temp[:-1].strip()
            i += len(temp) - 1
            if not overlap(operators, temp): 
                if isFloat(temp): tokens.append(('DOUBLE', temp))
                else: tokens.append(('VAR',temp))
            else: tokens.append(('EXP',temp))
        i += 1
    return tokens



#************************************************
#
# Function: scanAssignment
#
# Parameters: line - a read line from the program
#
# Purpose:  create and returns a list of tokens
#           from line
#
# Calls: string function split
#        list function appendd
#        function overlap
#        function isFloat
#
#************************************************
def scanAssignment(line):
    operators = ['(', ')', '+', '-', '*', '/']
    line = line[:-1].split('=')
    if len(line) < 2:
        print('***Error: Invalid declaration syntax ***')
        exit()
    tokens = [('VAR',line[0].strip()),('EQUALS','=')]
    if overlap(operators, line[1]): tokens.append(('EXP',line[1].strip()))
    elif isFloat(line[1]): tokens.append(('DOUBLE',float(line[1].strip())))
    elif '"' in line[1]: tokens.append(('STRING', line[1].replace('"','').strip()))
    else: tokens.append(('VAR',line[1].strip()))
    tokens.append(('SEMI',';'))
    return tokens
           

#************************************************
#
# Function: overlap
#
# Parameters: stringList - list of strings
#             string     - a string
#
# Purpose:  return true if item in string list is
#           in string. Returns false if not
#
# Calls: none
#
#************************************************            
def overlap(stringList, string):
    for item in stringList:
        if item in string:
            return True
    return False

#************************************************
#
# Function: isFloat
#
# Parameters: var - a string variable
#
# Purpose:  return true if var is a string of a
#           double, returns false if not
#
# Calls: function float
#
#************************************************  
def isFloat(var):
    try:
        float(var)
        return True
    except ValueError:
        return False

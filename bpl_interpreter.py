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
#  Description:  This program is an interpreter for the 
#                Bobcat Programming language. It reads in 
#                each line of the file, tokenizes it using
#                the scan function (bpl_scanner.py). It then
#                evaluates and executes these tokens. The value
#                of any expression is found using evaluate
#                (bpl_expressions.py).
#
#********************************************************
import bpl_scanner
import bpl_expressions
import sys
import re

symbolTable = {}  # holds variable names types and values


#************************************************
#
# Function: interpreter
#
# Parameters: none
#
# Purpose:  interpret and execute a program 
#           written in bpl 
#
# Calls: function open
#        function readlines
#        function close
#        bpl_scanner fucntion scan
#        function evaluate
#
#************************************************
def interpreter():
    bplProgram = open(sys.argv[1],'r')
    lines = bplProgram.readlines()
    bplProgram.close()
    scan = bpl_scanner.scan
    for line in lines:
        line = line.strip() 
        if line != '' and line[0] != '#':
            if line[-1] != ';':
                print ('***Error: Missing semicolon***')
                break
                
            evaluate(scan(line))

#************************************************
#
# Function: evaluate
#
# Parameters: tokens - tokenized line from bpl 
#                      program
#
# Purpose:  calls function to evaluate token
#           based on what type the token is
#
# Calls: function evaluateDeclaration
#        function evlauateAssignment
#        function evaluatePrint
#        function evaluateRead
#
#************************************************
def evaluate(tokens):
    if tokens[0][0] == 'TYPE': evaluateDeclaration(tokens)
    elif tokens[0][0] == 'VAR': evaluateAssignment(tokens)
    elif tokens[0][1] == 'print': evaluatePrint(tokens)
    elif tokens[0][1] == 'read': evaluateRead(tokens)

#************************************************
#
# Function: evaluateDeclaration
#
# Parameters: tokens - tokenized line from bpl 
#                      program
#
# Purpose:  add variables to symbolTable
#
# Calls: syntaxCheck
#
#************************************************
def evaluateDeclaration(tokens):
    if not syntaxCheck(tokens):
        print('***Error: Invalid declaration syntax ***')
        exit()
    if tokens[0][1] == 'DOUBLE': default = 0.0
    else: default = ''
    for i in tokens:
        if i[0] == 'VAR': symbolTable[i[1]] = [tokens[0][1], default]

#************************************************
#
# Function: evaluateAssignment
#
# Parameters: tokens - tokenized line from bpl 
#                      program
#
# Purpose:  assigns a value to a variable in
#           the symbolTable
#
# Calls: function edit
#        bpl_espressions function evaluate
#
#************************************************
def evaluateAssignment(tokens):
    var = tokens[0][1]
    try:
        varType = symbolTable[var][0]
        if tokens[2][0] == 'VAR':
            symbolTable[var][1] = symboltable[tokens[2][1]][1]
        elif tokens[2][0] == 'STRING':
            symbolTable[var][1] = edit(tokens[2][1])
        elif tokens[2][0] == 'DOUBLE':
            symbolTable[var][1] == tokens[2][1]
        elif tokens[2][0] == 'EXP':
            symbolTable[var][1] = bpl_expressions.evaluate(tokens[2][1],varType,symbolTable)
    except KeyError:
        print('***Error: Use of undeclared variable***')
        exit()


#************************************************
#
# Function: evaluatePrint
#
# Parameters: tokens - tokenized line from bpl 
#                      program
#
# Purpose:  output what is to be printed to screen
#
# Calls: function edit
#        function str
#        bpl_expressions function evaluate
#
#************************************************
def evaluatePrint(tokens):
    string = ''
    for i in tokens[1:]:
        if i[0] == 'STRING':
            string += edit(i[1])
        elif i[0] == 'DOUBLE':
            string += str(i[1])
        elif i[0] == 'VAR':
            try:
                string += str(symbolTable[i[1]][1])
            except KeyError:
                print('***Error: Use of undeclared variable***')
                exit()
        elif i[0] == 'EXP':
            if isDoubleExp(i[1]):
                string += str(bpl_expressions.evaluate(i[1],'DOUBLE',symbolTable))
            else:
                bpl_expressions.evaluate(i[1],'STRING',symbolTable)
    print(string, end='')
            
        
#************************************************
#
# Function: evaluateRead
#
# Parameters: tokens - tokenized line from bpl 
#                      program
#
# Purpose:  read in value from user and add it
#           to a variable in symbol table
#
# Calls: function input
#        function split
#        function float
#
#************************************************
def evaluateRead(tokens):
    try:
        if symbolTable[tokens[1][1]][0] == 'STRING':
            temp = input()
            symbolTable[tokens[1][1]][1] = temp
        elif symbolTable[tokens[1][1]][0] == 'DOUBLE':
            temp = input().split()
            index = 0;
            for i in tokens[1:]:
                if i[0] == 'VAR':
                    symbolTable[i[1]][1] = float(temp[index])
                    index += 1
    except KeyError:
        print('***Error: Use of undeclared variable***')
        exit()
           
                    

#************************************************
#
# Function: edit
#
# Parameters: string - a string from the program
#
# Purpose:  edit string for proper output
#
# Calls: re function findall
#        string function replace
#        function str
#
#************************************************
def edit(string):
    variables = re.findall('@\((\w*)\)',string)
    for i in variables:
        string = string.replace('@(' + i + ')',str(symbolTable[i][1]))
    return string.replace('\\t','    ').replace('\\n','\n')

#************************************************
#
# Function: isDoubleExp
#
# Parameters: exp - a string representation of an 
#                   expression
#
# Purpose:  returns true if exp is a double expression 
#           and false if not
#
# Calls: function split
#        bpl_scanner function isFloat
#
#************************************************
def isDoubleExp(exp):
    OPERATORS = ['(', ')', '+', '-', '*', '/'] 
    for i in OPERATORS:
        exp = exp.replace(i, ' ')
    exp = exp.split()
    for i in exp:
        if bpl_scanner.isFloat(i): return True
        elif i in symbolTable: return bpl_scanner.isFloat(symbolTable[i][1])
    return False
    
#************************************************
#
# Function: syntaxCheck
#
# Parameters: tokens - tokenized line from bpl 
#                      program
#
# Purpose:  checks that declaration has corrent
#           syntax
#
# Calls: function len
#
#************************************************
def syntaxCheck(tokens):
    OPERATORS = ['(', ')', '+', '-', '*', '/']
    i = 0;
    while i < len(tokens) - 1:
        if tokens[i][0] == 'VAR':
            if tokens[i+1][0] != 'COMMA' and tokens[i+1][0] != 'SEMI': return False
            for j in tokens[i][1]:
                if j in OPERATORS: return False
        i += 1
    return True         

if len(sys.argv) == 2:  # Checks for valid number of command line arguments
    interpreter()
else:
    print('Error: Invalid number of command line arguments')
    print('Please try running the program again with one command line argument')

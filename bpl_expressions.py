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
#                evaluate expressions from bpl programs.
#
#********************************************************
from stackClass import Stack
import re
#************************************************
#
# Function: evaluate
#
# Parameters: exp - a string representation of 
#                   an expression
#             expType - the type of exp (string, double)
#             symbolTable - symbol table used by 
#                           intrepreter
#             
#
# Purpose:  returns the evaluation of exp
#
# Calls: string function split
#        string function replace
#        function evaluateString
#        function evaluateDouble
#
#************************************************
def evaluate(exp,expType, symbolTable):
    TYPE = 0
    VALUE = 1
    OPERATORS = ['(', ')', '+', '-', '*', '/']   

    #************************************************
    #
    # Function: evaluateDouble
    #
    # Parameters: exp - a string representation of 
    #                   a double expression
    #
    # Purpose:  return the evalution of exp
    #
    # Calls: function infixToPostfix
    #        function evaluatePostfix
    #
    #************************************************ 
    def evaluateDouble(exp):
        exp = infixToPostfix(exp)
        return evaluatePostfix(exp)

    #************************************************
    #
    # Function: evaluateString
    #
    # Parameters: exp - a string representation of 
    #                   a string expression
    #
    # Purpose:  return the evaluation of exp
    #
    # Calls: string function strip
    #        string function replace
    #
    #************************************************ 
    def evaluateString(exp):
        newString = ''
        for string in exp:
            if '"' in string: 
                string = string.strip().replace('"','')
                string = edit(string)
            else: string = symbolTable[string.strip()][VALUE]
            newString += string
        return newString

    def edit(string):
        variables = re.findall('@\((\w*)\)',string)
        for i in variables:
            string = string.replace('@(' + i + ')',symbolTable[i][1])
        return string.replace('\\t','    ').replace('\t','    ').replace('\\n','\n')
            
    
   
    #************************************************
    #
    # Function: infixToPostfix
    #
    # Parameters: exp - a string infix expression
    #
    # Purpose:  return a postfix string list
    #
    # Calls: string function replace
    #        string fucntion split
    #        Stack constuctor
    #        Stack function push
    #        Stack function peek
    #        Stack function pop
    #        Stack function isEmpty
    #
    #************************************************
    def infixToPostfix(exp):
        postfix = ''
        PRECEDENCE = {'=' : 0, '(' : 1, '+' : 2, '-' : 2, '*' : 3, '/' : 3}
        operatorStack = Stack()
        i = 0
        while i < len(exp):
            if exp[i] not in OPERATORS:
                postfix += exp[i] + ' '
                i += 1
            elif exp[i] == '(':
                operatorStack.push(exp[i])
                i += 1
            elif exp[i] == ')':
                while operatorStack.peek() != '(':
                    postfix += operatorStack.pop() + ' '
                operatorStack.pop()
                i += 1
            elif operatorStack.isEmpty() or PRECEDENCE[exp[i]] > PRECEDENCE[operatorStack.peek()]:
                operatorStack.push(exp[i])
                i += 1
            elif PRECEDENCE[exp[i]] <= PRECEDENCE[operatorStack.peek()]:
                postfix += operatorStack.pop() + ' '
        while not operatorStack.isEmpty():
            postfix += operatorStack.pop() + ' '
        return postfix[:-1].split()

   
    #************************************************
    #
    # Function: evaluatePostfix
    #
    # Parameters: exp - a string list postfix expression
    #
    # Purpose:  return the result of l and r, operated
    #           on by the operator that parameter operator
    #           is representing
    #
    # Calls: function isFloat
    #        function float
    #        function evaluate
    #        Stack constuctor
    #        Stack function push
    #        Stack function pop
    #
    #************************************************         
    def evaluatePostfix(exp):
        operandStack = Stack()
        for i in exp:
            if i not in OPERATORS:
                if isFloat(i): operandStack.push(float(i))
                else: operandStack.push(symbolTable[i][VALUE])
            else:
                r = operandStack.pop()
                l = operandStack.pop()
                operandStack.push(evaluateMath(l,i,r))
        return operandStack.pop()

    #************************************************
    #
    # Function: evaluate
    #
    # Parameters: l - number on left side of operator
    #             operator - a string of an operator
    #             r - number on right side of operator
    #
    # Purpose:  return the result of l and r, operated
    #           on by the operator that parameter operator
    #           is representing
    #
    # Calls: none
    #
    #************************************************
    def evaluateMath(l,operator,r):
        if operator == '+':
            return l + r
        elif operator == '-':
            return l - r
        elif operator == '*':
            return l * r
        elif operator == '/':
            return l / r


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
        
    if expType == 'DOUBLE':
        for i in OPERATORS:
            exp = exp.replace(i, ' ' + i + ' ')
        exp = exp.split()
        return evaluateDouble(exp)
    elif expType == 'STRING':
        exp = exp.split('+')
        return evaluateString(exp)

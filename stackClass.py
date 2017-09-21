#************************************************
#
# Class: Stack
#
# Author: interactivepython.org
#
# Description: This file contains the class Stack.
#              This is not my code, it was found on
#              the website interactivepython.org
#
# Link:  http://interactivepython.org/courselib/static/pythonds/BasicDS/ImplementingaStackinPython.html
#
#************************************************
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

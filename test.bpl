# BPL Test Program
print "This is my first program\n";
string greeting, name;
greeting = "Bobcat Programming " + "Language (BPL)";
print greeting, "\n";
print "Enter your name\n";
read name;
string myname;
print "Your name is @(name)", "\n";
greeting = " Welcome " + name + " to CS 3200\n";
print "greeting is ", greeting, "\n";

# some double calculations
double x, y, z;
print "Enter the value of x and y ";
read x, y;
y = y + 13;
z = ((2 +x)*y)*2 + 			50;
print "The value of x is: \t\t", x, "\n";
print "The value of y is: \t", y, "\n";
print "The value of z is: \t", z, "\n";

print "@(name): Value of (23+5-2*x) is ", (23+5-2*x), ", where x = @(x)", "\n";

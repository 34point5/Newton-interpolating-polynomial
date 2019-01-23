#!/usr/bin/env python

from sys import argv
from os import system
from collections import Counter
from matplotlib.pyplot import *
import sympy
import numpy

system('clear')
print '-----'

# validate arguments
if len(argv) != 3:
	print 'valid usage:'
	print '\t./interpolate.py <coefficients file> <interpolation resolution>'
	print '\tpython interpolate.py <coefficients file> <interpolation resolution>'
	print '-----'
	raise SystemExit

# check if input file exists
try:
	points = open(argv[1])
except IOError:
	print 'File \'%s\' not found.' % argv[1]
	print 'files in current directory:'
	system('ls --color=always')
	print '-----'
	raise SystemExit

# check if numer of points is valid
try:
	resolution = abs(int(argv[2]))
except ValueError:
	print 'Argument \'%s\' is not an integer.' % argv[2]
	print 'Give the number of interpolation points to be generated as an integer.'
	print '-----'
	raise SystemExit

# check contents of input file
try:
	n = abs(int(points.readline())) # number of points, not the degree of the polynomial
	x = [float(item_x) for item_x in points.readline().strip().split(' ')]
	y = [float(item_y) for item_y in points.readline().strip().split(' ')]
	points.close()
except ValueError:
	print 'The contents of \'%s\' are not in the specified format.' % argv[1]
	print 'format:'
	print '\t<number of points>'
	print '\t<space-separated list of horizontal coordinates>'
	print '\t<space-separated list of vertical coordinates>'
	print '-----'
	raise SystemExit

# obviously
if resolution <= n:
	print 'The number of points given is not more than the number of points required.'
	print 'No interpolation is necessary.'
	print '-----'
	raise SystemExit

# check if the number of the horizontal coordinates is correct
if len(x) != n:
	print x
	print 'There are %d horizontal coordinates in \'%s\' but %d are expected.' % (len(x), argv[1], n)
	print '-----'
	raise SystemExit

# check if the number of the vertical coordinates is correct
if len(y) != n:
	print y
	print 'There are %d vertical coordinates in \'%s\' but %d are expected.' % (len(y), argv[1], n)
	print '-----'
	raise SystemExit

# get all occurrences of some item in a list
# print [i for i, x in enumerate('random funny useless list') if x == 'e']

# check if points are legal
frequency = Counter(x)
repetitions = [item for item in frequency if frequency[item] > 1]
if repetitions != []:
	print 'There are repeated horizontal coordinates in \'%s\'.' % argv[1]
	print x
	print 'The following points appear more than once.'
	print repetitions
	print '-----'
	raise SystemExit

# the collection of all divided difference coefficients
# initialize it with all vertical coordinates
diff = [y]

# obtain all orders of divided difference coefficients
for count in range(n - 1):
	temporary_list = [(diff[count][index + 1] - diff[count][index]) / (x[index + count + 1] - x[index]) for index in range(n - count - 1)]
	diff.append(temporary_list)

# obtain the polynomial p(z)
z = sympy.symbols('z')
p = diff[0][0] # constant term
q = 1 # initializing something for the loop
for count in range(1, n):
	q *= z - x[count - 1] # all the terms containing the variable
	p = sympy.simplify(p + diff[count][0] * q) # each new term is added

# extract the polynomial coefficients from the SymPy polynomial
coefficients = sympy.Poly(p, z).coeffs()

# convert SymPy floats to ordinary floats
coefficients = [float(item) for item in coefficients]

# evaluate the polynomial at some set of point which include the given points
left = min(x)
right = max(x)
wide_x = numpy.linspace(left, right, resolution)
wide_y = numpy.polyval(coefficients, wide_x)

# display approximate coefficients
print 'interpolating polynomial:'
approximate_coefficients = '[%s]' % ', '.join(map(str, ['%.2f' % item for item in coefficients]))
print '\tpower\tcoefficient'
for index, item in enumerate(coefficients):
	print '\t %d\t' % (n - index - 1),
	print '%s' % str('%.2f' % item).rjust(int(6 + numpy.log10(max(coefficients))))

# plot the points and the polynomial
figure().canvas.set_window_title('polynomial interpolation')
plot(wide_x, wide_y, 'b-', label = r'$y = p(x)$', linewidth = 0.8)
plot(x, y, 'r.', label = 'given samples', linewidth = 0.8)
legend()
title(r'$p\equiv\,$%s' % approximate_coefficients)
xlabel(r'$x$')
ylabel(r'$y$')
grid(True)
show()

print '-----'

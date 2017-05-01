#!/usr/bin/env python3
import sys, argparse, os
import pandas as pd
from scipy import stats

parser = argparse.ArgumentParser(description='Convert CSV file to PGFPlots for use in TeX. Optional arguments for regression.', epilog=r'Be sure to include \usepackage{pgfplots}. This script depends on SciPy and Pandas.')

# Positional (i.e. required) arguments
parser.add_argument('csv', help='The CSV file to be converted')

# Optional arguments
parser.add_argument('-r', '--regress', help='Perform simple linear regression?', action='store_true')
parser.add_argument('-x', '--xlabel', help='Label for x axis')
parser.add_argument('-y', '--ylabel', help='Label for y axis')
parser.add_argument('-t', '--title', help='Title of graph')

# Parse arguments
args = parser.parse_args()

# Read CSV
data = pd.read_csv(args.csv)

# Get column names from CSV
x_col = list(data)[0]
y_col = list(data)[1]

# Get row information from CSV
x_data = data[x_col]
y_data = data[y_col]

x_max = max(x_data)
x_min = min(x_data)

y_max = max(y_data)
y_min = min(y_data)

# If labels are specified, use those. Otherwise use column names and CSV title.
if args.xlabel == None:
    x_lab = x_col
else:
    x_lab = args.xlabel

if args.ylabel == None:
    y_lab = y_col
else:
    y_lab = args.ylabel

if args.title == None:
    title = os.path.splitext(os.path.basename(args.csv))[0]
else:
    title = args.title

# Format actual data

formatted_data = ""
for i in range(len(x_data)):
    formatted_data += r"  (" + str(x_data[i]) + "," + str(y_data[i]) + r")" + '\n'

# Compute regression, if desired.

def compute_regression(x,y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    reg = (
    r'\addplot [' '\n'
    r'    domain=' + str(round(x_min,2)) + ":" + str(round(x_max,2)) + ',' '\n'
    r'    samples=100, ' '\n'
    r'    color=red,' '\n'
    r']' '\n'
    r'{.00001 + 0.8571 * x};' '\n'
    r'\addlegendentry{$y \approx ' + str(round(intercept,2)) + ' + ' + str(round(slope,2))  + '\cdot x$}' '\n\n'
    )
    return reg

if args.regress:
    regress = compute_regression(x_data,y_data)
else:
    regress = ""    

#Base string used for a PGFPlot.  Will add more options over time.
s = (r'\begin{figure}[h]' '\n'
r'\begin{center}' '\n'
r'\begin{tikzpicture}' '\n'
r'\begin{axis}[' '\n'
r'    axis lines = left,' '\n'
r'    xlabel = {' + x_lab + r'},' '\n'
r'    ylabel = {' + y_lab + r'},' '\n'
r'    title = {' + title + r'}' '\n'
r']' '\n'
+ regress + 
r'\addplot[only marks] coordinates {' '\n'
+ formatted_data +
r'  };' '\n\n'

r'\end{axis}' '\n'
r'\end{tikzpicture}' '\n'
r'\end{center}' '\n'
r'\end{figure}')

print(s)




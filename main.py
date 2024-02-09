
# This program generates metrical stress tableaux in a format compatible with OTSoft, a software that offers various ways to investigate theories within the OT framework
# The program does the following:
# 1. Generates a set of inputs, with word lengths specified by user
# 2. Generates a set of candidates for each input, with stress levels selected by user
# 3. Computes constraint violations for each input-candidate pair, with a constraint set selected by the user
# 4. Prints tableaux (compatible with OTSoft) with all of the above information

import random
import os
import sys
from datetime import datetime   # for time stamp in file name
from constraints import *
from utils import *


# Parameters: set by user
constraints = constraints_Gordon      # Variable (list). Corresponds to one of the theories in constraints.py.
min_input_length = 2                  # Integer. Minimal number of syllables in an input
max_input_length = 7                  # Integer. Maximal number of syllables in an input
grid_tiers = [1,2]                    # List of integers. Number of grid levels in candidates: [1] for x1 level, [1,2] for x1+x2 levels, [2] for only single-stress candidates
DPS = True                            # Boolean. Determines whether to genearte additional inputs with a stress-attracting property on some syllable (maximally one per input).
REP = False                           # Boolean. Determines whether to genearte additional inputs with a stress-repelling property on some syllable (maximally one per input).


# Automatic setting of a boolean parameter based on the selected constraint set.
# Determines whether candidates have an active edge (@ diacritic).
if constraints == constraints_AE or constraints == constraints_AE_AlignEdges:
    active_edge_Gen = True                  
else:  
    active_edge_Gen = False                  


### Generate inputs based on user specifications
inputs = get_inputs(min_input_length,max_input_length,DPS,REP)


### Generate candidates for each inputs based on user specifications
inp_and_cands = []
for i in range(0,len(inputs)):
    cands = get_candidates(input=inputs[i],tiers=grid_tiers,active_edge=active_edge_Gen)
    inp_and_cands.append([inputs[i],cands])


### Generate tableaux (for OTSoft)
# "tableaux" is a list of lists, each list corresponds to a single candidate and has the format [input,candidate,[violation1,violation2,...violationn]] 
tableaux = []

for pair in inp_and_cands:
    input, cands = pair
    for cand in cands:
        cand_pair = [input,cand]
        violations = count_violations(cand_pair,constraints)
        tableaux.append([input,cand,violations])

string_constraints = ''
for constraint in constraints:
    string_constraints = string_constraints + '  ' + constraint
print(string_constraints)
for tableau in tableaux[:50]:
    print(tableau)


# Print "tableaux" into a text file in OTSoft-compatible format
current_datetime = datetime.now().strftime("%Y-%m-%d %H.%M.%S")
file_name = current_datetime + ' ' + 'OTSoft input.txt'
if not os.path.isdir('Inputs_OTSoft'):
    os.mkdir("Inputs_OTSoft") # Create subdirectory
os.chdir("Inputs_OTSoft") # Change the current working directory to "subdir" 
with open(file_name,"w") as file:
    # print two lines with constraint names
    for i in range(0,2):
        file.write('\t'+'\t')
        for constraint in constraints:
            file.write('\t' + str(constraint))
        file.write('\n')
    # print inputs, candidates, and constraint violations
    current_input = ''
    for candidate_line in tableaux:
        input, surface, violations = candidate_line
        violations = '\t'.join([str(i) for i in violations])
        if candidate_line[0] == current_input:
            file.write('\t' + surface + '\t\t'+ violations + '\n') 
        else:
            file.write(input + '\t' + surface + '\t\t' + violations + '\n')
            file.write('\t' + surface + '\t\t'+ violations + '\n') # Repeating the first candidate in another line because of a bug in OTSoft
            current_input = candidate_line[0]






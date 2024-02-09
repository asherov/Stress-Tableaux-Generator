
# This file defines functions that do the following:
# 1. Generate a set of inputs, with word lengths specified by user
# 2. Generate a set of candidates for each input, with stress levels selected by user
# 3. Compute constraint violations for each input-candidate pair, with a constraint set selected by the user

import re
import itertools
from constraints import *

# Generate inputs
# Each input is a string (=word), each character denotes a syllable
# o =syllable with no special properties
# D = syllable with a stress-attracting property (for "DPS")
# R = syllable with a stress-repelling property (for "Repel")
# For technical reasons make the simplification that DPS and REP are always a part of the input; in actuality but they are sometimes a derived property (likewise for syllabification)
def get_inputs(min_length=2,max_length=7,dps=False,rep=False):
    
    inputs = []

    base_inputs = []
    for i in range(min_length,max_length+1):
        # the basis for input generation -- one form per word length
        input = ["o"]*i
        base_inputs.append(input)
        # inputs without any stress-attrcting or stress-repelling syllables
        plain_input = ''.join(input)    
        inputs.append(plain_input)

    # Generate all possible permutations with one stress-attracting syllable
    if dps == True:
        inputs_with_stress = base_inputs.copy()
        for input in base_inputs:
            current_input = input
            current_input[0] = 'D'
            D_inputs = [''.join(p) for p in itertools.permutations(current_input,len(input))]
            inputs = inputs + list(set(D_inputs))
    
    # Generate all possible permutations with one stress-repelling syllable
    if rep == True:
        inputs_with_heavies = base_inputs.copy()
        for input in base_inputs:
            current_input = input
            current_input[0] = 'R'
            R_inputs = [''.join(p) for p in itertools.permutations(current_input,len(input))]
            inputs = inputs + list(set(R_inputs))

    # Generate all possible permutations with one stress-attracting and one stress-repelling syllable
    if dps == True and rep == True:
        inputs_with_heavies = base_inputs.copy()
        for input in base_inputs:
            current_input = input
            current_input[0] = 'D'
            current_input[1] = 'R'
            DnR_inputs = [''.join(p) for p in itertools.permutations(current_input,len(input))]
            inputs = inputs + list(set(DnR_inputs))

    return inputs


# Generate candidates with different stress patterns
# The value of the digit denotes the level of stress, as follows:
# 0 = unstressed, 1 = secondary stress , 2 = primary stress
def get_candidates(input,tiers,active_edge=False):

    # get number of syllables
    word_length = len(input)

    ## get all possible stress assignments for tier 1
    if 1 in tiers:
        tier_1_patterns = []
        current_stress = ['o']*word_length    # create a list of n repetitions of '0'
        for i in range(0,word_length):
            current_stress[i] = 's'
            new_stress_permutations = [''.join(p) for p in itertools.permutations(current_stress,word_length)]
            tier_1_patterns = tier_1_patterns + new_stress_permutations
        tier_1_patterns = list(set(tier_1_patterns))  # to remove duplicates
    
        # for each tier 1 pattern, get all positions of tier 2 stress
        if 2 in tiers:
            tier_2_patterns = []
            for tier_1_pattern in tier_1_patterns:
                # find the indeces of tier 1 stresses in the candidate
                indeces_tier1 = [i.start() for i in re.finditer('s', tier_1_pattern)]
                # crate all possible tier 2 locations based on existing tier 1 stresses
                for index in indeces_tier1:
                    tier_2_candidate = list(tier_1_pattern)
                    tier_2_candidate[index] = 'S'
                    tier_2_pattern = ''.join(map(str,tier_2_candidate))
                    tier_2_patterns.append(tier_2_pattern)
            patterns = tier_2_patterns
        else:
            patterns = tier_1_patterns
    
    ## Alternative: get only single-stress patterns
    else:
        single_stress_patterns = []
        for i in range(0,word_length):
            current_stress = ['o']*word_length
            current_stress[i] = 'S'
            new_stress_permutations = [''.join(current_stress)]
            single_stress_patterns = single_stress_patterns + new_stress_permutations
        patterns = single_stress_patterns 

    ## Create a right-active-edge and left-active-edge candidates for each pattern
    if active_edge:
        patterns_with_active_edges = []
        ActiveEdge = '@'
        for i in range(0,len(patterns)):
            patterns_with_active_edges.append(patterns[i]+ActiveEdge)
            patterns_with_active_edges.append(ActiveEdge+patterns[i])
        patterns = patterns_with_active_edges
    
    return patterns


# Calculate violations of constraints for each candidate
def count_violations(candidate,constraints):
    # input
    # candidate: a list of two items – input, surface form
    # constraints: a list of constraints, each constraint is a list of four items: constraint name, regex, type (M for markedness or Faithfulmess), gradience (G for gradient, C for categorical)
    # output: a vector of integers, each correponds to the number of violations for one constraint for the present candidate
    candidate_input, candidate_surface = candidate
    cand_surface_stripped = candidate_surface.replace('@','')  # For calculating violations while ignoring active edge character
    violations = []
    for constraint in constraints:
        
        if 'AlignAll' in constraint: # Gradient align calculating distance in *syllables* for *every stress*
            if 'L' in constraint:
                distances = [i for i in range(len(cand_surface_stripped)) if cand_surface_stripped[i]=='s' or cand_surface_stripped[i]=='S']
            elif 'R' in constraint:    
                distances = [len(cand_surface_stripped)-i-1 for i in range(len(cand_surface_stripped)) if cand_surface_stripped[i]=='s' or cand_surface_stripped[i]=='S']
            elif 'AE' in constraint:
                if bool(re.search('^@',candidate_surface)):
                    distances = [i for i in range(len(cand_surface_stripped)) if cand_surface_stripped[i]=='s' or cand_surface_stripped[i]=='S']
                elif bool(re.search('@$',candidate_surface)):
                    distances = [len(cand_surface_stripped)-i-1 for i in range(len(cand_surface_stripped)) if cand_surface_stripped[i]=='s' or cand_surface_stripped[i]=='S']
                else:
                    raise TypeError('There is a problem with AlignAll/AE.')
            else:
                raise TypeError('There is no such alignment constraints.')
            num_violations = sum(distances)
        
        elif 'Align/Edges' in constraint: # Gradient, the sum of violations for AlignSome/R and AlignSome/L from Gordon
            num_violations = len(re.findall(CON['Align/R'],candidate_surface)) + len(re.findall(CON['Align/L'],candidate_surface))

        elif 'DPS' in constraint:
            num_violations = 0
            if len(cand_surface_stripped) != len(candidate_input):
                raise TypeError('Input and stripped candidate do not have identical length.')
            for i in range(len(candidate_input)):
                if re.match(r"D",candidate_input[i]) and re.match(r"o",cand_surface_stripped[i]):
                    num_violations = num_violations + 1

        elif 'REP' in constraint:
            num_violations = 0
            if len(cand_surface_stripped) != len(candidate_input):
                raise TypeError('Input and stripped candidate do not have identical length.')
            for i in range(len(candidate_input)):
                if re.match(r"R",candidate_input[i]) and re.match(r"[sS]",cand_surface_stripped[i]):
                    num_violations = num_violations + 1
    
        elif 'A-*Clash' in constraint: # An adjusted version of *Clash – clashes with peak get 2 violations: Assign one * for each unique pair of grid marks above level 1 in adjacent columns
            num_violations = len(re.findall(CON['*Clash'],candidate_surface)) + len(re.findall(CON['*Clash-at-Peak'],candidate_surface))

        elif 'A-*Lapse' in constraint: # An adjusted version of *Clash – clashes with peak get 2 violations: Assign one * for each unique pair of grid marks above level 1 in adjacent columns
            num_violations = len(re.findall(CON['*Lapse'],candidate_surface)) + len(re.findall(CON['*Lapse-not-at-Peak'],candidate_surface))

        elif 'AlignPeak_syl' in constraint: # Gradient align calculating distance in *syllables* for *the peak*
            if 'L' in constraint:        
                num_violations = cand_surface_stripped.index('S')
            elif 'R' in constraint:
                num_violations = len(cand_surface_stripped)-cand_surface_stripped.index('S')-1
            elif 'AE' in constraint:
                if bool(re.search('^@',candidate_surface)):
                    num_violations = cand_surface_stripped.index('S')
                elif bool(re.search('@$',candidate_surface)):
                    num_violations = len(cand_surface_stripped)-cand_surface_stripped.index('S')-1
                else: 
                    raise TypeError('There is a problem with AlignPeak/AE.')
            else:
                raise TypeError('There is no such alignment constraints.')

        # Heinz et al.'s constraints

        elif 'FirstStressLeft' in constraint: 
            num_violations = (len(re.findall(CON['Align/L'],candidate_surface)) * 2) + len(re.findall('^[^S]*s',candidate_surface))

        elif 'LastStressRight' in constraint: 
            num_violations = (len(re.findall(CON['Align/R'],candidate_surface)) * 2) + len(re.findall('s[^S]*$',candidate_surface))

        elif 'Clash-at-Initial' in constraint: 
            num_violations = (len(re.findall('(?<!^)(?=([sS][sS]))',candidate_surface)) * 2) + len(re.findall('^[sS][sS]',candidate_surface))

        elif 'Clash-near-Right' in constraint: 
            num_violations = (len(re.findall('(?=([sS][sS].*..$))',candidate_surface)) * 2) + len(re.findall('[sS][sS].$',candidate_surface)) + len(re.findall('[sS][sS]$',candidate_surface))

        elif 'Lapse-near-Left' in constraint:  
            num_violations = (len(re.findall('(?<!^..)(?=(oo))',candidate_surface)) * 2) + len(re.findall('^oo',candidate_surface)) + len(re.findall('^.oo',candidate_surface))

        elif 'Lapse-near-Right' in constraint: 
            num_violations = (len(re.findall('(?=(oo.*...$))',candidate_surface)) * 2) + len(re.findall('oo..$',candidate_surface)) + len(re.findall('oo.$',candidate_surface)) + len(re.findall('oo$',candidate_surface))

        elif 'H_*Clash-at-Peak' in constraint: 
            num_violations = (len(re.findall('(?=(sS|Ss))',candidate_surface)) * 2) + len(re.findall('(?=(ss))',candidate_surface))

        elif 'H_Lapse-at-Peak' in constraint:  
            num_violations = (len(re.findall('(?<!(S))(?=(oo[^S]))',candidate_surface)) * 2) + len(re.findall('(?=(ooS|Soo))',candidate_surface))

        else:
            num_violations = len(re.findall(CON[constraint],candidate_surface))
    
        num_violations = max(0,num_violations)     # Avoid negative number of violations, specifically due to G-*(Ext)Lapse

        violations.append(num_violations)
    
    return violations
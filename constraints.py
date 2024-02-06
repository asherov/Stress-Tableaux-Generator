
# This file defines constraints on metrical stress
# Constraints are organized in a dictionary, where keys are constraint names (strings) and values are regular expressions matching any violation of the constraint (strings)
# Constraints that cannot be reduced to regular expressions have value None and are defines separately in the violation-assignment function (count_violations in utils.py)


CON = { 
        ## General constraints
    
        # Rhythm
        '*Clash':'(?=([sS][sS]))',
        '*Lapse':'(?=(oo))',                
        '*Clash-at-Peak':'(?=(sS|Ss))',
        '*Lapse-not-at-Peak':'(?=([^S]oo[^S]))',       
        '*Lapse-in-Trough':'(soos)',         # From Kager (2005), replaces *Lapse-not-at-Peak (Kager 2001, 2004)
        '*ExtClash':'(?=([sS]o?[sS]))',      # probably not needed in the theory, subsumed by other stress-minimizing constraints (see Elenbaas 1999; Staub 2014)
        '*ExtLapse':'(?=(ooo))',             # see Elenbaas 1999; Staub 2014

        # Categorical alignment -- not compatible with AE representations
        'Stress/L':'^o',                     # Categorical version (causes window-breaking pathology)
        'Stress/R':'o$',                     # Categorical version (causes window-breaking pathology)
        '*Lapse/L':'^oo',                    # Categorical version (causes window-breaking pathology)
        '*Lapse/R':'oo$',                    # Categorical version (causes window-breaking pathology)
        '*ExtLapse/L':'^ooo',                # Categorical version (causes window-breaking pathology)
        '*ExtLapse/R':'ooo$',                # Categorical version (causes window-breaking pathology)
        'Stress/Edges':'((^o)|(o$))',        # Categorical version (causes window-breaking pathology)
        'RightMost':'S.*s',                  # Assign one * if the peak is followed by some stress (categorical)
        'LeftMost':'s.*S',                   # Assign one * if the peak is preceded by some stress (categorical)

        # Gradient alignment
        'AlignAll/L':None,                   # violations calculated without regex; For each stress, assign one * for every syllable separating the stress from the L edge
        'AlignAll/R':None,                   # violations calculated without regex; For each stress, assign one * for every syllable separating the stress from the R edge
        'Align/L':'(?:(?<=^o)|(?<=^oo)|(?<=^ooo)|(?<=^oooo)|(?<=^ooooo)|(?<=^oooooo)|(?<=^@o)|(?<=^@oo)|(?<=^@ooo)|(?<=^@oooo)|(?<=^@ooooo)|(?<=^@oooooo))',       # For nearest stress; this must be done this way, because lookbehind can only scope over fixed-length sequences
        'Align/R':'o(?=o*@?$)',              # For nearest stress; can use the * quantifier here, because lookahead can also scope over non-fixed-length sequences
        'AlignPeak/L':'s(?=.*S)',         
        'AlignPeak/R':'((?<=S)s)|((?<=S.)s)|((?<=S..)s)|((?<=S...)s)|((?<=S....)s)|((?<=S.....)s)|((?<=S......)s)',         
        'AlignPeak_syl/L':None,              # violations calculated without regex; Assign one * for every syllable separating the peak from the L edge
        'AlignPeak_syl/R':None,              # violations calculated without regex; Assign one * for every syllable separating the peak from the R edge        
        
        # Stress repulsion
        'NonInit':'^[sS]',
        # 'NonFin':'[sS]$',                                # Reformulated in the AE set
        'ExtNonInit':'^.?[sS]',                            # Categorical (violated once if there is stress in the first two syllables)
        'ExtNonFin':'[sS].?$',                             # Categorical (violated once if there is stress in the last two syllables); Reformulated in the AE set
        'G-ExtNonInit':'(?:(?<=^[sS])|(?<=^.[sS]))',       # Gradient (violated by each stress in the first two syllables)
        'G-ExtNonFin':'(?:(?=[sS]$)|(?=[sS].$))',          # Gradient (violated by each stress in the last two syllables)
        
        # Other
        'Culminativity':'^[^S]*$',           # in current version of this code all candidates satisfy culminativity; note that this only counts a violation for words with no level 2 stress at all; it does not count a violation for words with multiple level 2 stresses                
        'OneStress':'s',                     # penalizes all stresses which are not the peak
   
        ## Constraints for the Active Edge system

        # Setting the active edge
        'AE/R':'[^@]$',
        'AE/L':'^[^@]',

        # Categorical alignment
        '*StressAE':'(@o|o@)', 
        '*LapseAE':'(@oo|oo@)',
        '*ExtLapseAE':'(@ooo|ooo@)',
        'InitialBeat':'^@?o',                     
        'PeakAE':'(@.*s.*S|S.*s.*@)',   # Assign one * if the peak is separated from the active edge by another stress

        # Gradient alignment 
        'AlignAll/AE':None,             
        'Align/AE':'((?:(?<=^@o)|(?<=^@oo)|(?<=^@ooo)|(?<=^@oooo)|(?<=^@ooooo)|(?<=^@oooooo))|(o(?=o*@$)))',     # For nearest stress
        'G-*Lapse/AE':'((?:(?<=^@oo)|(?<=^@ooo)|(?<=^@oooo)|(?<=^@ooooo)|(?<=^@oooooo))|(o(?=oo*@$)))',          # For nearest stress
        'G-*ExtLapse/AE':'((?:(?<=^@ooo)|(?<=^@oooo)|(?<=^@ooooo)|(?<=^@oooooo))|(o(?=ooo*@$)))',                # For nearest stress
        'AlignPeak/AE':'(s(?=.*S[^@]*$))|((?<=S)s(?=.*@))|((?<=S.)s(?=.*@))|((?<=S..)s(?=.*@))|((?<=S...)s(?=.*@))|((?<=S....)s(?=.*@))|((?<=S.....)s(?=.*@))|((?<=S......)s(?=.*@))',     
        'AlignPeak_syl/AE':None,     

        # Stress repulsion
        'NonPeriph/AE':'(@[sS]|[sS]@)',
        'ExtNonPeriph/AE':'(@o?[sS]|[sS]o?@)',                                                      # Categorical
        'G-ExtNonPeriph/AE':'(((?<=@)[sS])|((?<=@.)[sS])|([sS](?=(.@)))|([sS](?=(@))))',            # Gradient
        'A-ExtNonPeriph/AE':'(?<=@[sS])|(?<=@.[sS])|(?<=@[sS].)|(?=.[sS]@)|(?=[sS].@)|(?=[sS]@)',   # Adjusted – Assing one * if one of the two syllables at the AE bears stress and an additional * if the peripheral syllably at the AE bears stress
        
        'NonFin':'[sS]@?$',                           
        'ExtNonFin':'[sS]o?@?$',                                    # Categorical
        'G-ExtNonFin':'([sS](?=(.@?$))|[sS](?=(@?$)))',             # Gradient, Assign one * for each stress on the last two syllables
        'A-ExtNonFin':'(?=[sS].@?$)|(?=.[sS]@?$)|(?=[sS]@?$)',      # Adjusted, taken from Heinz et al. – Assing one * if one of the last two syllables bears stress and an additional * if the ultima bears stress

        # Reformulated rhythmic constraints
        '*NonFinalLapse':'(?=(oo[^$@]))',                           # Kager (2001: 4), though there is an overlap with the effect of ExtNonFin
        '*InternalClash':'(?=((?<!([@^]))[sS][sS](?!([$@]))))',     # Kager (2001: 11), though it's not clear whether he claims it is symmetrical for both edges
        '*InitialClash':'^@?[sS][sS]',                              # Staub (2014: 25) claims that there is a strong dispreference for initial clashes. But he doesn't actually compare clashes in different positions, just clashes w.r.t non-clashes at the edges.


        ## Constraints from Heinz et al.

        'FirstStressLeft':None,         # "incurs two violations for every X0 between the left word boundary and the leftmost stressed syllable. An additional violation is scored if the leftmost stressed syllable is secondary stressed"
        'LastStressRight':None,         # "incurs two violations for every X0 between the right word boundary and the rightmost stressed syllable. An additional violation is scored if the rightmost stressed syllable is secondary stressed"
        'NoInitialStress':'^@?[sS]',    # "incurs a violation if the initial syllable bears stress"
        # 'HaveInitialStress':None,     # Already exists as "Stress/L"
        # 'NoFinalStress':None,         # Already exists as "NonFin"
        # 'NoFinalFoot':None,           # Already exists as "A-ExtNonFin"
        'NoStress':'[sS]',              # "incurs a violation for each stressed syllable"
        #'NoExtLapse':None,             # Already exists as "*ExtLapse"
        #'NoExtLapseR':None,            # Already exists as "*ExtLapse/R"
        'Clash-at-Initial':None,        # "incurs one violation if there is clash between the initial and peninitial syllables, and two violations if there is a clash elsewhere"
        'Clash-near-Right':None,        # "incurs one violation if there is a clash between the final and penultimate syllables, one violation if there is a clash between the penultimate and antepenultimate syllables, and two violations if there is a clash elsewhere"
        'Lapse-near-Left':None,         # "incurs one violation if a lapse occurs among the first and second, or among the second or third syllables in a word. It incurs two violations for lapses ocurring elsewhere."
        'Lapse-near-Right':None,        # "incurs one violation if a lapse occurs among the final and penultimate syllables, or among the penultimate and antepenultimate syllables, or among the antepenultimate and pre-antepenultimate syllables. It incurs two violations for lapses ocurring elsewhere."
        }



# Create lists with a subset of the constraints to test various theories

# Constraint set from Asherov (2023)
constraints_AE = [
                'AE/R',
                'AE/L',
                'AlignPeak/AE',                
                'Align/AE',
                'G-*Lapse/AE',
                'G-*ExtLapse/AE',
                'NonPeriph/AE',
                'A-ExtNonPeriph/AE',
                'OneStress',
                'DPS',
                'REP',
                'NonFin',
                'Align/L',
                '*Lapse',           
                '*ExtLapse',
                '*Lapse-in-Trough',
                '*NonFinalLapse',
                '*Clash',           
                '*Clash-at-Peak',   
                ]



# Constraint set from Gordon (2002)
constraints_Gordon = [
                'AlignAll/L',
                'AlignAll/R',
                'Align/Edges',    
                'AlignPeak/L',
                'AlignPeak/R',
                '*Lapse/L',
                '*Lapse/R',
                '*ExtLapse/L',              # Added, not in original paper. Required for avoiding a known undergeneration problem
                '*ExtLapse/R',
                'NonFin',
                '*Clash',
                '*Lapse',
                '*ExtLapse',
                'DPS',
                'REP',
                ]

# Constraint set from Heinz et al. (2005)
constraints_HeinzEtAl = [
                'FirstStressLeft',
                'LastStressRight',
                'NoInitialStress',
                'Stress/L',                     # HaveInitialStress
                'NonFin',                       # NoFinalStress
                'A-ExtNonFin',                  # NoFinalFoot
                'NoStress',         
                '*ExtLapse',                    # NoExtLapse
                '*ExtLapse/R',                  # NoExtLapseR
                'Clash-at-Initial',        
                'Clash-near-Right',
                'Lapse-near-Left',
                'Lapse-near-Right',
                'H_*Clash-at-Peak',             # Inferred, not listed in their appendix
                'H_Lapse-at-Peak',              # Inferred, not listed in their appendix
                'DPS',                          # Added, not in original paper
                'REP',                          # Added, not in original paper
                ]

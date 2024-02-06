This code generates metrical stress tableaux in a format compatible with OTSoft, a software that offers various ways to investigate theories within the OT framework.

Specifically, this code does the following:
1. Generates a set of inputs, with word lengths specified by user
2. Generates a set of candidates for each input, with stress levels selected by user
3. Computes constraint violations for each input-candidate pair, with a constraint set selected by the user
4. Prints tableaux (compatible with OTSoft) with all of the above information

Notes:
- Possible stress levels for candidates include (a) only one stress or (b) both primary and secondary stresses
- The code is preconfigured with metrical stress constraints from three theories of stress in Optimality Theory: Gordon (2002), Heinz et al. (2005), and Asherov (2023)

References:
Asherov, Daniel. 2023. "Metrical Grids and Active Edges." Doctoral dissertation, MIT.
Gordon, Matthew. 2002. “A Factorial Typology of Quantity-Insensitive Stress.” Natural Language & Linguistic Theory 20 (3): 491–552.
Heinz, Jeffrey, Greg Kobele, and Jason Riggle. 2005. “Exploring the Typology of Quantity-Insensitive Stress Systems without Gradient Constraints.” Presented in the 79th Annual Meeting of the Linguistic Society of America, Oakland.


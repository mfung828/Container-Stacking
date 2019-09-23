# Container-Stacking
I attempt to use dynamic programming and heuristics to optimally rearrange n rectangular containers from a starting configuration to a specified end configuration. I start with holding space A in which sits the beginning Configuration A and holding space B, in which, initially sits no containers. By the end of the entire process, holding space A will be empty and holding space B will be in the end-goal configuration. 

The objective is to minimize the number of displacements of the containers (including the ones used directly to move Container A to its corresponding location A in the end goal configuration), with the constraint that containers displaced for the sake of accessing other containers may be placed temporarily in Holding Space A or B. Also, both configurations must be rectangular and the same size and dimensions. 

I initially implement a heuristic, mainly to identify whichever containers may be immediately placed in its proper corresponding end configuration location in Holding space B and greedily move these containers. Only when there are no longer any such readily accessible containers will the algorithm resort to implementing a dynamic programming approach.

The dynamic programming approach calls for a backwards chaining start point. Hence, I break the problem down into sub problems and solve for k=1 containers all the way to n. Practically speaking, however, because of the heuristic, it is highly unlikely that my algorithm will have to be implemented all the way to n. 

For each k, I find all states where there are k remaining containers left to be placed in the final configuration. This is essentially a combinatorics problem, where I have to find C, k of n number of feasible configurations. For example, if there are only 2 containers remaining and the end configuration were represented as a 2 row * 3 column matrix, then possibilities may include a configuration where there are 2 empty spaces on the top row, but certainly (because of gravity) not one where there are 2 empty spaces on the bottom row. 

For this combinatorics problem, I devised a strategy that maps container number to matrix position number. For example, given the configuration, where 0 denotes emptiness:

<img src="https://latex.codecogs.com/gif.latex? \begin{vmatrix}
0&0&3\\
4&5&6\\
\end{vmatrix} " />

the combinatorics problem reduces to the generation of C' number of subsets of k elements. 

Once all states- a tough feat since the generation of these subsets is factorially expensive, while the arrangement of each subset is also factorially expensive- are generated, I store each state and keep track of resultant states, optimal values, and scores, so that in the end, I may select the minimal policy. 

This type of project finds usage in many real-world applications such as rail Container stacking. It is important to minimize the number of displacements because in the real world, each displacement involves the usage of a crane, manpower and many labour-hours. Hence, the solving of this problem is extremely important. 


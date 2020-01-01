# TSP
This is my attempt to visualize/simulate the traveling salesman problem. 

The graph starts at (0, 0) and then tries to visit every point while trying to minimize the Euclidean distance. The number of points can be specified in the initialization
```
#i.e. for a (0, 0) and 5 other random points
#     initialize using:
plotCompareProblem(5)

#The default # of random points is 5
```
There are 2 simple algorithms used in this codebase for comparision

1) Brute force - basically trying all permutations and just reporting the minimum
2) Greedy - just go to the nearest one from the current

The brute force method is O(N!) complex algorithm and takes very long to run

Brute force is gureenteed to report the lowest distance while the greedy algorithm is simply a *best guess*

Some times (especially at small samples), the output is the same

![Alt text](image/same.png?raw=true "Same Outcome")

But the greedy algorithm is not gureenteed to be optimal

![Alt text](image/different?raw=true "Different Outcome")

The simulation can be ran using
```
python traveling.py
```
The code uses matplotlib and has been tested for python 3.7

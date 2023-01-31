import numpy as np
import tsp
import tsplib95

problem = tsplib95.load('qa194.tsp')

#print(problem)

temp = problem.as_name_dict()
res = temp["node_coords"]
print(res)
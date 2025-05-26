from search_algorithm import SearchAlgorithm
from queue import Queue 
from search_algorithm import Node

from queue import Queue

def bfs(problem):
    frontiera = Queue()
    frontiera.put((problem.init, [problem.init]))  
    visto = set()
    explored = []

    while not frontiera.empty():  
        current, path = frontiera.get()
        if current in visto:
            continue
        visto.add(current)
        explored.append(current)

        if problem.isGoal(current):
            return path, explored

        for successor, _ in problem.getSuccessors(current):  # ignora il costo
            if successor not in visto:
                frontiera.put((successor, path + [successor]))

    return [], explored

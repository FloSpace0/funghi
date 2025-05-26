from search_algorithm import SearchAlgorithm
from queue import LifoQueue
from search_algorithm import Node
class DFS(SearchAlgorithm):
    """Depth First Search

    Args:
        Solver (_type_): This is an implementation for the Solver class
    """
def dfs(problem):
    stack = [(problem.init, [problem.init])]
    visited = set()
    explored = []

    while stack:
        current, path = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        explored.append(current)
        if problem.isGoal(current):
            return path, explored

        for successor, _ in problem.getSuccessors(current):
            if successor not in visited:
                stack.append((successor, path + [successor]))

    return [], explored

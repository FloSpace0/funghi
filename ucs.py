from queue import PriorityQueue

def ucs(problem):
    frontiera = PriorityQueue()
    frontiera.put((0, problem.init, [problem.init]))  # (costo, stato, percorso)
    visited = {}
    explored = []

    while not frontiera.empty():
        cost, current, path = frontiera.get()

        if current in visited and visited[current] <= cost:
            continue

        visited[current] = cost
        explored.append(current)

        if problem.isGoal(current):
            return path, explored

        for successor, step_cost in problem.getSuccessors(current):
            totale = cost + step_cost
            if successor not in visited or totale < visited.get(successor, float('inf')):
                frontiera.put((totale, successor, path + [successor]))

    return [], explored

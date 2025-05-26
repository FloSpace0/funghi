from queue import PriorityQueue

def manhattan_heuristic(pos, goal):
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

def astar(problem, heuristic=manhattan_heuristic):
    frontiera = PriorityQueue()
    start = problem.init
    goal = problem.goal

    frontiera.put((0, 0, start, [start]))  # (f(n), g(n), stato, percorso)
    visited = {}
    explored = []

    while not frontiera.empty():
        f, g, current, path = frontiera.get()

        if current in visited and visited[current] <= g:
            continue

        visited[current] = g
        explored.append(current)

        if problem.isGoal(current):
            return path, explored

        for successor, step_cost in problem.getSuccessors(current):
            g_new = g + step_cost
            h = heuristic(successor, goal)
            f_new = g_new + h

            if successor not in visited or g_new < visited.get(successor, float('inf')):
                frontiera.put((f_new, g_new, successor, path + [successor]))

    return [], explored

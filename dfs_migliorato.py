def dfs(problem):
    frontiera = [(problem.init, [problem.init])]  # pila: lista usata come stack
    visto = set()
    explored = []

    while frontiera:  # controlla se la lista non è vuota
        current, path = frontiera.pop()  # prende l'ultimo elemento

        if current in visto:
            continue
        visto.add(current)
        explored.append(current)

        if problem.isGoal(current):
            return path, explored

        for successor, _ in reversed(problem.getSuccessors(current)):  
            if successor not in visto:
                frontiera.append((successor, path + [successor]))

    return [], explored

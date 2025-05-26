from search_problem import SearchProblem

# Movimento in 8 direzioni
DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 1),
              (1, 0), (1, -1), (0, -1), (-1, -1)]

class PathfindingProblem(SearchProblem):
    def __init__(self, world, start, goal, costs):
        super().__init__(start, goal, costs)
        self.world = world
        self.costs = costs


    def getSuccessors(self, state):
        successors = []
        for dx, dy in DIRECTIONS:
            nx, ny = state[0] + dx, state[1] + dy
            if 0 <= nx < self.world.x_lim and 0 <= ny < self.world.y_lim:
                if (nx, ny) not in self.world.walls:
                    terrain = self.world.get_terrain(nx, ny)
                    cost = self.costs.get(terrain, 1)
                    successors.append(((nx, ny), cost))
        return successors

    def isGoal(self, state):
        return state == self.goal

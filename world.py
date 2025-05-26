class World:
    def __init__(self, x_lim: int, y_lim: int, walls: set, terrain: dict):
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.walls = walls  # set di tuple (x, y)
        self.terrain = terrain  # dict {(x, y): tipo_terreno}

    def get_terrain(self, x, y):
        return self.terrain.get((x, y), None)

    def __str__(self):
        ret = ""
        for x in range(0, self.x_lim):
            for y in range(0, self.y_lim):
                if (x, y) in self.walls:
                    ret += "%"
                else:
                    ret += " "
            ret += "\n"
        return ret

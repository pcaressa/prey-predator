"""
    Agent based plants vs. herbivores vs. carnivores simulation
    Copyright (C) 2023 by Paolo Caressa

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    The code is maintained in the repository:
    <https://github.com/pcaressa/licenses/predator_prey>
    
    See the enclosed README.md for explanations.
"""

from random import choice, randrange, shuffle, uniform
import tkinter as tk

# Constants denoting something inside a territory cell
# They are used to fill the "kind" attribute of all
# classes, so one can easily check what is on a certain
# territory cell
NIL = 0.0
PLANT = 1.0
HERBIVORE = 2.0
CARNIVORE = 3.0


class Territory:

    def __init__(self, N, M):
        self.N = N
        self.M = M
        self.CELL_WIDTH = 1024//max(N, M)
        self.grid = [[Nil() for i in range(M)] for j in range(N)]

    def __str__(self):
        t = "-"*self.M + "\n"
        for x in range(self.N):
            for y in range(self.M):
                k = self.grid[x][y].kind
                if k == NIL:
                    t += " "
                elif k == PLANT:
                    t += "P" # "\U0001F33F"
                elif k == HERBIVORE:
                    t += "H" # "\U0001F407"
                elif k == CARNIVORE:
                    t += "C" # "\U0001F98A"
            t += "\n"
        t += "-"*self.M + "\n"
        return t

    def get(self, x, y):
        """Retrieve the object located at the x,y coordinates
        in the territory and returns it."""
        return self.grid[x][y]

    def put(self, x, y, obj):
        """Insert the object obj into the territory at the
        given coordinates: the previous object is discarded."""
        self.grid[x][y] = obj

    def find_near(self, x, y, kind):
        """Returns the list coordinates of cells around (x,y)
        where there is an object of the given kind,
        as a list [(x1,y1),...,(xn,ym)]"""
        neighbors = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i == 0 and j == 0:
                    continue
                if 0 <= x+i < self.N and 0 <= y+j < self.M and self.grid[x+i][y+j].kind == kind:
                    neighbors.append((x+i,y+j))
        return neighbors

    def find_empty(self, x1=0, y1=0, x2=-1, y2=-1):
        """Finds an empty cell in the territory in the rectangle
        with left upper coordinate (x0,y0) and right lower
        coordinate (x1,y1)"""
        if x2 == -1: x2 = self.N
        if y2 == -1: y2 = self.M
        for i in range(self.N*self.M):
            x = randrange(x1, x2)
            y = randrange(y1, y2)
            if self.get(x, y).kind == NIL:
                return x, y
        raise "NO MORE SPACE FOR ANIMALS OR PLANTS!!!"

    def display(self, canvas):
        for y in range(self.N):
            for x in range(self.M):
                # Coordinates of rectangle to print
                x0, y0 = self.CELL_WIDTH*x, self.CELL_WIDTH*y
                x1, y1 = x0 + self.CELL_WIDTH, y0 + self.CELL_WIDTH
                if self.grid[y][x].kind == PLANT:
                    canvas.create_rectangle((x0, y0), (x1, y1),
                                            fill="green", outline="green")
                if self.grid[y][x].kind == HERBIVORE:
                    canvas.create_rectangle((x0, y0), (x1, y1),
                                            fill="grey", outline="grey")
                if self.grid[y][x].kind == CARNIVORE:
                    canvas.create_rectangle((x0, y0), (x1, y1),
                                            fill="red", outline="red")


class Nil:
    """This class is needed instead of None since we want it
    to have a `kind` attribute, to make code simpler."""
    kind = NIL


class Plant:
    kind = PLANT
    threshold = 0   # Number of plants around an empty place needed to generate another plant


class Animal:

    @classmethod
    def reproduce(cls, territory, x, y):
        return cls(territory, x, y)
    
    def __init__(self, territory, x, y):
        self.territory = territory
        self.x = x
        self.y = y
        self.territory.put(x, y, self)

    def age(self):
        self.energy -= 1
        self.timespan -= 1

    def can_mate(self, month, spawn):
        if self.energy >= self.threshold and \
            (month%12) >= self.mate_start and \
            (month%12) <= self.mate_end:
            # look for a cell for the cub and choose it
            # randomly among the available ones
            n = self.territory.find_near(self.x, self.y, NIL)
            if len(n) > 0:
                x1, y1 = choice(n)
                cub = self.reproduce(self.territory, x1,y1)
                spawn.append(cub)
                return True
        return False

    def is_dead(self):
        if self.energy < 0 or self.timespan < 0:
            self.energy = -1
            self.territory.put(self.x, self.y, Nil())
            return True
        return False

    def move_random(self):
        """An animal may move on an empty cell or on a cell where
        there is a plant."""
        n = self.territory.find_near(self.x, self.y, NIL)
        if len(n) > 0:
            x, y = choice(n)
            self.move_to(x, y)
        else:
            n = self.territory.find_near(self.x, self.y, PLANT)
            if len(n) > 0:
                x, y = choice(n)
                self.move_to(x, y)

    def move_to(self, x, y):
        self.territory.put(self.x, self.y, Nil())
        self.x = x
        self.y = y
        self.territory.put(x, y, self)


class Herbivore(Animal):

    kind = HERBIVORE

    def __init__(self, territory, x, y):
        super().__init__(territory, x,y)
        self.energy = 8
        self.timespan = (8 + randrange(-1,2))*12
        self.mate_start = 1
        self.mate_end = 4
        self.threshold = 3    # minimum amount of energy to spawn

    def __repr__(self):
        return f"Herbivore: x={self.x}, y={self.y}; energy={self.energy}; timespan={self.timespan}; start mate={self.mate_start}, end mate={self.mate_end}; threshold={self.threshold}"

    def can_eat(self):
        n = self.territory.find_near(self.x, self.y, PLANT)
        if len(n) > 0:
            # choose a plant the herbivore shall eat
            x1, y1 = choice(n)
            self.move_to(x1, y1)
            self.energy += 1
            return True
        return False
    

class Carnivore(Animal):

    kind = CARNIVORE

    def __init__(self, territory, x, y):
        super().__init__(territory, x,y)
        self.energy = 12
        self.timespan = (12 + randrange(-1,2))*12
        self.mate_start = 6
        self.mate_end = 11
        self.threshold = 6    # minimum amount of energy to spawn

    def __repr__(self):
        return f"Carnivore: x={self.x}, y={self.y}; energy={self.energy}; timespan={self.timespan}; start mate={self.mate_start}, end mate={self.mate_end}; threshold={self.threshold}"

    def can_eat(self):
        n = self.territory.find_near(self.x, self.y, HERBIVORE)
        # At least two herbivores should be at hand
        if len(n) > 1:
            # choose an herbivore the carnivore shall eat
            x1, y1 = choice(n)
            self.territory.get(x1, y1).energy = -1  # eaten animal dies
            self.move_to(x1, y1)
            self.energy += 1
            return True
        return False

    def move_random(self):
        """A carnivore moves more than a herbivore."""
        super().move_random()
        super().move_random()
        super().move_random()
        super().move_random()


def simulation(N: int,
               M: int,
               MAX_MONTH: int,
               PLANT_RATIO: float,
               HERBIVORE_RATIO: float,
               CARNIVORE_RATIO: float):
    CELL_WIDTH = 1024//max(N, M)

    n_plants = int(N*M * PLANT_RATIO)
    n_herbivores = int(N*M * HERBIVORE_RATIO)
    n_carnivores = int(N*M * CARNIVORE_RATIO)

    # Set up the territory
    territory = Territory(N, M)

    # Set up living beings: plants are elements of the territory
    for i in range(n_plants):
        x, y = territory.find_empty()
        territory.put(x, y, Plant())

    # Animals are collected lists and referenced in the territory
    herbivores = []
    for i in range(n_herbivores):
        # Herbivores are located at North
        x, y = territory.find_empty(0, 0, N//2, M)
        animal = Herbivore(territory, x, y)
        herbivores.append(animal)

    carnivores = []
    for i in range(n_carnivores):
        # Carnivores are located at South
        x, y = territory.find_empty(N//2+1, 0, N, M)
        animal = Carnivore(territory, x, y)
        carnivores.append(animal)

    print("Simulation with:")
    print(f"\t{N*M} territory area")
    print(f"\t{n_plants} plants")
    print(f"\t{n_herbivores} herbivores")
    print(f"\t{n_carnivores} carnivores")
    print(f"Timespan: {MAX_MONTH/12} years")
    print()

    csvstring = "Time; Plants; Herbivores; Carnivores\n"

    root = tk.Tk()
    root.geometry(f"{CELL_WIDTH*M}x{CELL_WIDTH*N}")
    root.title("Predator-prey simulation")
    canvas = tk.Canvas(root, width = CELL_WIDTH*M, height = CELL_WIDTH*N, bg = "white")
    canvas.pack(anchor = tk.CENTER, expand = True)

    for month in range(MAX_MONTH):

        # Information about this month
        n_plants = sum([sum([int(territory.get(x, y).kind == PLANT) for y in range(M)]) for x in range(N)])
        n_herbivores = len(herbivores)
        n_carnivores = len(carnivores)

        csvstring += f"{month}; {n_plants}; {n_herbivores}; {n_carnivores}\n"
        print(f"{month}; {n_plants}; {n_herbivores}; {n_carnivores}")
        if M*N < 4096:
            print(territory)

        canvas.delete("all")
        territory.display(canvas)
        root.update()

        # Stopping conditions
        if n_plants == 0:
            print("No more plants!")
            break
        if n_herbivores == 0:
            print("No more herbivores!")
            break
        if n_carnivores == 0:
            print("No more carnivores!")
            break

        # Plants grow: randomly check for void cells and, if
        # there are more than 2 plants around them, put a plant
        # in them, too
        for i in range(N*M):
            x = randrange(0, N)
            y = randrange(0, M)
            if territory.get(x, y).kind == NIL:
                # Counts the number of neighbourhoods: if more than
                # Plant.threshold plants are around the empty place
                # then here a plant shall be born
                if len(territory.find_near(x, y, PLANT)) > Plant.threshold:
                    territory.put(x, y, Plant())

        # Animals do things
        for species in [herbivores, carnivores]:
            shuffle(species)
            spawn = []
            for animal in species:
                animal.age()
                if not (animal.is_dead() \
                    or animal.can_mate(month, spawn) \
                        or animal.can_eat()):
                    animal.move_random()
            species += spawn

        # Dispose corpses: use explicitly indexed loop since the
        # lists are changed inside the loop!
        for species in [herbivores, carnivores]:
            i = 0
            while i < len(species):
                if species[i].energy < 0:
                    del species[i]
                else:
                    i += 1

    with open("lvts.csv", "w") as f:
        f.write(str(csvstring))
    print("Time series dumped on file lvts.csv")


simulation(N = 100,
           M = 100,
           MAX_MONTH = 512,
           PLANT_RATIO = 0.5,
           HERBIVORE_RATIO = 0.03,
           CARNIVORE_RATIO = 0.01)


# A sample implementation of an agent-based model

### Paolo Caressa

This repository contains a script which implements, in a non idiomatic and plain lean-and-mean Python 3 (no Numpy, no Pandas, no Matplotlib etc.), an agent based model for a simple ecological predator-prey system.

It is essentially borrowed from Gary W Flake *The Computational Beauty of the Nature*, where the idea for the set up and the algorithms in their essence are described.

This is not serious research, just a toy but I hope it could be useful to someone.

The simulation happens in a *territory*, thus a 2D grid whose
cells can contain nothing, plants, a herbivore or a carnivore.
    
Each cell is addressed by a pair of coordinates (x,y) that
are integers running as x=0,...,N-1 and y=0,...,M-1.

Two cells are *near* if |x1-x2| <= 1 and |y1-y2| <= 1
    
Three kinds of agents share the territory:

- Plants
- Herbivores
- Carnivores
        
Plants are randomly spread on the territory according to
a certain percentage PLANT_RATIO, and they breed and spread
on the territory, just by contact with empty cells that they
populate (a certain `threshold`, static attribute of the `Plant` class, determines how many plants are needed around an empty spot to let a plant to be born therein).
    
It is assumed that plants
do not die, unless a herbivore eats them, and they are just characterized by occupying a cell
or not.
    
Animals, instead, can die, mate, eat and move, so they
need to be singly represented as agents. Common features
to all animals are:

- (x,y) coordinates of animal position in the territory.
- energy, a number which decreases at each simulation
    cycle and that is increased when the animal eats
    but decreased when the herbivore breeds.
- timespan, the number of expected months of living.
- threshold, the minimum amount of energy needed to breed.
- mating season limits, a lower and upper month of the
    year in which the animal can mate.

At each simulation
cycle each animal, in random order, does the following:

- increase its age and decrease its energy (and die if it becomes too old or too weak);
- if its energy is sufficient and the current month is one its mating season then it mates, if there's an empty space around it. On mating energy decreases.
- else if eat, is there's food at hand.
- else move around.

Herbivores eat plants if there's one plant around them and move to the plant location. Carnivores eat herbivores if there's one around them and move to the herbivore location: the herbivore dies.

At start herbivores are located at north, carnivores at south: once can change that and make each species to be located in a rectangle inside the territory at start.

Also, at start the number of herbivores and carnivores can be changed on changing the HERBIVORE_RATIO and CARNIVORE_RATIO parameters in the `simulation` function.

Data collected during the simulation are eventually saved on a csv file `prey_predator_simulation.csv`.

A simulation cycle represents a month.

### Implementation details (largely TODO)

The code is simple minded, not optimized but hopefully easily understandable and portable.

Since object orientation was invented to program simulations I used classes: two classes are just attribute containers, `Nil` and `Plant` which represent an empty spot in the territory and a plant. The `Territory` class essentially maintains the grid where living beings take place, and also has methods to display its status: in particular, by using the `Tkinker` built-in class, a simple animation is performed during the simulation.

The `Animal` class abstract features of all species included in the simulation, while the `Carnivore` and `Herbivore` subclasses model obviously carnivores and herbivores, implementing virtual functions when needed.
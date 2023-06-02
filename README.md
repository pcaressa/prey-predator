# A sample implementation of an agent-based model

### Paolo Caressa

This repository contains a script which implements, in a non idiomatic and plain lean-and-mean Python 3 (no Numpy, no Pandas etc.), an agent based model for a simple ecological predator-prey system.

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
        
Plants are randomly sparsed on the territory according to
a certain percentage PLANT_RATIO, and they breed and spread
on the territory, just by contact with empty cells that they
populate.
    
Actually, plants do not need to be represented by agents
since they are part of the territory. It is assumed that plants
do not die and they are just characterized by occupying a cell
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
    
Herbivores are randomly sparsed on the territory according
to a certain percentage HERBIVORE_RATIO. At each simulation
cycle each herbivore, in random order, can do the following:

    IF its energy or its timespan is <= 0 THEN die.
    ELIF its energy >= its threshold and the month is one of
        the mating season and there is an empty cell near
        the cell occupied by the animal THEN a new animal
        is born in the empty cell. The parent energy
        decreases.
    ELIF there is a plant in a cell near to its cell
        THEN move to that cell, eat the plant and increase
        its energy.
    ELSE try to move on a near cell if empty.

Carnivores are randomly sparsed on the territory according
to a certain percentage CARNIVORE_RATIO. At each simulation
cycle each carnivore, in random order, can do the following:
    
    IF its energy or its timespan is <= 0 THEN die.
    ELIF its energy >= its threshold and the month is one of
        the mating season and there is an empty cell near
        the cell occupied by the animal THEN a new animal
        is born in the empty cell.
    ELIF there is a herbivore in a cell near to its cell
        THEN move to that cell and eat the herbovore, which
        dies.
    ELSE try to move on a near cell if empty or contains
        a plant.

A simulation cycle represents a month.

## Implementation

The code is simple minded, not optimized but hopefully easily understandable and portable.

Since object orientation was invented to program simulations it is worth to use classes.

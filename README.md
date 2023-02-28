# Ludobots
3d bot simulations

Generating a random assortment of body parts with different color for sensors and links. 

![Bot Creation and mutation logic](https://i.imgur.com/DcCmU4V.jpg)

This is a tool that generates random creatures with the aim of moving in a particular direction (x direction). The creatures are made up of a variable number of links, and assigned sensors with some probablity. with a set number of links we generate a body and mutate it based on their movement in x direction. Fitness works on improving the x direction.

Fitness curves for 5 random seeds for population size 5 and generations 100.

![Fitness curves](https://raw.githubusercontent.com/AnshulH/Ludobots/assign8/fitcurves.jpg)

## Citation

Code influenced from two sources:
- Pyrosim package: https://github.com/jbongard/pyrosim
- r/ludobots - https://www.reddit.com/r/ludobots/ 

## How to run
```
python search.py
```
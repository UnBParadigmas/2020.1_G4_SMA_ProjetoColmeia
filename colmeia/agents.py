from mesa import Agent
from colmeia.random_walk import RandomWalker
from colmeia.schedule import RandomActivationByBreed
from random import random

class WorkerBee(RandomWalker):
   

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
       
        self.random_move()
        living = True

        if self.model.honey:
           
            self.energy -= 1

            
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            grass_patch = [obj for obj in this_cell if isinstance(obj, HoneyComb)][0]
            if grass_patch.fully_grown:
                self.energy += self.model.bee_gain_frrom_food
                grass_patch.fully_grown = False

           
            if self.energy < 0:
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)
                living = False

        if living and self.random.random() < self.model.bee_reproduce:
           
            if self.model.honey:
                self.energy /= 2
            lamb = WorkerBee(
                self.model.next_id(), self.pos, self.model, self.moore, self.energy
            )
            self.model.grid.place_agent(lamb, self.pos)
            self.model.schedule.add(lamb)


class Death(RandomWalker):
   

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        self.energy -= 1

      
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        bees = [obj for obj in this_cell if isinstance(obj, WorkerBee)]
        if len(bees) > 0:
            bee_to_kil = self.random.choice(bees)
            self.energy += self.model.death_gain_from_food

            
            self.model.grid._remove_agent(self.pos, bee_to_kil)
            self.model.schedule.remove(bee_to_kil)

        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.death_reproduce:
                self.energy /= 2
                cub = Death(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy
                )
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)


class HoneyComb(Agent):
   

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
       
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
               
                self.fully_grown = True
                self.countdown = self.model.honey_regrowth_time
            else:
                self.countdown -= 1

# class QueenBee(Agent):

#     def __init__(self, unique_id, model):

#         super().__init__(unique_id, model)
#         self.queenbee = random(0.04, 0.09)
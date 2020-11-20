
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from colmeia.agents import WorkerBee, Death, HoneyComb
from colmeia.schedule import RandomActivationByBreed


class BeeHoney(Model):

    height = 20
    width = 20

    initial_bees = 100
    initial_deaths = 50

    bee_reproduce = 0.04
    death_reproduce = 0.05

    death_gain_from_food = 20

    honey = True
    honey_regrowth_time = 30
    bee_gain_frrom_food = 4

    verbose = True  # Print-monitoring

    description = (
        "A model for simulating death and bees (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        height=20,
        width=20,
        initial_bees=100,
        initial_deaths=50,
        bee_reproduce=0.04,
        death_reproduce=0.05,
        death_gain_from_food=20,
        honey=True,
        honey_regrowth_time=30,
        bee_gain_frrom_food=4,
    ):
        
        super().__init__()
        
        self.height = height
        self.width = width
        self.initial_bees = initial_bees
        self.initial_deaths = initial_deaths
        self.bee_reproduce = bee_reproduce
        self.death_reproduce = death_reproduce
        self.death_gain_from_food = death_gain_from_food
        self.honey = honey
        self.honey_regrowth_time =honey_regrowth_time
        self.bee_gain_frrom_food = bee_gain_frrom_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Deaths": lambda m: m.schedule.get_breed_count(Death),
                "Operarias": lambda m: m.schedule.get_breed_count(WorkerBee),
            }
        )

        
        for i in range(self.initial_bees):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.bee_gain_frrom_food)
            bees = WorkerBee(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(bees, (x, y))
            self.schedule.add(bees)

        
        for i in range(self.initial_deaths):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.death_gain_from_food)
            death = Death(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(death, (x, y))
            self.schedule.add(death)

        
        if self.honey:
            for agent, x, y in self.grid.coord_iter():

                fully_grown = self.random.choice([True, False])

                if fully_grown:
                    countdown = self.honey_regrowth_time
                else:
                    countdown = self.random.randrange(
                        self.honey_regrowth_time)

                patch = HoneyComb(self.next_id(), (x, y),
                                   self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_breed_count(Death),
                    self.schedule.get_breed_count(WorkerBee),
                ]
            )

    def run_model(self, step_count=200):

        if self.verbose:
            print("Initial number deaths: ",
                  self.schedule.get_breed_count(Death))
            print("Initial number bees: ", self.schedule.get_breed_count(WorkerBee))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print("Final number deaths: ", self.schedule.get_breed_count(Death))
            print("Final number bees: ", self.schedule.get_breed_count(WorkerBee))

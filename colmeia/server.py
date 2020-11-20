from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from colmeia.agents import Death, WorkerBee, HoneyComb
from colmeia.model import BeeHoney


def bee_honey_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is WorkerBee:
        portrayal["Shape"] = "colmeia/resources/bee.png"

        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Death:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = ["#000", "#0053", "#dddd"]
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)

        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is HoneyComb:
        if agent.fully_grown:
            portrayal["Shape"] = "colmeia/resources/honey.png"
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(bee_honey_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Operarias", "Color": "#fcbe1f"},{"Label": "Deaths", "Color": "#b1b1c8"},
        ]
)

model_params = {
    "honey_regrowth_time": UserSettableParameter(
        "slider", "Honey Regrowth Time", 20, 1, 50
    ),
    "initial_bees": UserSettableParameter(
        "slider", "Initial WorkerBee Population", 100, 10, 300
    ),
    "bee_reproduce": UserSettableParameter(
        "slider", "WorkerBee Reproduction Rate", 0.04, 0.01, 1.0, 0.01
    ),
    "initial_deaths": UserSettableParameter(
        "slider", "Initial Death Population", 50, 10, 300
    ),
    "death_reproduce": UserSettableParameter(
        "slider",
        "Death Reproduction Rate",
        0.05,
        0.01,
        1.0,
        0.01,
        description="The rate at which death agents reproduce.",
    ),
    "death_gain_from_food": UserSettableParameter(
        "slider", "Death Gain From Food Rate", 20, 1, 50
    ),
    "bee_gain_frrom_food": UserSettableParameter(
        "slider", "WorkerBee Gain From Food", 4, 1, 10
    ),
}

server = ModularServer(
    BeeHoney, [canvas_element,
                chart_element], "Death WorkerBee Predation", model_params
)
server.port = 8521

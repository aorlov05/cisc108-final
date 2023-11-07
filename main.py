from dataclasses import dataclass
from designer import *


@dataclass
class World:
    ground: DesignerObject


def create_world() -> World:
    """
    Create a new world with green grass ground

    Returns:
        A new designer world instance
    """
    ground = Rectangle('green', get_width(), 100, 0, get_height() - 100, anchor='topleft')
    return World(ground)


when('starting', create_world)
start()

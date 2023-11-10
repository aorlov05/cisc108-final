from dataclasses import dataclass
from designer import *
import random
from random import randomint

# Constants which represent the ground height and position
HEIGHT_OF_GROUND = 100
TOP_OF_GROUND_Y = get_height() - HEIGHT_OF_GROUND


@dataclass
class Player:
    cannon: DesignerObject
    wheel: DesignerObject


@dataclass
class World:
    ground: DesignerObject
    player: Player
    moles: list[DesignerObject]


def create_world() -> World:
    """
    Creates a new world with the initial state of ground and the player

    Returns:
        A new designer world instance
    """
    ground = Rectangle('green', get_width(), HEIGHT_OF_GROUND, 0,
                       TOP_OF_GROUND_Y, anchor='topleft')
    player = create_player()
    return World(ground, player)


def create_player() -> Player:
    """
    Creates a new player object which consists of a cannon and a wheel
    and sets it on top of the ground.

    Returns:
        A player object representing the user
    """
    cannon = image("./cannon.png", anchor="midtop")
    wheel = image("./wheel.png", anchor="midbottom")
    wheel.y = TOP_OF_GROUND_Y
    cannon.y = wheel.y - cannon.height
    return Player(cannon, wheel)


def create_moles() -> DesignerObject:
    moles = emoji("🐀")
    set_x = (moles, random_x)
    set_y = (moles, random_y)
    return World(moles)

def make_moles(world: World):
    not_too_many_moles = len(world.moles) < 2
    random_chance = randint(1, 100) == 2
    if not_too_many_moles and random_chance:
        world.moles.append(create_moles())

def moles_dissapear(world:World):
    kept = []
    for mole in world.moles:
        if "moles survived for longer then 10 seconds?":
            kept.append(mole)
        else:
            destroy(mole)
    world.moles = kept

when('starting', create_world)
when("updating", make_moles)
when("updating", moles_dissapear)
start()

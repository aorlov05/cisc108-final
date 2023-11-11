from dataclasses import dataclass
from designer import *
from random import randint


# Constants which represent the ground height and position
HEIGHT_OF_GROUND = 100
TOP_OF_GROUND_Y = get_height() - HEIGHT_OF_GROUND


@dataclass
class Player:
    cannon: DesignerObject
    wheel: DesignerObject
    left: bool
    right: bool


@dataclass
class World:
    ground: DesignerObject
    player: Player
    moles: list[DesignerObject]
    lives_count: int
    lives: DesignerObject
    ammo: list[DesignerObject]


def create_world() -> World:
    """
    Creates a new world with the initial state of ground and the player

    Returns:
        A new designer world instance
    """
    ground = Rectangle('green', get_width(), HEIGHT_OF_GROUND, 0,
                       TOP_OF_GROUND_Y, anchor='topleft')
    player = create_player()
    lives = create_lives()
    return World(ground, player, [], 3, lives, [])


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
    return Player(cannon, wheel, False, False)


def move_player(player: Player, pixels: int):
    """
    Moves the player the specified number of pixels

    Args:
        player (Player): The player object
        pixels (int): The number of pixels to move the player
    """
    player.cannon.x += pixels
    player.wheel.x += pixels


def update_player_position(world: World):
    """
    If the player is moving left, move the player position and
    rotate the player wheel towards the corresponding direction

    Args:
        world (World): The world instance
    """
    if world.player.left:
        move_player(world.player, -5)
        turn_left(world.player.wheel, 5)
    elif world.player.right:
        move_player(world.player, 5)
        turn_right(world.player.wheel, 5)


def on_key_press_move_player(world: World, key: str):
    """
    Moves the player left when holding a, moves them right when holding d

    Args:
        world (World): The world instance
        key (str): The key the user presses
    """
    if key == "a":
        world.player.left = True
    elif key == "d":
        world.player.right = True


def on_key_release_stop_player(world: World, key: str):
    """
    Stops moving the player left when holding a, moves them right when holding d

    Args:
        world (World): The world instance
        key (str): The key the user presses
    """
    if key == "a":
        world.player.left = False
    elif key == "d":
        world.player.right = False


def create_moles() -> DesignerObject:
    """
    Makes the moles that the player is trying to shoot appear randomly

    Returns:
        A picture (emoji) of a mole that is the players target
    """
    new_mole = emoji("🐀")
    new_mole.x = randint(1, get_width())
    new_mole.y = randint(1, TOP_OF_GROUND_Y)
    return new_mole


def make_moles(world: World):
    """
    This determines when a new mole should appear on screen, so they aren't constantly appearing
    Args:
        world (World): The world instance
    """
    not_too_many_moles = len(world.moles) < 2
    random_chance = randint(1, 100) == 2
    if not_too_many_moles and random_chance:
        world.moles.append(create_moles())


def destroy_moles(world: World):
    """
    Gets rid of the moles after an amount of time if they are not shot by the player
    Args:
        world (World): The world instance
    """
    pass


def create_lives() -> DesignerObject:
    """
        the user starts with 3 lives represented by the three heart emojis
        Returns:
            three hearts representing the lives
        """
    lives = text("red", "Lives: 3", 40, anchor="topleft")
    lives.x = 5  # Some margin so that the text doesn't hug the corner
    lives.y = 5
    return lives

def stop_player(world: World):
    """
    Stops the player from going beyond the bounds of the screen by using the boundaries of the world
    Args:
        world (World): the world instance
    """
    if world.player.cannon.x > get_width():
        world.player.right = False
    elif world.player.cannon.x < 0:
        world.player.left = False


def update_lives(world: World):
    """
    the user starts with 3 lives represented by the three heart emojis
    Returns:
        three hearts representing the lives
    """
    world.lives.text = "Lives: " + str(world.lives_count)

def create_ammo() -> DesignerObject:
    """
    Makes the ammo that the player is shooting appear randomly on the ground

    Returns:
        A picture (emoji) of ammo that the  player picks up
    """
    new_ammo = image("https://www.clker.com//cliparts/K/Z/z/u/k/7/cannon-balls-hi.png", anchor = "midbottom")
    new_ammo.scale_x = .1
    new_ammo.scale_y = .1
    new_ammo.x = randint(1, get_width())
    new_ammo.y = TOP_OF_GROUND_Y
    return new_ammo

def make_ammo(world: World):
    """
    This determines when more ammo should appear on screen, so they aren't constantly appearing
    Args:
        world (World): The world instance
    """
    not_too_much_ammo = len(world.ammo) < 2
    random_chance = randint(1, 100) == 2
    if not_too_much_ammo and random_chance:
        world.ammo.append(create_ammo())

when("updating", make_moles)
when("updating", make_ammo)
when("updating", destroy_moles)
when('starting', create_world)
when('typing', on_key_press_move_player)
when('done typing', on_key_release_stop_player)
when('updating', update_player_position)
when("updating", stop_player)
when("updating", update_lives)
start()
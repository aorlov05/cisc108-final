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
    rotating_left: bool
    rotating_right: bool


@dataclass
class Mole:
    mole_img: DesignerObject
    is_mini: bool
    is_rabbit: bool


@dataclass
class World:
    ground: DesignerObject
    player: Player
    moles: list[Mole]
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
    return Player(cannon, wheel, False, False, False, False)


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


def create_mole(is_mini: bool, is_rabbit: bool) -> DesignerObject:
    """
    Makes the moles that the player is trying to shoot appear randomly

    Returns:
        A picture (emoji) of a mole that is the players target
    """
    if is_rabbit:
        new_mole = emoji("🐇")
    else:
        new_mole = emoji("🐀")
    new_mole.x = randint(1, get_width())
    new_mole.y = randint(1, TOP_OF_GROUND_Y)
    if is_mini:
        new_mole.scale_x = 0.5
        new_mole.scale_y = 0.5
    return new_mole


def make_moles(world: World):
    """
    This determines when a new mole should appear on screen, so they aren't constantly appearing

    Args:
        world (World): The world instance
    """
    not_too_many_moles = len(world.moles) < 2
    random_spawn_chance = randint(1, 100) == 2
    if not_too_many_moles and random_spawn_chance:
        # Adds a 10% chance for the mole to be small, or 10% for it to be a rabbit
        random_type_chance = randint(0, 10)
        is_mini = False
        is_rabbit = False
        if random_type_chance == 1:
            is_mini = True
        elif random_type_chance == 2:
            is_rabbit = True
        mole_img = create_mole(is_mini, is_rabbit)
        new_mole = Mole(mole_img, is_mini, is_rabbit)
        world.moles.append(new_mole)


def destroy_moles(world: World):
    """
    Gets rid of the moles after an amount of time if they are not shot by the player

    Args:
        world (World): The world instance
    """
    pass


def create_lives() -> DesignerObject:
    """
    The user starts with 3 lives represented by the three heart emojis

    Returns:
        DesignerObject: Text which displays how many lives the user has
    """
    lives = text("red", "Lives: 3", 40, anchor="topleft")
    lives.x = 5  # Some margin so that the text doesn't hug the corner
    lives.y = 5
    return lives


def set_player_screen_bounds(world: World):
    """
    Stops the player from going beyond the bounds of the screen by using the boundaries of the world

    Args:
        world (World): The world instance
    """
    if world.player.cannon.x > get_width():
        world.player.right = False
    elif world.player.cannon.x < 0:
        world.player.left = False


def update_lives(world: World):
    """
    Constantly sets the lives text equal to the user's number of lives

    Args:
        world (World): The world instance
    """
    world.lives.text = "Lives: " + str(world.lives_count)


def create_ammo() -> DesignerObject:
    """
    Makes the ammo that the player is shooting appear randomly on the ground

    Returns:
        A picture (emoji) of ammo that the player picks up
    """
    new_ammo = image("https://www.clker.com//cliparts/K/Z/z/u/k/7/cannon-balls-hi.png", anchor="midbottom")
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


def on_key_press_rotate_player(world: World, key: str):
    """
    Rotate the cannon in the respective direction when pressing the left or right arrow keys

    Args:
        world (World): The world instance
        key (str): The key the player pressed
    """
    if key == "left":
        world.player.rotating_left = True
    elif key == "right":
        world.player.rotating_right = True


def on_key_release_stop_rotate(world: World, key: str):
    """
    Stops rotating the cannon when the user lets go of the respective left or right arrow keys

    Args:
        world (World): The world instance
        key (str): The key the player pressed
    """
    if key == "left":
        world.player.rotating_left = False
    elif key == "right":
        world.player.rotating_right = False


def update_player_rotation(world: World):
    """
    While the player is holding the left or right arrow keys, rotate the cannon in the respective direction

    Args:
        world (World): The world instance
    """
    if world.player.rotating_left:
        turn_left(world.player.cannon, 5)
    elif world.player.rotating_right:
        turn_right(world.player.cannon, 5)

def collect_ammo(world: World, player: Player):
    picked_up_ammo = []
    for ball in world.ammo:
        if colliding(ball, player):
            picked_up_ammo.append(ball)

# Creates the world
when('starting', create_world)
# Handles mole spawning
when('updating', make_moles)
when('updating', make_ammo)
when('updating', destroy_moles)
# Updates player position on holding A or D
when('typing', on_key_press_move_player)
when('done typing', on_key_release_stop_player)
when('updating', update_player_position)
when('updating', set_player_screen_bounds)
# Updates the number of player lives
when('updating', update_lives)
# Allows player to rotate on arrow key hold
when('typing', on_key_press_rotate_player)
when('done typing', on_key_release_stop_rotate)
when('updating', update_player_rotation)
when('updating', collect_ammo)
start()

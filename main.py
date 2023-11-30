import math
from dataclasses import dataclass
from designer import *
from random import randint


# Constants which represent the ground height and position
HEIGHT_OF_GROUND = 100
TOP_OF_GROUND_Y = get_height() - HEIGHT_OF_GROUND
# Represents the highest number of degrees the cannon can rotate before stopping
MAX_CANNON_ANGLE = 85
CANNONBALL_SPEED = 5
MAX_AMMO = 10


@dataclass
class Player:
    cannon: DesignerObject
    wheel: DesignerObject
    left: bool
    right: bool
    rotating_left: bool
    rotating_right: bool
    moles_hit: int
    moles_hit_in_current_level: int
    ammo_count: int


@dataclass
class Mole:
    mole_img: DesignerObject
    is_mini: bool
    is_rabbit: bool


@dataclass
class Cannonball:
    ball: DesignerObject
    angle: int
    is_from_player: bool


@dataclass
class World:
    ground: DesignerObject
    player: Player
    moles: list[Mole]
    lives_count: int
    lives: DesignerObject
    ammo: list[DesignerObject]
    cannonballs: list[Cannonball]
    cannon_balls: DesignerObject
    level: int
    levels: DesignerObject


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
    cannon_balls = count_ammo()
    levels = count_level()
    return World(ground, player, [], 3, lives, [], [], cannon_balls, 1, levels)


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
    return Player(cannon, wheel, False, False, False, False, 0, 0, 0)


def get_half_cannon_width(world: World):
    """
    Returns half the width of the cannon to set its bounds

    Args:
        world (World): The world instance
    """
    return world.player.cannon.width // 2


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
    if key == "a" and world.player.cannon.x > get_half_cannon_width(world):
        world.player.left = True
    elif key == "d" and world.player.cannon.x < get_width() - get_half_cannon_width(world):
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


def create_mole(world: World, is_mini: bool, is_rabbit: bool) -> DesignerObject:
    """
    Makes the moles that the player is trying to shoot appear randomly

    Returns:
        A picture (emoji) of a mole that is the players target
    """
    if is_rabbit:
        new_mole = image("./rabbit.png")
    else:
        new_mole = image("./mouse.png")
    new_mole.x = randint(1, get_width())
    new_mole.y = randint(1, TOP_OF_GROUND_Y - world.player.cannon.height)
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
    not_too_many_moles = len(world.moles) <= world.level
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
        mole_img = create_mole(world, is_mini, is_rabbit)
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
    if world.player.cannon.x > get_width() - get_half_cannon_width(world):
        world.player.right = False
    elif world.player.cannon.x < get_half_cannon_width(world):
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
    new_ammo = image("ammo.png", anchor="midbottom")
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
    not_too_much_ammo = len(world.ammo) <= world.level
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
    player = world.player
    if key == "left" and player.cannon.angle < MAX_CANNON_ANGLE:
        player.rotating_left = True
    elif key == "right" and player.cannon.angle > -MAX_CANNON_ANGLE:
        player.rotating_right = True


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
    If the cannon is rotated too far right or left, stop it so that it doesn't face the ground

    Args:
        world (World): The world instance
    """
    player = world.player
    cannon = player.cannon
    if player.rotating_left:
        if cannon.angle >= MAX_CANNON_ANGLE:  # Stop cannon from turning towards the ground
            player.rotating_left = False
        turn_left(cannon, 5)
    elif player.rotating_right:
        if cannon.angle <= -MAX_CANNON_ANGLE:
            player.rotating_right = False
        turn_right(cannon, 5)

def count_ammo() -> DesignerObject:
    """
        The user starts with no ammo represented by the number at the top of the screen

        Returns:
            DesignerObject: Text which displays how much ammo the user has
        """
    cannon_balls = text("black", "Ammo: ", 40, anchor="topright")
    cannon_balls.x = 750  # Some margin so that the text doesn't hug the corner
    cannon_balls.y = 5
    return cannon_balls

def update_ammo(world: World):
    """
    Constantly sets the ammo text equal to the user's amount of ammo

    Args:
        world (World): The world instance
    """
    player = world.player
    for ball in world.ammo:
        if colliding(ball, player.cannon):
            if player.ammo_count < MAX_AMMO:
                player.ammo_count += 1
            else:
                player.ammo_count += 0
    world.cannon_balls.text = "Ammo: " + str(player.ammo_count)

def update_cannonball_position(world: World):
    """
    Constantly updates the cannonball position to move in the direction
    that the player cannon initially shot in
    https://stackoverflow.com/a/46697552

    Args:
        world (World): The world instance to get the cannonballs from
    """
    for cannonball in world.cannonballs:
        corrected_angle = -cannonball.angle - 90
        new_x = cannonball.ball.x + (CANNONBALL_SPEED * math.cos(math.radians(corrected_angle)))
        new_y = cannonball.ball.y + (CANNONBALL_SPEED * math.sin(math.radians(corrected_angle)))
        cannonball.ball.x = new_x
        cannonball.ball.y = new_y


def create_cannonball(x: int, y: int, is_from_player: bool, angle: int) -> Cannonball:
    """
    Spawns a cannonball at the player cannon's location

    Args:
        x (int): The x initial position of the cannonball
        y (int): The y initial position of the cannonball
        is_from_player (bool): If the player shot the cannonball
        angle (int): The angle to move the cannonball
    """
    if is_from_player:
        color = "black"
    else:
        color = "red"
    ball = circle(color, 10, x, y)
    new_cannonball = Cannonball(ball, angle, is_from_player)
    return new_cannonball


def shoot_cannonball(world: World, key: str):
    """
    Spawns a cannonball when the player presses space
    Checks if they have ammo to shoot, and removes one ammo if they do

    Args:
        world (World): The world instance to get the player
        key (str): The key pressed by the user
    """
    player = world.player
    if key == "space" and player.ammo_count >= 1:
        cannon = player.cannon
        # Spawns the cannonball in the center of the cannon
        cannonball = create_cannonball(cannon.x, cannon.y + (cannon.height // 2), True, cannon.angle)
        world.cannonballs.append(cannonball)
        world.player.ammo_count -= 1


def delete_cannonball(world: World, cannonball: Cannonball):
    """
    Removes a cannonball from the world

    Args:
        world (World): The world instance
        cannonball (Cannonball): The cannonball to remove
    """
    world.cannonballs.remove(cannonball)
    destroy(cannonball.ball)


def delete_mole(world: World, mole: Mole):
    """
    Removes a mole from the world

    Args:
        world (World): The world instance
        mole (Mole): The mole to remove
    """
    world.moles.remove(mole)
    destroy(mole.mole_img)


def destroy_cannonballs_outside_window(world: World):
    """
    Removes cannonballs which don't hit anything and go off the screen

    Args:
        world (World): The world instance to get the cannonballs
    """
    for cannonball in world.cannonballs:
        x = cannonball.ball.x
        y = cannonball.ball.y
        if x < 0 or x > get_width() or y < 0 or y > get_height():
            delete_cannonball(world, cannonball)


def check_if_level_passed(world: World):
    """
    Checks if the player hit enough moles to move to the next level

    Args:
         world (World): The world instance
    """
    if world.player.moles_hit_in_current_level >= world.level:
        world.player.moles_hit_in_current_level = 0
        world.level += 1


def cannonball_collides_with_mole(world: World):
    """
    Removes both the mole and the cannonball if they collide together.
    Increases the number of moles hit by one

    Args:
        world (World): The world instance to get the cannonballs and the moles
    """
    for cannonball in world.cannonballs:
        for mole in world.moles:
            if colliding(cannonball.ball, mole.mole_img) and cannonball.is_from_player:
                delete_cannonball(world, cannonball)
                delete_mole(world, mole)
                world.player.moles_hit += 1
                world.player.moles_hit_in_current_level += 1
                check_if_level_passed(world)


def mole_faces_player(world: World):
    for mole in world.moles:
        mole_img = mole.mole_img
        cannon = world.player.cannon
        rise = cannon.y - mole_img.y
        run = cannon.x - mole_img.x
        point_in_direction(mole_img, math.degrees(math.atan2(-rise, run)) % 360)


def mole_shoots_player(world: World):
    for mole in world.moles:
        random_fire_chance = randint(1, 100) <= world.level
        if random_fire_chance:
            mole_img = mole.mole_img
            cannonball = create_cannonball(mole_img.x, mole_img.y, False, mole_img.angle - 90)
            world.cannonballs.append(cannonball)


def delete_ammo(world: World, ammo: DesignerObject):
    """
    Removes ammo from the world

    Args:
        world (World): The world instance
        ammo (DesignerObject): the ammo being picked up and removed
    """
    world.ammo.remove(ammo)
    destroy(ammo)

def ammo_dissapears(world: World):
    """
        Removes the ammo if it collides with the player.

        Args:
            world (World): The world instance to get the cannonballs and the moles
        """
    player = world.player
    for ammo in world.ammo:
        if colliding(ammo, player.cannon):
            delete_ammo(world, ammo)

def count_level() -> DesignerObject:
    """
        States which level the user's on  at the top of the screen

        Returns:
            DesignerObject: Text which displays which level the user's on
        """
    levels = text("black", "Level: ", 40, anchor="midtop")
    levels.x = 400  # Some margin so that the text doesn't hug the corner
    levels.y = 5
    return levels

def update_level(world: World):
    """
    Constantly sets the level text equal to the user's level

    Args:
        world (World): The world instance
    """
    world.levels.text = "Level: " + str(world.level)

def game_over(world: World):
    """
    When the player runs out of lives, the game ends

    Args:
        world(World): The world instance
    """
    if world.lives_count == 0:
        pause()

def loose_lives(world: World):
    """
    This function decreases the number of lives that the player
    has when they are hit by a cannonball from the moles
    Args:
        world(World): the world instance
    """
    for cannonball in world.cannonballs:
        if not cannonball.is_from_player:
            if colliding(cannonball.ball, world.player.cannon):
                world.lives_count -= 1
                delete_cannonball(world,cannonball)
                game_over(world)


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
# Handle ammo and cannonball collisions and shooting
when('typing', shoot_cannonball)
when('updating', update_cannonball_position)
when('updating', destroy_cannonballs_outside_window)
when('updating', cannonball_collides_with_mole)
when("updating", update_ammo)
when("updating", ammo_dissapears)
when("updating", update_level)
when("updating", mole_faces_player)
when("updating", mole_shoots_player)
when("updating", loose_lives)
start()

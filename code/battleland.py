"""
This file contains source code of the game "Battleland".
Author: CreativeCloudAppDev2020
"""

# Game version: Pre-release 1


# Importing necessary libraries

import sys
import uuid
import random
import pickle
import copy
from mpmath import *
from functools import reduce

mp.pretty = True


# Creating static functions to be used throughout the game


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def mpf_sum_of_list(a_list: list) -> mpf:
    return mpf(str(sum(mpf(str(elem)) for elem in a_list if is_number(str(elem)))))


def mpf_product_of_list(a_list: list) -> mpf:
    return mpf(str(reduce(lambda a, b: mpf("1") if (not is_number(str(a)) and not is_number(str(b))) else
    mpf(str(a)) if (is_number(str(a)) and not is_number(str(b))) else
    mpf(str(b)) if (is_number(str(b)) and not is_number(str(a))) else
    mpf(str(a)) * mpf(str(b)), a_list)))


def generate_random_name() -> str:
    name: str = ""  # initial value
    letters: str = "abcdefghijklmnopqrstuvwxyz"
    length: int = random.randint(6, 20)
    for i in range(length):
        name += letters[random.randint(0, len(letters) - 1)]

    name = name.capitalize()
    return name


def generate_random_hero(name):
    # type: (str) -> Hero
    max_hp: mpf = mpf(random.randint(10000, 100000))
    max_magic_points: mpf = mpf(random.randint(10000, 100000))
    attack_power: mpf = mpf(random.randint(2000, 20000))
    defense: mpf = mpf(random.randint(2000, 20000))
    crit_rate: mpf = mpf(random.randint(150, 1000))
    crit_resistance: mpf = mpf(random.randint(150, 1000))
    crit_damage: mpf = mpf(random.random() * 2)
    max_steps: int = random.randint(10, 20)
    x: int = 0
    y: int = 0
    skills: list = [
        Skill("Weak Attacking Skill", "Attacking skill causing low amount of damage.", mpf("0.05"), mpf("0.05"),
              mpf("3.5"), mpf("3.5"), mpf(random.randint(200, 500))),
        Skill("Moderate Attacking Skill", "Attacking skill causing moderate amount of damage.", mpf("0.1"), mpf("0.1"),
              mpf("7"), mpf("7"), mpf(random.randint(500, 1000))),
        Skill("Strong Attacking Skill", "Attacking skill causing high amount of damage.", mpf("0.2"), mpf("0.2"),
              mpf("15"), mpf("15"), mpf(random.randint(1000, 2000)))
    ]
    return Hero(name, max_hp, max_magic_points, attack_power, defense, crit_rate, crit_resistance, crit_damage,
                max_steps, x, y, skills)


def generate_random_game_character(name):
    # type: (str) -> GameCharacter
    max_hp: mpf = mpf(random.randint(10000, 100000))
    max_magic_points: mpf = mpf(random.randint(10000, 100000))
    attack_power: mpf = mpf(random.randint(2000, 20000))
    defense: mpf = mpf(random.randint(2000, 20000))
    crit_rate: mpf = mpf(random.randint(150, 1000))
    crit_resistance: mpf = mpf(random.randint(150, 1000))
    crit_damage: mpf = mpf(random.random() * 2)
    max_steps: int = random.randint(10, 20)
    x: int = 0
    y: int = 0
    return GameCharacter(name, max_hp, max_magic_points, attack_power, defense, crit_rate, crit_resistance, crit_damage,
                         max_steps, x, y)


def generate_random_building(name):
    # type: (str) -> Building
    max_hp: mpf = mpf(random.randint(10000, 100000))
    defense: mpf = mpf(random.randint(2000, 20000))
    x: int = 0
    y: int = 0
    return Building(name, max_hp, defense, x, y)


def generate_random_battle_tower(name):
    # type: (str) -> BattleTower
    max_hp: mpf = mpf(random.randint(10000, 100000))
    defense: mpf = mpf(random.randint(2000, 20000))
    x: int = 0
    y: int = 0
    attack_power: mpf = mpf(random.randint(2000, 20000))
    crit_rate: mpf = mpf(random.randint(150, 1000))
    crit_resistance: mpf = mpf(random.randint(150, 1000))
    crit_damage: mpf = mpf(random.random() * 2)
    return BattleTower(name, max_hp, defense, x, y, attack_power, crit_rate, crit_resistance, crit_damage)


def load_game_data(file_name):
    # type: (str) -> Game
    return pickle.load(open(file_name, "rb"))


def save_game_data(game_data, file_name):
    # type: (Game, str) -> None
    pickle.dump(game_data, open(file_name, "wb"))


# Creating necessary classes


class Battlefield:
    """
    This class contains attributes of a battlefield in this game.
    """

    BATTLEFIELD_WIDTH: int = 20
    BATTLEFIELD_HEIGHT: int = 20

    def __init__(self, name):
        # type: (str) -> None
        self.name: str = name
        self.__tiles: list = []  # initial value
        for i in range(self.BATTLEFIELD_HEIGHT):
            current: list = []  # initial value
            for j in range(self.BATTLEFIELD_WIDTH):
                current.append(Tile(j, i))

            self.__tiles.append(current)

    def get_tile_at(self, x, y):
        # type: (int, int) -> Tile or None
        if x < 0 or x >= self.BATTLEFIELD_WIDTH or y < 0 or y >= self.BATTLEFIELD_HEIGHT:
            return None
        return self.get_tiles()[y][x]

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        for i in range(self.BATTLEFIELD_HEIGHT):
            current: str = ""  # initial value
            for j in range(self.BATTLEFIELD_WIDTH):
                if j == self.BATTLEFIELD_WIDTH - 1:
                    current += str(Tile(j, i))
                else:
                    current += str(Tile(j, i)) + " | "

            res += current + "\n"

        return res

    def get_tiles(self):
        # type: () -> list
        return self.__tiles

    def clone(self):
        # type: () -> Battlefield
        return copy.deepcopy(self)


class Tile:
    """
    This class contains attributes of a tile in the battlefield.
    """

    def __init__(self, x, y):
        # type: (int, int) -> None
        self.x: int = x
        self.y: int = y
        self.building: Building or None = None  # initial value
        self.game_character: GameCharacter or None = None  # initial value

    def __str__(self):
        # type: () -> str
        if self.building is None and self.game_character is None:
            return "NONE"
        elif self.building is not None:
            return "B"
        elif self.game_character is not None:
            return "GC"

    def add_building(self, building):
        # type: (Building) -> bool
        if self.building is not None or self.game_character is not None:
            return False

        self.building = building
        return True

    def remove_building(self):
        # type: () -> None
        self.building = None

    def add_game_character(self, game_character):
        # type: (GameCharacter) -> bool
        if self.building is not None or self.game_character is not None:
            return False

        self.game_character = game_character
        return True

    def remove_game_character(self):
        # type: () -> None
        self.game_character = None

    def get_distance(self, other):
        # type: (Tile) -> int
        return abs(self.x - other.x) + abs(self.y - other.y)

    def clone(self):
        # type: () -> Tile
        return copy.deepcopy(self)


class Move:
    """
    This class contains attributes of a move that can be carried out by game characters during battles.
    """

    def __init__(self, from_tile, to_tile):
        # type: (Tile, Tile) -> None
        self.from_tile: Tile = from_tile
        self.to_tile: Tile = to_tile

    def __str__(self):
        # type: () -> str
        return "Movement from (" + str(self.from_tile.x) + ", " + str(self.from_tile.y) + ") to (" + \
               str(self.to_tile.x) + ", " + str(self.to_tile.y) + ")\n"

    def clone(self):
        # type: () -> Move
        return copy.deepcopy(self)


class Rank:
    """
    This class contains attributes of a player rank.
    """

    POSSIBLE_VALUES: list = ["WARRIOR", "ELITE", "MASTER", "GRANDMASTER", "EPIC", "LEGEND", "MYTHIC"]

    def __init__(self, value):
        # type: (str) -> None
        self.value: str = value if value in self.POSSIBLE_VALUES else self.POSSIBLE_VALUES[0]

    def __str__(self):
        # type: () -> str
        return str(self.value)

    def clone(self):
        # type: () -> Rank
        return copy.deepcopy(self)


class Player:
    """
    This class contains attributes of a player in this game.
    """

    def __init__(self, name, level=1, exp=mpf("0"), required_exp=mpf("1e6")):
        # type: (str, int, mpf, mpf) -> None
        self.player_id: str = str(uuid.uuid1())  # Randomly generate an ID for the player
        self.name: str = name
        self.level: int = level
        self.exp: mpf = exp
        self.required_exp: mpf = required_exp
        self.hero_to_control: Hero or None = None  # initial value
        self.battle_coins: mpf = mpf("0")  # initial value
        self.global_coins: mpf = mpf("0")  # initial value
        self.rank: Rank = Rank("WARRIOR")
        self.wins: int = 0
        self.loses: int = 0
        self.corresponding_team: Team or None = None  # initial value

    def update_rank(self):
        # type: () -> None
        if self.wins < 10:
            self.rank = Rank("WARRIOR")
        elif 10 <= self.wins < 100:
            self.rank = Rank("ELITE")
        elif 100 <= self.wins < 200:
            self.rank = Rank("MASTER")
        elif 200 <= self.wins < 500:
            self.rank = Rank("GRANDMASTER")
        elif 500 <= self.wins < 1000:
            self.rank = Rank("EPIC")
        elif 1000 <= self.wins < 2000:
            self.rank = Rank("LEGEND")
        else:
            self.rank = Rank("MYTHIC")

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Level: " + str(self.level) + "\n"
        res += "EXP: " + str(self.exp) + "\n"
        res += "Required EXP to have to reach next level: " + str(self.required_exp) + "\n"
        res += "Hero to control:\n" + str(self.hero_to_control) + "\n"
        res += "Battle coins: " + str(self.battle_coins) + "\n"
        res += "Global coins: " + str(self.global_coins) + "\n"
        res += "Rank: " + str(self.rank) + "\n"
        res += "Wins - Loses: " + str(self.wins) + " - " + str(self.loses) + "\n"
        res += "Corresponding Team: " + str(self.corresponding_team) + "\n"
        return res

    def buy_rune(self, rune):
        # type: (Rune) -> bool
        if self.battle_coins >= rune.purchase_battle_coin_cost and isinstance(self.hero_to_control, Hero):
            self.battle_coins -= rune.purchase_battle_coin_cost
            self.hero_to_control.add_rune(rune)
            return True
        return False

    def buy_upgrade(self, upgrade):
        # type: (Upgrade) -> bool
        if self.global_coins >= upgrade.purchase_global_coin_cost and isinstance(self.hero_to_control, Hero):
            self.global_coins -= upgrade.purchase_global_coin_cost
            self.hero_to_control.apply_upgrade(upgrade)
            return True
        return False

    def restore_battle_coins(self):
        # type: () -> None
        self.battle_coins = mpf("0")

    def set_hero_to_control(self, hero):
        # type: (Hero) -> None
        self.hero_to_control = hero

    def clone(self):
        # type: () -> Player
        return copy.deepcopy(self)


class HumanPlayer(Player):
    """
    This class contains attributes of a human player.
    """

    def __init__(self, name, level=1, exp=mpf("0"), required_exp=mpf("1e6")):
        # type: (str, int, mpf, mpf) -> None
        Player.__init__(self, name, level, exp, required_exp)


class CPUPlayer(Player):
    """
    This class contains attributes of a player controlled by the CPU.
    """

    def __init__(self, level=1, exp=mpf("0"), required_exp=mpf("1e6")):
        # type: (int, mpf, mpf) -> None
        Player.__init__(self, generate_random_name(), level, exp, required_exp)


class Team:
    """
    This class contains attributes of teams of players brought to battles.
    """

    def __init__(self, battle_squad):
        # type: (BattleSquad) -> None
        self.battle_squad: BattleSquad = battle_squad
        self.__players: list = [hero.controlling_player for hero in self.battle_squad.get_heroes()]

    def __str__(self):
        # type: () -> str
        return str(self.battle_squad)

    def clone(self):
        # type: () -> Team
        return copy.deepcopy(self)


class BattleSquad:
    """
    This class contains attributes of a squad of game characters together with buildings brought to battles.
    """

    NUM_HEROES: int = 5
    NUM_VILLAGERS: int = 5
    NUM_DEFENSE_TOWERS: int = 3

    def __init__(self, heroes, villagers, defense_towers, town_center):
        # type: (list, list, list, TownCenter) -> None
        self.__heroes: list = heroes if len(heroes) == self.NUM_HEROES else []
        self.__villagers: list = villagers if len(villagers) == self.NUM_VILLAGERS else []
        self.__defense_towers: list = defense_towers if len(defense_towers) == self.NUM_DEFENSE_TOWERS else []
        assert self.__heroes != [] and self.__villagers != [] and \
               self.__defense_towers != [], "Failed to initialise battle squad! Must have 5 heroes, " \
                                            "5 villagers, 3 battle towers, and a town center!"
        self.town_center: TownCenter = town_center

    def all_died(self):
        # type: () -> bool
        """
        This method checks whether all battle towers and the town center has been destroyed or not.
        :return: whether all battle towers and the town center has been destroyed or not
        """
        for defense_tower in self.__defense_towers:
            if defense_tower.get_is_alive():
                return False

        if self.town_center.get_is_alive():
            return False
        return True

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Below is a list of heroes in this battle squad:\n"
        for hero in self.__heroes:
            res += str(hero) + "\n"

        res += "Below is a list of villagers in this battle squad:\n"
        for villager in self.__villagers:
            res += str(villager) + "\n"

        res += "Below is a list of defense towers in this battle squad:\n"
        for defense_tower in self.__defense_towers:
            res += str(defense_tower) + "\n"

        res += "Town center:\n" + str(self.town_center) + "\n"
        return res

    def get_heroes(self):
        # type: () -> list
        return self.__heroes

    def get_villagers(self):
        # type: () -> list
        return self.__villagers

    def get_defense_towers(self):
        # type: () -> list
        return self.__defense_towers


class Building:
    """
    This class contains attributes of a building in this game.
    """

    def __init__(self, name, max_hp, defense, x, y):
        # type: (str, mpf, mpf, int, int) -> None
        self.name: str = name
        self.battle_level: int = 1
        self.battle_exp: mpf = mpf("0")
        self.required_battle_exp: mpf = mpf("0")
        self.curr_hp: mpf = max_hp
        self.max_hp: mpf = max_hp
        self.defense: mpf = defense
        self.crit_resistance: mpf = mpf("200")  # Default value
        self.x: int = x
        self.y: int = y
        self.hp_heal_rate: mpf = self.max_hp / mpf("12")
        self.is_alive: bool = self.get_is_alive()
        self.corresponding_team: Team or None = None  # initial value

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Battle Level: " + str(self.battle_level) + "\n"
        res += "Battle EXP: " + str(self.battle_exp) + "\n"
        res += "Required Battle EXP to reach next battle level: " + str(self.required_battle_exp) + "\n"
        res += "HP: " + str(self.curr_hp) + "/" + str(self.max_hp) + "\n"
        res += "Defense: " + str(self.defense) + "\n"
        res += "Location: (" + str(self.x) + ", " + str(self.y) + ")\n"
        res += "HP heal rate: " + str(self.hp_heal_rate) + " per turn\n"
        res += "Is this building still alive? " + str(self.get_is_alive()) + "\n"
        res += "Corresponding team:\n" + str(self.corresponding_team) + "\n"
        return res

    def spawn(self, x, y, battlefield):
        # type: (int, int, Battlefield) -> bool
        if 0 <= x < battlefield.BATTLEFIELD_WIDTH and 0 <= y <= \
                battlefield.BATTLEFIELD_HEIGHT:
            if battlefield.get_tiles()[y][x].building is None \
                              and battlefield.get_tiles()[y][x].game_character is None:
                self.x = x
                self.y = y
                battlefield.get_tiles()[self.y][self.x].add_building(self)
                return True
            return False
        return False

    def get_is_alive(self):
        # type: () -> bool
        self.is_alive = self.curr_hp > 0
        return self.is_alive

    def clone(self):
        # type: () -> Building
        return copy.deepcopy(self)


class BattleTower(Building):
    """
    This class contains attributes of a battle tower all teams for battles have in this game. A battle tower can
    attack a nearby game character.
    """

    def __init__(self, name, max_hp, defense, x, y, attack_power, crit_rate, crit_resistance, crit_damage):
        # type: (str, mpf, mpf, int, int, mpf, mpf, mpf, mpf) -> None
        Building.__init__(self, name, max_hp, defense, x, y)
        self.attack_power: mpf = attack_power
        self.crit_rate: mpf = crit_rate
        self.crit_resistance: mpf = crit_resistance
        self.crit_damage: mpf = crit_damage
        self.has_attacked: bool = False  # initial value

    def __str__(self):
        # type: () -> str
        res: str = Building.__str__(self)
        res += "Attack Power: " + str(self.attack_power) + "\n"
        res += "Crit Rate: " + str(self.crit_rate) + "\n"
        res += "Crit Resistance: " + str(self.crit_resistance) + "\n"
        res += "Crit Damage: " + str(self.crit_damage * 100) + "%\n"
        res += "Has this battle tower attacked? " + str(self.has_attacked) + "\n"
        return res

    def level_up(self):
        # type: () -> None
        while self.battle_exp >= self.required_battle_exp:
            self.battle_level += 1
            self.required_battle_exp *= mpf("10") ** mpf(self.battle_level ** 2)
            self.attack_power *= 2
            self.max_hp *= 2
            self.curr_hp = self.max_hp
            self.defense *= 2

    def restore_battle_level(self):
        # type: () -> None
        self.attack_power /= 2 ** (self.battle_level - 1)
        self.max_hp /= 2 ** (self.battle_level - 1)
        self.curr_hp = self.max_hp
        self.defense /= 2 ** (self.battle_level - 1)
        self.battle_level = 1

    def attack(self, target, battlefield):
        # type: (GameCharacter, Battlefield) -> bool
        if self.corresponding_team == target.corresponding_team:
            return False  # cannot attack

        if battlefield.get_tiles()[target.y][target.x].get_distance(battlefield.get_tiles()[self.y][self.x]) > 1:
            return False  # cannot attack

        is_crit: bool = random.random() <= (self.crit_rate - target.crit_resistance) / 3000
        raw_damage: mpf = self.attack_power - target.defense if not is_crit else \
            self.attack_power * self.crit_damage - target.defense
        damage: mpf = raw_damage if raw_damage > 0 else 0
        target.curr_hp -= damage
        if not target.get_is_alive():
            target.times_killed += 1
            self.battle_exp += mpf("10") ** mpf(target.battle_level ** 2)
            self.level_up()

        self.has_attacked = True
        return True

    def restore_attacked_status(self):
        # type: () -> None
        self.has_attacked = False


class TownCenter(Building):
    """
    This class contains attributes of the town center all teams for battles have in this game.
    """

    def __init__(self, name, max_hp, defense, x, y):
        # type: (str, mpf, mpf, int, int) -> None
        Building.__init__(self, name, max_hp, defense, x, y)


class GameCharacter:
    """
    This class contains attributes of a game character.
    """

    def __init__(self, name, max_hp, max_magic_points, attack_power, defense, crit_rate, crit_resistance, crit_damage,
                 max_steps, x, y):
        # type: (str, mpf, mpf, mpf, mpf, mpf, mpf, mpf, int, int, int) -> None
        self.name: str = name
        self.battle_level: int = 1
        self.battle_exp: mpf = mpf("0")
        self.required_battle_exp: mpf = mpf("1e6")
        self.curr_hp: mpf = max_hp
        self.max_hp: mpf = max_hp
        self.curr_magic_points: mpf = max_magic_points
        self.max_magic_points: mpf = max_magic_points
        self.attack_power: mpf = attack_power
        self.defense: mpf = defense
        self.crit_rate: mpf = crit_rate
        self.crit_resistance: mpf = crit_resistance
        self.crit_damage: mpf = crit_damage
        self.max_steps: int = max_steps
        self.x: int = x
        self.y: int = y
        self.hp_heal_rate: mpf = self.max_hp / mpf("12")
        self.mp_heal_rate: mpf = self.max_magic_points / mpf("12")
        self.is_alive: bool = self.get_is_alive()
        self.__upgrades_applied: list = []  # initial value
        self.corresponding_team: Team or None = None  # initial value
        self.has_moved: bool = False  # initial value
        self.has_attacked: bool = False  # initial value
        self.kills: int = 0
        self.times_killed: int = 0

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Battle Level: " + str(self.battle_level) + "\n"
        res += "Battle EXP: " + str(self.battle_exp) + "\n"
        res += "Required Battle EXP to reach next battle level: " + str(self.required_battle_exp) + "\n"
        res += "HP: " + str(self.curr_hp) + "/" + str(self.max_hp) + "\n"
        res += "Magic Points: " + str(self.curr_magic_points) + "/" + str(self.max_magic_points) + "\n"
        res += "Attack Power: " + str(self.attack_power) + "\n"
        res += "Defense: " + str(self.defense) + "\n"
        res += "Crit Rate: " + str(self.crit_rate) + "\n"
        res += "Crit Resistance: " + str(self.crit_resistance) + "\n"
        res += "Crit Damage: " + str(self.crit_damage * 100) + "%\n"
        res += "Maximum number of steps this game character can move: " + str(self.max_steps) + "\n"
        res += "Location: (" + str(self.x) + ", " + str(self.y) + ")\n"
        res += "HP heal rate: " + str(self.hp_heal_rate) + " per turn\n"
        res += "Magic Points heal rate: " + str(self.mp_heal_rate) + " per turn\n"
        res += "Is this game character alive? " + str(self.get_is_alive()) + "\n"
        res += "Below is a list of upgrades applied to this game character:\n"
        for upgrade in self.__upgrades_applied:
            res += str(upgrade) + "\n"

        res += "Corresponding team:\n" + str(self.corresponding_team) + "\n"
        res += "Has this game character moved? " + str(self.has_moved) + "\n"
        res += "Has this game character attacked? " + str(self.has_attacked) + "\n"
        res += "Number of kills done during battle: " + str(self.kills) + "\n"
        res += "Number of times killed during battle: " + str(self.times_killed) + "\n"
        return res

    def level_up(self):
        # type: () -> None
        while self.battle_exp >= self.required_battle_exp:
            self.battle_level += 1
            self.required_battle_exp *= mpf("10") ** mpf(self.battle_level ** 2)
            self.attack_power *= 2
            self.max_hp *= 2
            self.curr_hp = self.max_hp
            self.max_magic_points *= 2
            self.curr_magic_points = self.max_magic_points
            self.defense *= 2

    def restore_to_initial(self):
        # type: () -> None
        self.restore_battle_level()
        self.kills = 0
        self.times_killed = 0
        self.restore_attacked_status()
        self.restore_moved_status()

    def restore_battle_level(self):
        # type: () -> None
        self.attack_power /= 2 ** (self.battle_level - 1)
        self.max_hp /= 2 ** (self.battle_level - 1)
        self.curr_hp = self.max_hp
        self.max_magic_points /= 2 ** (self.battle_level - 1)
        self.curr_magic_points = self.max_magic_points
        self.defense /= 2 ** (self.battle_level - 1)
        self.battle_level = 1

    def spawn(self, x, y, battlefield):
        # type: (int, int, Battlefield) -> bool
        if 0 <= x < battlefield.BATTLEFIELD_WIDTH and 0 <= y <= \
                battlefield.BATTLEFIELD_HEIGHT:
            if battlefield.get_tiles()[y][x].building is None \
                              and battlefield.get_tiles()[y][x].game_character is None:
                self.x = x
                self.y = y
                battlefield.get_tiles()[self.y][self.x].add_game_character(self)
                return True
            return False
        return False

    def respawn(self, x, y, battlefield):
        # type: (int, int, Battlefield) -> bool
        if not self.get_is_alive() and 0 <= x < battlefield.BATTLEFIELD_WIDTH and 0 <= y <= \
                battlefield.BATTLEFIELD_HEIGHT:
            if battlefield.get_tiles()[y][x].building is None \
                    and battlefield.get_tiles()[y][x].game_character is None:
                self.curr_hp = self.max_hp
                self.x = x
                self.y = y
                battlefield.get_tiles()[self.y][self.x].add_game_character(self)
                return True
            return False
        return False

    def restore_attacked_status(self):
        # type: () -> None
        self.has_attacked = False

    def restore_moved_status(self):
        # type: () -> None
        self.has_moved = False

    def heal(self):
        # type: () -> None
        self.curr_hp += self.hp_heal_rate
        self.curr_magic_points += self.mp_heal_rate
        if self.curr_hp > self.max_hp:
            self.curr_hp = self.max_hp

        if self.curr_magic_points > self.max_magic_points:
            self.curr_magic_points = self.max_magic_points

    def attack(self, target, battlefield):
        # type: (Building or GameCharacter, Battlefield) -> bool
        if self.corresponding_team == target.corresponding_team:
            return False  # cannot attack

        if battlefield.get_tiles()[target.y][target.x].get_distance(battlefield.get_tiles()[self.y][self.x]) > 1:
            return False  # cannot attack

        is_crit: bool = random.random() <= (self.crit_rate - target.crit_resistance) / 3000
        raw_damage: mpf = self.attack_power - target.defense if not is_crit \
            else self.attack_power * self.crit_damage - target.defense
        damage: mpf = raw_damage if raw_damage > 0 else 0
        target.curr_hp -= damage
        if isinstance(target, GameCharacter) and not target.get_is_alive():
            self.kills += 1
            target.times_killed += 1
            self.battle_exp += mpf("10") ** mpf(target.battle_level ** 2)
            self.level_up()

        self.has_attacked = True
        return True

    def move(self, dest_x, dest_y, battlefield):
        # type: (int, int, Battlefield) -> bool
        if self.has_moved:
            return False

        if dest_x < 0 or dest_x >= battlefield.BATTLEFIELD_WIDTH or dest_y < 0 or dest_y >= \
                battlefield.BATTLEFIELD_HEIGHT:
            return False

        move: Move = Move(battlefield.get_tiles()[self.y][self.x], battlefield.get_tiles()[dest_y][dest_x])
        move_is_valid: bool = move.from_tile.get_distance(move.to_tile) <= self.max_steps \
                              and battlefield.get_tiles()[dest_y][dest_x].building is None \
                              and battlefield.get_tiles()[dest_y][dest_x].game_character is None
        if move_is_valid:
            self.x = move.to_tile.x
            self.y = move.to_tile.y
            battlefield.get_tiles()[self.y][self.x].add_game_character(self)
            self.has_moved = True
            return True
        return False

    def get_is_alive(self):
        # type: () -> bool
        self.is_alive = self.curr_hp > 0
        return self.is_alive

    def clone(self):
        # type: () -> GameCharacter
        return copy.deepcopy(self)


class PlayerCharacter(GameCharacter):
    """
    This class contains attributes of a game character which can belong to player's team.
    """

    def __init__(self, name, max_hp, max_magic_points, attack_power, defense, crit_rate, crit_resistance, crit_damage,
                 max_steps, x, y):
        # type: (str, mpf, mpf, mpf, mpf, mpf, mpf, mpf, int, int, int) -> None
        GameCharacter.__init__(self, name, max_hp, max_magic_points, attack_power, defense, crit_rate, crit_resistance,
                               crit_damage, max_steps, x, y)


class Hero(PlayerCharacter):
    """
    This class contains attributes of a hero in this game.
    """

    def __init__(self, name, max_hp, max_magic_points, attack_power, defense, crit_rate, crit_resistance, crit_damage,
                 max_steps,
                 x, y, skills):
        # type: (str, mpf, mpf, mpf, mpf, mpf, mpf, mpf, int, int, int, list) -> None
        PlayerCharacter.__init__(self, name, max_hp, max_magic_points, attack_power, defense, crit_rate,
                                 crit_resistance,
                                 crit_damage, max_steps, x, y)
        self.__skills: list = skills
        self.__runes: list = []  # initial value
        self.controlling_player: Player or None = None  # initial value

    def __str__(self):
        # type: () -> str
        res: str = GameCharacter.__str__(self)  # initial value
        res += "Below is a list of skills this hero has:\n"
        for skill in self.__skills:
            res += str(skill) + "\n"

        res += "Below is a list of runes equipped to this hero:\n"
        for rune in self.__runes:
            res += str(rune) + "\n"

        res += "Name of player controlling this hero: " + str(self.controlling_player.name) + "\n"
        return res

    def restore_to_initial(self):
        # type: () -> None
        self.restore_battle_level()
        for rune in self.__runes:
            self.remove_rune(rune)

        self.kills = 0
        self.times_killed = 0
        self.restore_attacked_status()
        self.restore_moved_status()

    def attack(self, target, battlefield, skill_to_use=None):
        # type: (Building or GameCharacter, Battlefield, Skill or None) -> bool
        curr_skill: Skill or None = None  # initial value
        if battlefield.get_tiles()[target.y][target.x].get_distance(battlefield.get_tiles()[self.y][self.x]) > 1:
            return False  # cannot attack

        if skill_to_use not in self.__skills:
            return False  # skill is not owned by the hero

        if isinstance(skill_to_use, Skill) and self.curr_magic_points < skill_to_use.magic_points_cost:
            curr_skill = None  # cannot use skill
        else:
            curr_skill = skill_to_use

        is_crit: bool = random.random() <= (self.crit_rate - target.crit_resistance) / 3000
        raw_damage: mpf = self.attack_power - target.defense if not is_crit and curr_skill is None \
            else self.attack_power * self.crit_damage - target.defense if is_crit and curr_skill is None \
            else (self.max_hp * skill_to_use.damage_multiplier_to_max_hp + self.max_magic_points *
                  skill_to_use.damage_multiplier_to_max_magic_points + self.attack_power *
                  skill_to_use.damage_multiplier_to_attack_power + self.defense *
                  skill_to_use.damage_multiplier_to_defense) - target.defense if curr_skill is not None and not is_crit \
            else (self.max_hp * skill_to_use.damage_multiplier_to_max_hp + self.max_magic_points *
                  skill_to_use.damage_multiplier_to_max_magic_points + self.attack_power *
                  skill_to_use.damage_multiplier_to_attack_power + self.defense *
                  skill_to_use.damage_multiplier_to_defense) * self.crit_damage - target.defense if curr_skill is not None \
                                                                                                    and is_crit else 0
        damage: mpf = raw_damage if raw_damage > 0 else 0
        target.curr_hp -= damage
        self.has_attacked = True
        return True

    def set_controlling_player(self, player):
        # type: (Player) -> None
        self.controlling_player = player

    def add_rune(self, rune):
        # type: (Rune) -> None
        self.__runes.append(rune)
        self.max_hp *= rune.max_hp_multiplier
        self.curr_hp = self.max_hp
        self.max_magic_points *= rune.max_magic_points_multiplier
        self.curr_magic_points = self.max_magic_points
        self.attack_power *= rune.attack_power_multiplier
        self.defense *= rune.defense_multiplier
        self.crit_rate += rune.crit_rate_up
        self.crit_damage += rune.crit_damage_up
        self.crit_resistance += rune.crit_resistance_up

    def remove_rune(self, rune):
        # type: (Rune) -> bool
        if rune in self.__runes:
            self.__runes.remove(rune)
            self.max_hp /= rune.max_hp_multiplier
            self.curr_hp = self.max_hp
            self.max_magic_points /= rune.max_magic_points_multiplier
            self.curr_magic_points = self.max_magic_points
            self.attack_power /= rune.attack_power_multiplier
            self.defense /= rune.defense_multiplier
            self.crit_rate -= rune.crit_rate_up
            self.crit_damage -= rune.crit_damage_up
            self.crit_resistance -= rune.crit_resistance_up
            return True
        return False

    def get_upgrades_applied(self):
        # type: () -> list
        return self.__upgrades_applied

    def apply_upgrade(self, upgrade):
        # type: (Upgrade) -> None
        self.__upgrades_applied.append(upgrade)
        self.max_hp *= upgrade.max_hp_multiplier
        self.curr_hp = self.max_hp
        self.max_magic_points *= upgrade.max_magic_points_multiplier
        self.curr_magic_points = self.max_magic_points
        self.attack_power *= upgrade.attack_power_multiplier
        self.defense *= upgrade.defense_multiplier
        self.crit_rate += upgrade.crit_rate_up
        self.crit_damage += upgrade.crit_damage_up
        self.crit_resistance += upgrade.crit_resistance_up

    def add_skill(self, skill):
        # type: (Skill) -> None
        self.__skills.append(skill)

    def remove_skill(self, skill):
        # type: (Skill) -> bool
        if skill in self.__skills:
            self.__skills.remove(skill)
            return True
        return False

    def get_skills(self):
        # type: () -> list
        return self.__skills


class Villager(PlayerCharacter):
    """
    This class contains attributes of a villager in this game.
    """

    def __init__(self, name, max_hp, max_magic_points, attack_power, defense, crit_rate, crit_resistance, crit_damage,
                 max_steps, x, y):
        # type: (str, mpf, mpf, mpf, mpf, mpf, mpf, mpf, int, int, int) -> None
        PlayerCharacter.__init__(self, name, max_hp, max_magic_points, attack_power, defense, crit_rate,
                                 crit_resistance,
                                 crit_damage, max_steps, x, y)


class Skill:
    """
    This class contains attributes of a skill that heroes have.
    """

    def __init__(self, name, description, damage_multiplier_to_max_hp, damage_multiplier_to_max_magic_points,
                 damage_multiplier_to_attack_power, damage_multiplier_to_defense, magic_points_cost):
        # type: (str, str, mpf, mpf, mpf, mpf, mpf) -> None
        self.name: str = name
        self.description: str = description
        self.damage_multiplier_to_max_hp: mpf = damage_multiplier_to_max_hp
        self.damage_multiplier_to_max_magic_points: mpf = damage_multiplier_to_max_magic_points
        self.damage_multiplier_to_attack_power: mpf = damage_multiplier_to_attack_power
        self.damage_multiplier_to_defense: mpf = damage_multiplier_to_defense
        self.magic_points_cost: mpf = magic_points_cost

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Description: " + str(self.description) + "\n"
        res += "Damage multiplier to max HP: " + str(self.damage_multiplier_to_max_hp) + "\n"
        res += "Damage multiplier to max Magic Points: " + str(self.damage_multiplier_to_max_magic_points) + "\n"
        res += "Damage multiplier to attack power: " + str(self.damage_multiplier_to_attack_power) + "\n"
        res += "Damage multiplier to defense: " + str(self.damage_multiplier_to_defense) + "\n"
        res += "Magic Points Cost: " + str(self.magic_points_cost) + "\n"
        return res

    def clone(self):
        # type: () -> Skill
        return copy.deepcopy(self)


class Upgrade:
    """
    This class contains attributes of upgrades which can be applied to heroes.
    """

    def __init__(self, name, max_hp_multiplier, max_magic_points_multiplier, attack_power_multiplier,
                 defense_multiplier, crit_rate_up, crit_resistance_up, crit_damage_up, purchase_global_coin_cost):
        # type: (str, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf) -> None
        self.name: str = name
        self.max_hp_multiplier: mpf = max_hp_multiplier
        self.max_magic_points_multiplier: mpf = max_magic_points_multiplier
        self.attack_power_multiplier: mpf = attack_power_multiplier
        self.defense_multiplier: mpf = defense_multiplier
        self.crit_rate_up: mpf = crit_rate_up
        self.crit_resistance_up: mpf = crit_resistance_up
        self.crit_damage_up: mpf = crit_damage_up
        self.purchase_global_coin_cost: mpf = purchase_global_coin_cost

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Max HP Multiplier: " + str(self.max_hp_multiplier) + "\n"
        res += "Max Magic Points Multiplier: " + str(self.max_magic_points_multiplier) + "\n"
        res += "Attack Power Multiplier: " + str(self.attack_power_multiplier) + "\n"
        res += "Defense Multiplier: " + str(self.defense_multiplier) + "\n"
        res += "Crit Rate Up: " + str(self.crit_rate_up) + "\n"
        res += "Crit Resistance Up: " + str(self.crit_resistance_up) + "\n"
        res += "Crit Damage Up: " + str(self.crit_damage_up * 100) + "%\n"
        res += "Global Coin Cost: " + str(self.purchase_global_coin_cost) + "\n"
        return res

    def clone(self):
        # type: () -> Upgrade
        return copy.deepcopy(self)


class Rune:
    """
    This class contains attributes of a rune which can be bought during battles and equipped to heroes.
    """

    def __init__(self, name, max_hp_multiplier, max_magic_points_multiplier, attack_power_multiplier,
                 defense_multiplier,
                 crit_rate_up, crit_resistance_up, crit_damage_up, purchase_battle_coin_cost):
        # type: (str, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf) -> None
        self.name: str = name
        self.max_hp_multiplier: mpf = max_hp_multiplier
        self.max_magic_points_multiplier: mpf = max_magic_points_multiplier
        self.attack_power_multiplier: mpf = attack_power_multiplier
        self.defense_multiplier: mpf = defense_multiplier
        self.crit_rate_up: mpf = crit_rate_up
        self.crit_resistance_up: mpf = crit_resistance_up
        self.crit_damage_up: mpf = crit_damage_up
        self.purchase_battle_coin_cost: mpf = purchase_battle_coin_cost

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Max HP Multiplier: " + str(self.max_hp_multiplier) + "\n"
        res += "Max Magic Points Multiplier: " + str(self.max_magic_points_multiplier) + "\n"
        res += "Attack Power Multiplier: " + str(self.attack_power_multiplier) + "\n"
        res += "Defense Multiplier: " + str(self.defense_multiplier) + "\n"
        res += "Crit Rate Up: " + str(self.crit_rate_up) + "\n"
        res += "Crit Resistance Up: " + str(self.crit_resistance_up) + "\n"
        res += "Crit Damage Up: " + str(self.crit_damage_up * 100) + "%\n"
        res += "Battle Coin Cost: " + str(self.purchase_battle_coin_cost) + "\n"
        return res

    def clone(self):
        # type: () -> Rune
        return copy.deepcopy(self)


class Shop:
    """
    This class contains attributes of a shop in this game.
    """

    def __init__(self):
        # type: () -> None
        self.__upgrades_sold: list = []
        self.__runes_sold: list = []

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Below is a list of upgrades sold in this shop:\n"
        for upgrade in self.__upgrades_sold:
            res += str(upgrade) + "\n"

        res += "Below is a list of runes sold in this shop:\n"
        for rune in self.__runes_sold:
            res += str(rune) + "\n"

        return res

    def get_upgrades_sold(self):
        # type: () -> list
        return self.__upgrades_sold

    def get_runes_sold(self):
        # type: () -> list
        return self.__runes_sold

    def clone(self):
        # type: () -> Shop
        return copy.deepcopy(self)


class BattlefieldShop(Shop):
    """
    This class contains attributes of a shop where the players can buy items during battles.
    """

    def __init__(self, runes_sold):
        # type: (list) -> None
        Shop.__init__(self)
        self.__runes_sold = runes_sold

    def get_upgrades_sold(self):
        # type: () -> list
        return self.__upgrades_sold

    def get_runes_sold(self):
        # type: () -> list
        return self.__runes_sold


class GlobalShop(Shop):
    """
    This class contains attributes of a shop where the players can buy items outside battles.
    """

    def __init__(self, upgrades_sold):
        # type: (list) -> None
        Shop.__init__(self)
        self.__upgrades_sold = upgrades_sold

    def get_upgrades_sold(self):
        # type: () -> list
        return self.__upgrades_sold

    def get_runes_sold(self):
        # type: () -> list
        return self.__runes_sold


class Game:
    """
    This class contains attributes of saved game data.
    """

    def __init__(self, human_players):
        # type: (list) -> None
        self.__human_players: list = human_players

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Below is a list of human players saved in this saved game data:\n"
        for human_player in self.__human_players:
            res += str(human_player) + "\n"

        return res

    def add_human_player(self, human_player):
        # type: (HumanPlayer) -> None
        self.__human_players.append(human_player)

    def get_human_players(self):
        # type: () -> list
        return self.__human_players

    def get_human_player_by_name(self, name):
        # type: (str) -> HumanPlayer or None
        for human_player in self.__human_players:
            if name == human_player.name:
                return human_player

        return None

    def get_human_player_by_index(self, index):
        # type: (int) -> HumanPlayer or None
        if index < 0 or index >= len(self.__human_players):
            return None
        return self.__human_players[index]

    def clone(self):
        # type: () -> Game
        return copy.deepcopy(self)


# Creating main function to run the game.


def main():
    """
    This main function is used to run the game.
    :return: None
    """

    print("Welcome to 'Battleland' by 'CreativeCloudAppDev2020'.")
    print("'Battleland' is an offline turn based battle arena game running on command line interface.")
    print("In order to win a battle in this game, your team has to destroy all the opponent's team's buildings.")
    print("This is as villagers and heroes can respawn in this game.")

    # Automatically load saved game data
    file_name: str = "SAVED BATTLELAND GAME PROGRESS"
    new_game: Game
    try:
        new_game = load_game_data(file_name)
    except FileNotFoundError:
        new_game = Game([])

    print("Enter 'Y' for yes.")
    print("Enter anything else for no.")
    continue_ask: str = input("Do you want to continue playing 'Battleland'? ")
    while continue_ask == "Y":
        # Asking whether the user wants to play in single player or multiplayer mode.
        ALLOWED_MODES: list = ["SINGLE PLAYER", "MULTIPLAYER"]
        print("Enter 'SINGLE PLAYER' to play in single player mode.")
        print("Enter 'MULTIPLAYER' to play in multiplayer mode.")
        mode: str = input("What game mode do you want to play in? ")
        while mode not in ALLOWED_MODES:
            print("Enter 'SINGLE PLAYER' to play in single player mode.")
            print("Enter 'MULTIPLAYER' to play in multiplayer mode.")
            mode = input("Sorry, invalid input! What game mode do you want to play in? ")

        # If the user chooses to play in single player mode
        if mode == "SINGLE PLAYER":
            # Display all the human players in the saved game data
            print("Below is a list of human players in the saved game data:\n")
            for human_player in new_game.get_human_players():
                print(str(human_player) + "\n")

            # Check whether a human player is in the saved game data or not
            if len(new_game.get_human_players()) == 0:
                # As there are no human players, ask the user to create a human player data
                print("Sorry, no human players have been saved! Please create new human player data!")
                name: str = input("Please enter your name: ")
                new_human_player: HumanPlayer = HumanPlayer(name)
                # Creating a hero for the human player to control.
                new_hero: Hero = generate_random_hero(name)
                new_hero.controlling_player = new_human_player
                new_human_player.hero_to_control = new_hero
                new_game.add_human_player(new_human_player)
            else:
                # Play single player mode
                print("You are now playing single player mode.")
                human_player_name = input("Please enter name of human player to play with: ")
                curr_human_player: HumanPlayer or None = new_game.get_human_player_by_name(human_player_name)
                while curr_human_player is None:
                    human_player_name = input("Sorry, that player does not exist! "
                                              "Please enter name of human player to play with: ")
                    curr_human_player = new_game.get_human_player_by_name(human_player_name)

                selected_human_player: HumanPlayer = new_game.get_human_player_by_name(human_player_name)
                selected_human_player.hero_to_control.controlling_player = selected_human_player

                # Create nine CPU players, place all players in two different teams of five, and then start the battle
                cpu_players: list = []  # initial value
                for i in range(9):
                    curr_cpu_player: CPUPlayer = CPUPlayer()
                    hero_to_control: Hero = generate_random_hero(curr_cpu_player.name)
                    hero_to_control.controlling_player = curr_cpu_player
                    curr_cpu_player.hero_to_control = hero_to_control
                    cpu_players.append(curr_cpu_player)

                team_1_battle_heroes: list = []  # initial value
                team_2_battle_heroes: list = []  # initial value
                if random.random() <= 0.5:
                    team_1_battle_heroes.append(selected_human_player.hero_to_control)
                else:
                    team_2_battle_heroes.append(selected_human_player.hero_to_control)

                cpu_player_index: int = 0  # initial value
                while len(team_1_battle_heroes) < 5:
                    team_1_battle_heroes.append(cpu_players[cpu_player_index].hero_to_control)
                    cpu_player_index += 1

                while len(team_2_battle_heroes) < 5:
                    team_2_battle_heroes.append(cpu_players[cpu_player_index].hero_to_control)
                    cpu_player_index += 1

                team_1_villagers: list = []  # initial value
                team_2_villagers: list = []  # initial value
                for i in range(5):
                    team_1_villagers.append(generate_random_game_character(generate_random_name()))
                    team_2_villagers.append(generate_random_game_character(generate_random_name()))

                team_1_battle_towers: list = []  # initial value
                team_2_battle_towers: list = []  # initial value
                for i in range(3):
                    team_1_battle_towers.append(generate_random_battle_tower(generate_random_name()))
                    team_2_battle_towers.append(generate_random_battle_tower(generate_random_name()))

                team_1_town_center: TownCenter = generate_random_building(generate_random_name())
                team_2_town_center: TownCenter = generate_random_building(generate_random_name())
                team1: Team = Team(BattleSquad(team_1_battle_heroes, team_1_villagers, team_1_battle_towers,
                                               team_1_town_center))
                team2: Team = Team(BattleSquad(team_2_battle_heroes, team_2_villagers, team_2_battle_towers,
                                               team_2_town_center))
                for hero in team1.battle_squad.get_heroes():
                    player: Player = hero.controlling_player
                    player.corresponding_team = team1

                for hero in team2.battle_squad.get_heroes():
                    player: Player = hero.controlling_player
                    player.corresponding_team = team2

                print("Team 1:\n" + str(team1))
                print("Team 2:\n" + str(team2))

                # Starting the battle by spawning the heroes, villagers, battle towers, and town centers
                battlefield: Battlefield = Battlefield(generate_random_name())
                for hero in team1.battle_squad.get_heroes():
                    x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                    y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                    curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                    while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                        x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile = battlefield.get_tiles()[y][x]

                    hero.spawn(x, y, battlefield)

                for hero in team2.battle_squad.get_heroes():
                    x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                    y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                    curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                    while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                        x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile = battlefield.get_tiles()[y][x]

                    hero.spawn(x, y, battlefield)

                for villager in team1.battle_squad.get_villagers():
                    x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                    y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                    curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                    while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                        x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile = battlefield.get_tiles()[y][x]

                    villager.spawn(x, y, battlefield)

                for villager in team2.battle_squad.get_villagers():
                    x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                    y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                    curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                    while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                        x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile = battlefield.get_tiles()[y][x]

                    villager.spawn(x, y, battlefield)

                for defense_tower in team1.battle_squad.get_defense_towers():
                    x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                    y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                    curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                    while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                        x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile = battlefield.get_tiles()[y][x]

                    defense_tower.spawn(x, y, battlefield)

                for defense_tower in team2.battle_squad.get_defense_towers():
                    x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                    y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                    curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                    while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                        x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile = battlefield.get_tiles()[y][x]

                    defense_tower.spawn(x, y, battlefield)

                x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                    x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                    y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                    curr_tile = battlefield.get_tiles()[y][x]

                team1.battle_squad.town_center.spawn(x, y, battlefield)
                x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                    x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                    y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                    curr_tile = battlefield.get_tiles()[y][x]

                team2.battle_squad.town_center.spawn(x, y, battlefield)

                # Initialising the battlefield shop and the rate at which battle coins are added to each player
                runes: list = []  # initial value
                for i in range(20):
                    curr_rune: Rune = Rune("Rune #" + str(i + 1), mpf("0.2") * (i + 1), mpf("0.2") * (i + 1),
                                            mpf("0.2") * (i + 1), mpf("0.2") * (i + 1), mpf("150") * (i + 1),
                                            mpf("150") * (i + 1), mpf("0.2") * (i + 1), mpf("1e5") * (mpf("10") ** i))
                    runes.append(curr_rune)

                battlefield_shop: BattlefieldShop = BattlefieldShop(runes)
                battle_coin_production_rate: mpf = mpf("1e5")
                turn: int = 0  # initial value
                while not team1.battle_squad.all_died() and not team2.battle_squad.all_died():
                    turn += 1
                    if turn % 2 == 1:
                        print("Current representation of the battlefield is as below:\n", str(battlefield))
                        print("It is team one's turn to make moves.")
                        for hero_index in range(5):
                            whose_turn: Hero = team1.battle_squad.get_heroes()[hero_index]
                            # Checking whether the player controlling the hero  is a human player or not
                            if isinstance(whose_turn.controlling_player, HumanPlayer):
                                # Ask the user whether he/she wants to buy a rune from the battlefield shop or not.
                                curr_player: Player = whose_turn.controlling_player
                                print("Below is a list of runes sold in the battlefield shop:\n")
                                for rune in battlefield_shop.get_runes_sold():
                                    print(str(rune) + "\n")

                                    # Ask the user whether he/she wants to buy a rune from the battlefield shop or not.
                                    curr_player: Player = whose_turn.controlling_player
                                    print("Below is a list of runes sold in the battlefield shop:\n")
                                    for rune in battlefield_shop.get_runes_sold():
                                        print(str(rune) + "\n")

                                print("Enter 'Y' for yes.")
                                print("Enter anything else for no.")
                                buy_ask: str = input("Do you want to buy a rune? ")
                                if buy_ask == "Y":
                                    rune_index: int = int(
                                        input("Please enter the index of the rune you want to buy: "))
                                    while rune_index < 0 or rune_index >= len(battlefield_shop.get_runes_sold()):
                                        rune_index = int(input("Sorry, invalid input! "
                                                                "Please enter the index of the rune you want to buy: "))

                                    to_buy: Rune = battlefield_shop.get_runes_sold()[rune_index]
                                    if curr_player.battle_coins >= to_buy.purchase_battle_coin_cost:
                                        print("You have successfully purchased " + str(to_buy.name) + ".")
                                        curr_player.buy_rune(to_buy)
                                    else:
                                        print("Sorry, insufficient battle coins!")

                                # Ask the user to input x and y coordinates of tile to move the hero to
                                x: int = int(input("Please enter x-coordinates of the tile to move the hero to: "))
                                y: int = int(input("Please enter y-coordinates of the tile to move the hero to: "))
                                while not whose_turn.move(x, y, battlefield):
                                    # Ask the user to input x and y coordinates of tile to move the hero to
                                    print("Invalid move! Please try again!")
                                    x = int(input("Please enter x-coordinates of the tile to move the hero to: "))
                                    y = int(input("Please enter y-coordinates of the tile to move the hero to: "))

                                # Checking whether the hero can attack or not
                                if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y)
                                    print("Enter 'Y' for yes.")
                                    print("Enter anything else for no.")
                                    attack_ask: str = input("Do you want to attack the game character or building at "
                                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                    if attack_ask == "Y":
                                        if curr_tile.building is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                print("Enter 'Y' for yes.")
                                                print("Enter anything else for no.")
                                                use_skill_ask: str = input("Do you want to use a skill? ")
                                                if use_skill_ask == "Y":
                                                    print("Below is a list of skills the hero has:\n")
                                                    for skill in whose_turn.get_skills():
                                                        print(str(skill) + "\n")

                                                    skill_index: int = int(input("Please enter index of skill to "
                                                                                 "use: "))
                                                    while skill_index < 0 or skill_index >= \
                                                        len(whose_turn.get_skills()) or (0 <= \
                                                        skill_index < len(whose_turn.get_skills()) and \
                                                        whose_turn.get_skills()[skill_index].magic_points_cost > \
                                                        whose_turn.curr_magic_points):
                                                        skill_index = int(input("Sorry, invalid input! "
                                                                                "Please enter index of skill to use: "))

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                        elif curr_tile.game_character is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                print("Enter 'Y' for yes.")
                                                print("Enter anything else for no.")
                                                use_skill_ask: str = input("Do you want to use a skill? ")
                                                if use_skill_ask == "Y":
                                                    print("Below is a list of skills the hero has:\n")
                                                    for skill in whose_turn.get_skills():
                                                        print(str(skill) + "\n")

                                                    skill_index: int = int(input("Please enter index of skill to "
                                                                                 "use: "))
                                                    while skill_index < 0 or skill_index >= \
                                                        len(whose_turn.get_skills()) or (0 <= \
                                                        skill_index < len(whose_turn.get_skills()) and \
                                                        whose_turn.get_skills()[skill_index].magic_points_cost > \
                                                        whose_turn.curr_magic_points):
                                                        skill_index = int(input("Sorry, invalid input! "
                                                                                "Please enter index of skill to use: "))

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y)
                                    print("Enter 'Y' for yes.")
                                    print("Enter anything else for no.")
                                    attack_ask: str = input("Do you want to attack the game character or building at "
                                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                    if attack_ask == "Y":
                                        if curr_tile.building is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                print("Enter 'Y' for yes.")
                                                print("Enter anything else for no.")
                                                use_skill_ask: str = input("Do you want to use a skill? ")
                                                if use_skill_ask == "Y":
                                                    print("Below is a list of skills the hero has:\n")
                                                    for skill in whose_turn.get_skills():
                                                        print(str(skill) + "\n")

                                                    skill_index: int = int(input("Please enter index of skill to "
                                                                                 "use: "))
                                                    while skill_index < 0 or skill_index >= \
                                                        len(whose_turn.get_skills()) or (0 <= \
                                                        skill_index < len(whose_turn.get_skills()) and \
                                                        whose_turn.get_skills()[skill_index].magic_points_cost > \
                                                        whose_turn.curr_magic_points):
                                                        skill_index = int(input("Sorry, invalid input! "
                                                                                "Please enter index of skill to use: "))

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                        elif curr_tile.game_character is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                print("Enter 'Y' for yes.")
                                                print("Enter anything else for no.")
                                                use_skill_ask: str = input("Do you want to use a skill? ")
                                                if use_skill_ask == "Y":
                                                    print("Below is a list of skills the hero has:\n")
                                                    for skill in whose_turn.get_skills():
                                                        print(str(skill) + "\n")

                                                    skill_index: int = int(input("Please enter index of skill to "
                                                                                 "use: "))
                                                    while skill_index < 0 or skill_index >= \
                                                        len(whose_turn.get_skills()) or (0 <= \
                                                        skill_index < len(whose_turn.get_skills()) and \
                                                        whose_turn.get_skills()[skill_index].magic_points_cost > \
                                                        whose_turn.curr_magic_points):
                                                        skill_index = int(input("Sorry, invalid input! "
                                                                                "Please enter index of skill to use: "))

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1)
                                    print("Enter 'Y' for yes.")
                                    print("Enter anything else for no.")
                                    attack_ask: str = input("Do you want to attack the game character or building at "
                                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                    if attack_ask == "Y":
                                        if curr_tile.building is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                print("Enter 'Y' for yes.")
                                                print("Enter anything else for no.")
                                                use_skill_ask: str = input("Do you want to use a skill? ")
                                                if use_skill_ask == "Y":
                                                    print("Below is a list of skills the hero has:\n")
                                                    for skill in whose_turn.get_skills():
                                                        print(str(skill) + "\n")

                                                    skill_index: int = int(input("Please enter index of skill to "
                                                                                 "use: "))
                                                    while skill_index < 0 or skill_index >= \
                                                        len(whose_turn.get_skills()) or (0 <= \
                                                        skill_index < len(whose_turn.get_skills()) and \
                                                        whose_turn.get_skills()[skill_index].magic_points_cost > \
                                                        whose_turn.curr_magic_points):
                                                        skill_index = int(input("Sorry, invalid input! "
                                                                                "Please enter index of skill to use: "))

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                        elif curr_tile.game_character is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                print("Enter 'Y' for yes.")
                                                print("Enter anything else for no.")
                                                use_skill_ask: str = input("Do you want to use a skill? ")
                                                if use_skill_ask == "Y":
                                                    print("Below is a list of skills the hero has:\n")
                                                    for skill in whose_turn.get_skills():
                                                        print(str(skill) + "\n")

                                                    skill_index: int = int(input("Please enter index of skill to "
                                                                                 "use: "))
                                                    while skill_index < 0 or skill_index >= \
                                                        len(whose_turn.get_skills()) or (0 <= \
                                                        skill_index < len(whose_turn.get_skills()) and \
                                                        whose_turn.get_skills()[skill_index].magic_points_cost > \
                                                        whose_turn.curr_magic_points):
                                                        skill_index = int(input("Sorry, invalid input! "
                                                                                "Please enter index of skill to use: "))

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1)
                                    print("Enter 'Y' for yes.")
                                    print("Enter anything else for no.")
                                    attack_ask: str = input("Do you want to attack the game character or building at "
                                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                    if attack_ask == "Y":
                                        if curr_tile.building is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                print("Enter 'Y' for yes.")
                                                print("Enter anything else for no.")
                                                use_skill_ask: str = input("Do you want to use a skill? ")
                                                if use_skill_ask == "Y":
                                                    print("Below is a list of skills the hero has:\n")
                                                    for skill in whose_turn.get_skills():
                                                        print(str(skill) + "\n")

                                                    skill_index: int = int(input("Please enter index of skill to "
                                                                                 "use: "))
                                                    while skill_index < 0 or skill_index >= \
                                                        len(whose_turn.get_skills()) or (0 <= \
                                                        skill_index < len(whose_turn.get_skills()) and \
                                                        whose_turn.get_skills()[skill_index].magic_points_cost > \
                                                        whose_turn.curr_magic_points):
                                                        skill_index = int(input("Sorry, invalid input! "
                                                                                "Please enter index of skill to use: "))

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                        elif curr_tile.game_character is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                print("Enter 'Y' for yes.")
                                                print("Enter anything else for no.")
                                                use_skill_ask: str = input("Do you want to use a skill? ")
                                                if use_skill_ask == "Y":
                                                    print("Below is a list of skills the hero has:\n")
                                                    for skill in whose_turn.get_skills():
                                                        print(str(skill) + "\n")

                                                    skill_index: int = int(input("Please enter index of skill to "
                                                                                 "use: "))
                                                    while skill_index < 0 or skill_index >= \
                                                        len(whose_turn.get_skills()) or (0 <= \
                                                        skill_index < len(whose_turn.get_skills()) and \
                                                        whose_turn.get_skills()[skill_index].magic_points_cost > \
                                                        whose_turn.curr_magic_points):
                                                        skill_index = int(input("Sorry, invalid input! "
                                                                                "Please enter index of skill to use: "))

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                            elif isinstance(whose_turn.controlling_player, CPUPlayer):
                                # Making the CPU controlled player decide whether to buy a rune or not
                                curr_player: Player = whose_turn.controlling_player
                                if random.random() <= 0.75:
                                    rune_index: int = random.randint(0, len(battlefield_shop.get_runes_sold()) - 1)
                                    while rune_index < 0 or rune_index >= len(battlefield_shop.get_runes_sold()):
                                        rune_index = random.randint(0, len(battlefield_shop.get_runes_sold()) - 1)

                                    to_buy: Rune = battlefield_shop.get_runes_sold()[rune_index]
                                    if curr_player.battle_coins >= to_buy.purchase_battle_coin_cost:
                                        curr_player.buy_rune(to_buy)

                                x: int = random.randint(0, 19)
                                y: int = random.randint(0, 19)
                                while not whose_turn.move(x, y, battlefield):
                                    x = random.randint(0, 19)
                                    y = random.randint(0, 19)

                                # Checking whether the hero can attack or not
                                if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                will_use_skill: bool = random.random() <= 0.75
                                                if will_use_skill:
                                                    skill_index: int = random.randint(0, len(whose_turn.get_skills()) - 1)
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = random.randint(0, len(whose_turn.get_skills()) - 1)

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                        elif curr_tile.game_character is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                will_use_skill: bool = random.random() <= 0.75
                                                if will_use_skill:
                                                    skill_index: int = random.randint(0,
                                                                                      len(whose_turn.get_skills()) - 1)
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = random.randint(0,
                                                                                     len(whose_turn.get_skills()) - 1)

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                will_use_skill: bool = random.random() <= 0.75
                                                if will_use_skill:
                                                    skill_index: int = random.randint(0,
                                                                                      len(whose_turn.get_skills()) - 1)
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = random.randint(0,
                                                                                     len(whose_turn.get_skills()) - 1)

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                        elif curr_tile.game_character is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                will_use_skill: bool = random.random() <= 0.75
                                                if will_use_skill:
                                                    skill_index: int = random.randint(0,
                                                                                      len(whose_turn.get_skills()) - 1)
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                                whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                        skill_index = random.randint(0,
                                                                                     len(whose_turn.get_skills()) - 1)

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                will_use_skill: bool = random.random() <= 0.75
                                                if will_use_skill:
                                                    skill_index: int = random.randint(0,
                                                                                      len(whose_turn.get_skills()) - 1)
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = random.randint(0,
                                                                                     len(whose_turn.get_skills()) - 1)

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                        elif curr_tile.game_character is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                will_use_skill: bool = random.random() <= 0.75
                                                if will_use_skill:
                                                    skill_index: int = random.randint(0,
                                                                                      len(whose_turn.get_skills()) - 1)
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                                whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                        skill_index = random.randint(0,
                                                                                     len(whose_turn.get_skills()) - 1)

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                will_use_skill: bool = random.random() <= 0.75
                                                if will_use_skill:
                                                    skill_index: int = random.randint(0,
                                                                                      len(whose_turn.get_skills()) - 1)
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                                whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                        skill_index = random.randint(0,
                                                                                     len(whose_turn.get_skills()) - 1)

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                        elif curr_tile.game_character is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                will_use_skill: bool = random.random() <= 0.75
                                                if will_use_skill:
                                                    skill_index: int = random.randint(0,
                                                                                      len(whose_turn.get_skills()) - 1)
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = random.randint(0,
                                                                                     len(whose_turn.get_skills()) - 1)

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                        # Make all the villagers in the team move.
                        for villager_index in range(5):
                            whose_turn: Villager = team1.battle_squad.get_villagers()[villager_index]
                            x: int = random.randint(0, 19)
                            y: int = random.randint(0, 19)
                            while not whose_turn.move(x, y, battlefield):
                                x = random.randint(0, 19)
                                y = random.randint(0, 19)

                            # Checking whether the hero can attack or not
                            if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y), Tile):
                                curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y)
                                will_attack: bool = random.random() <= 0.75
                                if will_attack:
                                    if curr_tile.building is not None:
                                        whose_turn.attack(curr_tile.building, battlefield)

                                    elif curr_tile.game_character is not None:
                                        whose_turn.attack(curr_tile.game_character, battlefield)

                            elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y), Tile):
                                curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y)
                                will_attack: bool = random.random() <= 0.75
                                if will_attack:
                                    if curr_tile.building is not None:
                                        whose_turn.attack(curr_tile.building, battlefield)

                                    elif curr_tile.game_character is not None:
                                        whose_turn.attack(curr_tile.game_character, battlefield)

                            elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1), Tile):
                                curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1)
                                will_attack: bool = random.random() <= 0.75
                                if will_attack:
                                    if curr_tile.building is not None:
                                        whose_turn.attack(curr_tile.building, battlefield)

                                    elif curr_tile.game_character is not None:
                                        whose_turn.attack(curr_tile.game_character, battlefield)

                            elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1), Tile):
                                curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1)
                                will_attack: bool = random.random() <= 0.75
                                if will_attack:
                                    if curr_tile.building is not None:
                                        whose_turn.attack(curr_tile.building, battlefield)

                                    elif curr_tile.game_character is not None:
                                        whose_turn.attack(curr_tile.game_character, battlefield)

                        for hero in team1.battle_squad.get_heroes():
                            hero.restore_moved_status()
                            hero.restore_attacked_status()
                            battle_coin_production_rate *= (mpf("10") ** turn)
                            hero.controlling_player.battle_coins += battle_coin_production_rate
                            hero.heal()

                        for hero in team2.battle_squad.get_heroes():
                            if not hero.get_is_alive():
                                x: int = random.randint(0, 19)
                                y: int = random.randint(0, 19)
                                curr_tile: Tile = battlefield.get_tiles()[y][x]
                                while curr_tile.game_character is not None and curr_tile.building is not None:
                                    x = random.randint(0, 19)
                                    y = random.randint(0, 19)
                                    curr_tile = battlefield.get_tiles()[y][x]

                                hero.respawn(x, y, battlefield)

                    else:
                        print("Current representation of the battlefield is as below:\n", str(battlefield))
                        print("It is team two's turn to make moves.")
                        for hero_index in range(5):
                            whose_turn: Hero = team2.battle_squad.get_heroes()[hero_index]
                            # Checking whether the player controlling the hero  is a human player or not
                            if isinstance(whose_turn.controlling_player, HumanPlayer):
                                # Ask the user whether he/she wants to buy a rune from the battlefield shop or not.
                                curr_player: Player = whose_turn.controlling_player
                                print("Below is a list of runes sold in the battlefield shop:\n")
                                for rune in battlefield_shop.get_runes_sold():
                                    print(str(rune) + "\n")

                                    # Ask the user whether he/she wants to buy a rune from the battlefield shop or not.
                                    curr_player: Player = whose_turn.controlling_player
                                    print("Below is a list of runes sold in the battlefield shop:\n")
                                    for rune in battlefield_shop.get_runes_sold():
                                        print(str(rune) + "\n")

                                print("Enter 'Y' for yes.")
                                print("Enter anything else for no.")
                                buy_ask: str = input("Do you want to buy a rune? ")
                                if buy_ask == "Y":
                                    rune_index: int = int(
                                        input("Please enter the index of the rune you want to buy: "))
                                    while rune_index < 0 or rune_index >= len(battlefield_shop.get_runes_sold()):
                                        rune_index = int(input("Sorry, invalid input! "
                                                               "Please enter the index of the rune you want to buy: "))

                                    to_buy: Rune = battlefield_shop.get_runes_sold()[rune_index]
                                    if curr_player.battle_coins >= to_buy.purchase_battle_coin_cost:
                                        print("You have successfully purchased " + str(to_buy.name) + ".")
                                        curr_player.buy_rune(to_buy)
                                    else:
                                        print("Sorry, insufficient battle coins!")

                                # Ask the user to input x and y coordinates of tile to move the hero to
                                x: int = int(input("Please enter x-coordinates of the tile to move the hero to: "))
                                y: int = int(input("Please enter y-coordinates of the tile to move the hero to: "))
                                while not whose_turn.move(x, y, battlefield):
                                    # Ask the user to input x and y coordinates of tile to move the hero to
                                    print("Invalid move! Please try again!")
                                    x = int(input("Please enter x-coordinates of the tile to move the hero to: "))
                                    y = int(input("Please enter y-coordinates of the tile to move the hero to: "))

                                # Checking whether the hero can attack or not
                                if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y)
                                    print("Enter 'Y' for yes.")
                                    print("Enter anything else for no.")
                                    attack_ask: str = input("Do you want to attack the game character or building at "
                                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                    if attack_ask == "Y":
                                        if curr_tile.building is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                print("Enter 'Y' for yes.")
                                                print("Enter anything else for no.")
                                                use_skill_ask: str = input("Do you want to use a skill? ")
                                                if use_skill_ask == "Y":
                                                    print("Below is a list of skills the hero has:\n")
                                                    for skill in whose_turn.get_skills():
                                                        print(str(skill) + "\n")

                                                    skill_index: int = int(input("Please enter index of skill to "
                                                                                 "use: "))
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = int(input("Sorry, invalid input! "
                                                                                "Please enter index of skill to use: "))

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                        elif curr_tile.game_character is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                print("Enter 'Y' for yes.")
                                                print("Enter anything else for no.")
                                                use_skill_ask: str = input("Do you want to use a skill? ")
                                                if use_skill_ask == "Y":
                                                    print("Below is a list of skills the hero has:\n")
                                                    for skill in whose_turn.get_skills():
                                                        print(str(skill) + "\n")

                                                    skill_index: int = int(input("Please enter index of skill to "
                                                                                 "use: "))
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = int(input("Sorry, invalid input! "
                                                                                "Please enter index of skill to use: "))

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y)
                                    print("Enter 'Y' for yes.")
                                    print("Enter anything else for no.")
                                    attack_ask: str = input("Do you want to attack the game character or building at "
                                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                    if attack_ask == "Y":
                                        if curr_tile.building is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                print("Enter 'Y' for yes.")
                                                print("Enter anything else for no.")
                                                use_skill_ask: str = input("Do you want to use a skill? ")
                                                if use_skill_ask == "Y":
                                                    print("Below is a list of skills the hero has:\n")
                                                    for skill in whose_turn.get_skills():
                                                        print(str(skill) + "\n")

                                                    skill_index: int = int(input("Please enter index of skill to "
                                                                                 "use: "))
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = int(input("Sorry, invalid input! "
                                                                                "Please enter index of skill to use: "))

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                        elif curr_tile.game_character is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                print("Enter 'Y' for yes.")
                                                print("Enter anything else for no.")
                                                use_skill_ask: str = input("Do you want to use a skill? ")
                                                if use_skill_ask == "Y":
                                                    print("Below is a list of skills the hero has:\n")
                                                    for skill in whose_turn.get_skills():
                                                        print(str(skill) + "\n")

                                                    skill_index: int = int(input("Please enter index of skill to "
                                                                                 "use: "))
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = int(input("Sorry, invalid input! "
                                                                                "Please enter index of skill to use: "))

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1)
                                    print("Enter 'Y' for yes.")
                                    print("Enter anything else for no.")
                                    attack_ask: str = input("Do you want to attack the game character or building at "
                                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                    if attack_ask == "Y":
                                        if curr_tile.building is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                print("Enter 'Y' for yes.")
                                                print("Enter anything else for no.")
                                                use_skill_ask: str = input("Do you want to use a skill? ")
                                                if use_skill_ask == "Y":
                                                    print("Below is a list of skills the hero has:\n")
                                                    for skill in whose_turn.get_skills():
                                                        print(str(skill) + "\n")

                                                    skill_index: int = int(input("Please enter index of skill to "
                                                                                 "use: "))
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = int(input("Sorry, invalid input! "
                                                                                "Please enter index of skill to use: "))

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                        elif curr_tile.game_character is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                print("Enter 'Y' for yes.")
                                                print("Enter anything else for no.")
                                                use_skill_ask: str = input("Do you want to use a skill? ")
                                                if use_skill_ask == "Y":
                                                    print("Below is a list of skills the hero has:\n")
                                                    for skill in whose_turn.get_skills():
                                                        print(str(skill) + "\n")

                                                    skill_index: int = int(input("Please enter index of skill to "
                                                                                 "use: "))
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = int(input("Sorry, invalid input! "
                                                                                "Please enter index of skill to use: "))

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1)
                                    print("Enter 'Y' for yes.")
                                    print("Enter anything else for no.")
                                    attack_ask: str = input("Do you want to attack the game character or building at "
                                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                    if attack_ask == "Y":
                                        if curr_tile.building is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                print("Enter 'Y' for yes.")
                                                print("Enter anything else for no.")
                                                use_skill_ask: str = input("Do you want to use a skill? ")
                                                if use_skill_ask == "Y":
                                                    print("Below is a list of skills the hero has:\n")
                                                    for skill in whose_turn.get_skills():
                                                        print(str(skill) + "\n")

                                                    skill_index: int = int(input("Please enter index of skill to "
                                                                                 "use: "))
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = int(input("Sorry, invalid input! "
                                                                                "Please enter index of skill to use: "))

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                        elif curr_tile.game_character is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                print("Enter 'Y' for yes.")
                                                print("Enter anything else for no.")
                                                use_skill_ask: str = input("Do you want to use a skill? ")
                                                if use_skill_ask == "Y":
                                                    print("Below is a list of skills the hero has:\n")
                                                    for skill in whose_turn.get_skills():
                                                        print(str(skill) + "\n")

                                                    skill_index: int = int(input("Please enter index of skill to "
                                                                                 "use: "))
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = int(input("Sorry, invalid input! "
                                                                                "Please enter index of skill to use: "))

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                            elif isinstance(whose_turn.controlling_player, CPUPlayer):
                                # Making the CPU controlled player decide whether to buy a rune or not
                                curr_player: Player = whose_turn.controlling_player
                                if random.random() <= 0.75:
                                    rune_index: int = random.randint(0, len(battlefield_shop.get_runes_sold()) - 1)
                                    while rune_index < 0 or rune_index >= len(battlefield_shop.get_runes_sold()):
                                        rune_index = random.randint(0, len(battlefield_shop.get_runes_sold()) - 1)

                                    to_buy: Rune = battlefield_shop.get_runes_sold()[rune_index]
                                    if curr_player.battle_coins >= to_buy.purchase_battle_coin_cost:
                                        curr_player.buy_rune(to_buy)

                                x: int = random.randint(0, 19)
                                y: int = random.randint(0, 19)
                                while not whose_turn.move(x, y, battlefield):
                                    x = random.randint(0, 19)
                                    y = random.randint(0, 19)

                                # Checking whether the hero can attack or not
                                if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                will_use_skill: bool = random.random() <= 0.75
                                                if will_use_skill:
                                                    skill_index: int = random.randint(0,
                                                                                      len(whose_turn.get_skills()) - 1)
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = random.randint(0,
                                                                                     len(whose_turn.get_skills()) - 1)

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                        elif curr_tile.game_character is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                will_use_skill: bool = random.random() <= 0.75
                                                if will_use_skill:
                                                    skill_index: int = random.randint(0,
                                                                                      len(whose_turn.get_skills()) - 1)
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = random.randint(0,
                                                                                     len(whose_turn.get_skills()) - 1)

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                will_use_skill: bool = random.random() <= 0.75
                                                if will_use_skill:
                                                    skill_index: int = random.randint(0,
                                                                                      len(whose_turn.get_skills()) - 1)
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = random.randint(0,
                                                                                     len(whose_turn.get_skills()) - 1)

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                        elif curr_tile.game_character is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                will_use_skill: bool = random.random() <= 0.75
                                                if will_use_skill:
                                                    skill_index: int = random.randint(0,
                                                                                      len(whose_turn.get_skills()) - 1)
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                        whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                        skill_index = random.randint(0,
                                                                                     len(whose_turn.get_skills()) - 1)

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                will_use_skill: bool = random.random() <= 0.75
                                                if will_use_skill:
                                                    skill_index: int = random.randint(0,
                                                                                      len(whose_turn.get_skills()) - 1)
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = random.randint(0,
                                                                                     len(whose_turn.get_skills()) - 1)

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                        elif curr_tile.game_character is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                will_use_skill: bool = random.random() <= 0.75
                                                if will_use_skill:
                                                    skill_index: int = random.randint(0,
                                                                                      len(whose_turn.get_skills()) - 1)
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                        whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                        skill_index = random.randint(0,
                                                                                     len(whose_turn.get_skills()) - 1)

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                will_use_skill: bool = random.random() <= 0.75
                                                if will_use_skill:
                                                    skill_index: int = random.randint(0,
                                                                                      len(whose_turn.get_skills()) - 1)
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                        whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                        skill_index = random.randint(0,
                                                                                     len(whose_turn.get_skills()) - 1)

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                        elif curr_tile.game_character is not None:
                                            skill_to_use: Skill or None = None  # initial value
                                            has_usable_skill: bool = False  # initial value
                                            for skill in whose_turn.get_skills():
                                                if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                    has_usable_skill = True

                                            if has_usable_skill:
                                                will_use_skill: bool = random.random() <= 0.75
                                                if will_use_skill:
                                                    skill_index: int = random.randint(0,
                                                                                      len(whose_turn.get_skills()) - 1)
                                                    while skill_index < 0 or skill_index >= \
                                                            len(whose_turn.get_skills()) or (0 <= \
                                                                                             skill_index < len(
                                                                whose_turn.get_skills()) and \
                                                                                             whose_turn.get_skills()[
                                                                                                 skill_index].magic_points_cost > \
                                                                                             whose_turn.curr_magic_points):
                                                        skill_index = random.randint(0,
                                                                                     len(whose_turn.get_skills()) - 1)

                                                    skill_to_use = whose_turn.get_skills()[skill_index]

                                            whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                        # Make all the villagers in the team move.
                        for villager_index in range(5):
                            whose_turn: Villager = team2.battle_squad.get_villagers()[villager_index]
                            x: int = random.randint(0, 19)
                            y: int = random.randint(0, 19)
                            while not whose_turn.move(x, y, battlefield):
                                x = random.randint(0, 19)
                                y = random.randint(0, 19)

                            # Checking whether the hero can attack or not
                            if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y), Tile):
                                curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y)
                                will_attack: bool = random.random() <= 0.75
                                if will_attack:
                                    if curr_tile.building is not None:
                                        whose_turn.attack(curr_tile.building, battlefield)

                                    elif curr_tile.game_character is not None:
                                        whose_turn.attack(curr_tile.game_character, battlefield)

                            elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y), Tile):
                                curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y)
                                will_attack: bool = random.random() <= 0.75
                                if will_attack:
                                    if curr_tile.building is not None:
                                        whose_turn.attack(curr_tile.building, battlefield)

                                    elif curr_tile.game_character is not None:
                                        whose_turn.attack(curr_tile.game_character, battlefield)

                            elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1), Tile):
                                curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1)
                                will_attack: bool = random.random() <= 0.75
                                if will_attack:
                                    if curr_tile.building is not None:
                                        whose_turn.attack(curr_tile.building, battlefield)

                                    elif curr_tile.game_character is not None:
                                        whose_turn.attack(curr_tile.game_character, battlefield)

                            elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1), Tile):
                                curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1)
                                will_attack: bool = random.random() <= 0.75
                                if will_attack:
                                    if curr_tile.building is not None:
                                        whose_turn.attack(curr_tile.building, battlefield)

                                    elif curr_tile.game_character is not None:
                                        whose_turn.attack(curr_tile.game_character, battlefield)

                        for hero in team2.battle_squad.get_heroes():
                            hero.restore_moved_status()
                            hero.restore_attacked_status()
                            battle_coin_production_rate *= (mpf("10") ** turn)
                            hero.controlling_player.battle_coins += battle_coin_production_rate
                            hero.heal()

                        for hero in team1.battle_squad.get_heroes():
                            if not hero.get_is_alive():
                                x: int = random.randint(0, 19)
                                y: int = random.randint(0, 19)
                                curr_tile: Tile = battlefield.get_tiles()[y][x]
                                while curr_tile.game_character is not None and curr_tile.building is not None:
                                    x = random.randint(0, 19)
                                    y = random.randint(0, 19)
                                    curr_tile = battlefield.get_tiles()[y][x]

                                hero.respawn(x, y, battlefield)

                if team1.battle_squad.all_died():
                    print("Team 2 wins the battle!")
                    # Give awards to all team 1 and team 2 players
                    for hero in team1.battle_squad.get_heroes():
                        corresponding_player: Player = hero.controlling_player
                        corresponding_player.global_coins += mpf("10") ** (hero.kills // 5)

                    for hero in team2.battle_squad.get_heroes():
                        corresponding_player: Player = hero.controlling_player
                        corresponding_player.global_coins += mpf("10") ** hero.kills

                elif team2.battle_squad.all_died():
                    print("Team 1 wins the battle!")
                    # Give awards to all team 1 and team 2 players
                    for hero in team1.battle_squad.get_heroes():
                        corresponding_player: Player = hero.controlling_player
                        corresponding_player.global_coins += mpf("10") ** hero.kills

                    for hero in team2.battle_squad.get_heroes():
                        corresponding_player: Player = hero.controlling_player
                        corresponding_player.global_coins += mpf("10") ** (hero.kills // 5)

                for hero in team1.battle_squad.get_heroes():
                    hero.restore_to_initial()
                    hero.controlling_player.restore_battle_coins()
                    curr_player: Player = hero.controlling_player
                    curr_player.update_rank()

                for hero in team2.battle_squad.get_heroes():
                    hero.restore_to_initial()
                    hero.controlling_player.restore_battle_coins()
                    curr_player: Player = hero.controlling_player
                    curr_player.update_rank()

        # Else if the user chooses to play in multiplayer mode
        elif mode == "MULTIPLAYER":
            # Display all the human players in the saved game data
            print("Below is a list of human players in the saved game data:\n")
            for human_player in new_game.get_human_players():
                print(str(human_player) + "\n")

            # Check whether at least two human players are in the saved game data or not
            if len(new_game.get_human_players()) < 2:
                # Tell the user that multiplayer mode cannot be played and then ask the user to choose whether he/she
                # wants to create new human player data or just proceed to deciding whether to continue playing the
                # game or not
                print("Sorry, we cannot play multiplayer mode as there are insufficient human players saved.")
                print("Enter 'Y' for yes.")
                print("Enter anything else for no.")
                create_human_player_data: str = input("Do you want to create human player data? ")
                if create_human_player_data == "Y":
                    num_human_players: int = int(input("How many new human players' data do you want to create "
                                                       "(at least 1)? "))
                    while num_human_players <= 0:
                        num_human_players = int(input("Sorry, invalid input! "
                                                      "How many new human players' data do you want to create "
                                                      "(at least 1)? "))

                    for i in range(num_human_players):
                        # Ask the user to create a human player data
                        name: str = input("Please enter your name: ")
                        new_human_player: HumanPlayer = HumanPlayer(name)
                        # Creating a hero for the human player to control.
                        new_hero: Hero = generate_random_hero(name)
                        new_hero.controlling_player = new_human_player
                        new_human_player.hero_to_control = new_hero
                        new_game.add_human_player(new_human_player)

            else:
                # Play multiplayer mode
                print("You are now playing multiplayer mode.")
                num_human_players_playing: int = int(input("How many human players are playing the game (2 - 10)? "))
                while num_human_players_playing < 2 or num_human_players_playing > 10 or num_human_players_playing < \
                        len(new_game.get_human_players()):
                    num_human_players_playing = int(
                        input("Sorry, either you input a number out of range or the number you input exceeds the "
                              "number of human players in the saved game data! How many human players are "
                              "playing the game (2 - 10)? "))

                selected_human_players: list = []  # initial value
                for i in range(num_human_players_playing):
                    # Display all the human players in the saved game data
                    print("Below is a list of human players in the saved game data:\n")
                    for human_player in new_game.get_human_players():
                        print(str(human_player) + "\n")

                    human_player_name: str = input("Please enter name of human player to be involved in the battle: ")
                    curr_human_player: HumanPlayer or None = new_game.get_human_player_by_name(human_player_name)
                    while curr_human_player is None or curr_human_player in selected_human_players:
                        human_player_name: str = input(
                            "Sorry, that player either does not exist or is already chosen! "
                            "Please enter another name of human player to be involved in the battle: ")
                        curr_human_player = new_game.get_human_player_by_name(human_player_name)

                    selected_human_player: HumanPlayer = new_game.get_human_player_by_name(human_player_name)
                    selected_human_player.hero_to_control.controlling_player = selected_human_player
                    selected_human_players.append(selected_human_player)

                # Check whether there are 10 human players selected or not. If not, add some CPU players.
                if len(selected_human_players) == 10:
                    # Start playing the 5 v 5 PVP Battle
                    print("Welcome to 5 v 5 PVP Battle!")

                    # Dividing the human players to two different teams
                    team_1_battle_heroes: list = []  # initial value
                    team_2_battle_heroes: list = []  # initial value
                    for i in range(len(selected_human_players)):
                        if i % 2 == 0:
                            team_1_battle_heroes.append(selected_human_players[i].hero_to_control)
                        else:
                            team_2_battle_heroes.append(selected_human_players[i].hero_to_control)

                    team_1_villagers: list = []  # initial value
                    team_2_villagers: list = []  # initial value
                    for i in range(5):
                        team_1_villagers.append(generate_random_game_character(generate_random_name()))
                        team_2_villagers.append(generate_random_game_character(generate_random_name()))

                    team_1_battle_towers: list = []  # initial value
                    team_2_battle_towers: list = []  # initial value
                    for i in range(3):
                        team_1_battle_towers.append(generate_random_battle_tower(generate_random_name()))
                        team_2_battle_towers.append(generate_random_battle_tower(generate_random_name()))

                    team_1_town_center: TownCenter = generate_random_building(generate_random_name())
                    team_2_town_center: TownCenter = generate_random_building(generate_random_name())
                    team1: Team = Team(BattleSquad(team_1_battle_heroes, team_1_villagers, team_1_battle_towers,
                                                   team_1_town_center))
                    team2: Team = Team(BattleSquad(team_2_battle_heroes, team_2_villagers, team_2_battle_towers,
                                                   team_2_town_center))
                    for hero in team1.battle_squad.get_heroes():
                        player: Player = hero.controlling_player
                        player.corresponding_team = team1

                    for hero in team2.battle_squad.get_heroes():
                        player: Player = hero.controlling_player
                        player.corresponding_team = team2

                    print("Team 1:\n" + str(team1))
                    print("Team 2:\n" + str(team2))

                    # Starting the battle by spawning the heroes, villagers, battle towers, and town centers
                    battlefield: Battlefield = Battlefield(generate_random_name())
                    for hero in team1.battle_squad.get_heroes():
                        x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                        while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                            x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                            y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                            curr_tile = battlefield.get_tiles()[y][x]

                        hero.spawn(x, y, battlefield)

                    for hero in team2.battle_squad.get_heroes():
                        x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                        while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                            x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                            y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                            curr_tile = battlefield.get_tiles()[y][x]

                        hero.spawn(x, y, battlefield)

                    for villager in team1.battle_squad.get_villagers():
                        x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                        while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                            x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                            y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                            curr_tile = battlefield.get_tiles()[y][x]

                        villager.spawn(x, y, battlefield)

                    for villager in team2.battle_squad.get_villagers():
                        x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                        while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                            x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                            y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                            curr_tile = battlefield.get_tiles()[y][x]

                        villager.spawn(x, y, battlefield)

                    for defense_tower in team1.battle_squad.get_defense_towers():
                        x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                        while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                            x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                            y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                            curr_tile = battlefield.get_tiles()[y][x]

                        defense_tower.spawn(x, y, battlefield)

                    for defense_tower in team2.battle_squad.get_defense_towers():
                        x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                        while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                            x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                            y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                            curr_tile = battlefield.get_tiles()[y][x]

                        defense_tower.spawn(x, y, battlefield)

                    x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                    y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                    curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                    while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                        x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile = battlefield.get_tiles()[y][x]

                    team1.battle_squad.town_center.spawn(x, y, battlefield)
                    x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                    y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                    curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                    while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                        x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile = battlefield.get_tiles()[y][x]

                    team2.battle_squad.town_center.spawn(x, y, battlefield)

                    # Initialising the battlefield shop and the rate at which battle coins are added to each player
                    runes: list = []  # initial value
                    for i in range(20):
                        curr_rune: Rune = Rune("Rune #" + str(i + 1), mpf("0.2") * (i + 1), mpf("0.2") * (i + 1),
                                               mpf("0.2") * (i + 1), mpf("0.2") * (i + 1), mpf("150") * (i + 1),
                                               mpf("150") * (i + 1), mpf("0.2") * (i + 1),
                                               mpf("1e5") * (mpf("10") ** i))
                        runes.append(curr_rune)

                    battlefield_shop: BattlefieldShop = BattlefieldShop(runes)
                    battle_coin_production_rate: mpf = mpf("1e5")
                    turn: int = 0  # initial value
                    while not team1.battle_squad.all_died() and not team2.battle_squad.all_died():
                        turn += 1
                        if turn % 2 == 1:
                            print("Current representation of the battlefield is as below:\n", str(battlefield))
                            print("It is team one's turn to make moves.")
                            for hero_index in range(5):
                                whose_turn: Hero = team1.battle_squad.get_heroes()[hero_index]
                                # Checking whether the player controlling the hero  is a human player or not
                                if isinstance(whose_turn.controlling_player, HumanPlayer):
                                    # Ask the user whether he/she wants to buy a rune from the battlefield shop or not.
                                    curr_player: Player = whose_turn.controlling_player
                                    print("Below is a list of runes sold in the battlefield shop:\n")
                                    for rune in battlefield_shop.get_runes_sold():
                                        print(str(rune) + "\n")

                                        # Ask the user whether he/she wants to buy a rune from the battlefield shop or not.
                                        curr_player: Player = whose_turn.controlling_player
                                        print("Below is a list of runes sold in the battlefield shop:\n")
                                        for rune in battlefield_shop.get_runes_sold():
                                            print(str(rune) + "\n")

                                    print("Enter 'Y' for yes.")
                                    print("Enter anything else for no.")
                                    buy_ask: str = input("Do you want to buy a rune? ")
                                    if buy_ask == "Y":
                                        rune_index: int = int(
                                            input("Please enter the index of the rune you want to buy: "))
                                        while rune_index < 0 or rune_index >= len(battlefield_shop.get_runes_sold()):
                                            rune_index = int(input("Sorry, invalid input! "
                                                                   "Please enter the index of the rune you want to buy: "))

                                        to_buy: Rune = battlefield_shop.get_runes_sold()[rune_index]
                                        if curr_player.battle_coins >= to_buy.purchase_battle_coin_cost:
                                            print("You have successfully purchased " + str(to_buy.name) + ".")
                                            curr_player.buy_rune(to_buy)
                                        else:
                                            print("Sorry, insufficient battle coins!")

                                    # Ask the user to input x and y coordinates of tile to move the hero to
                                    x: int = int(input("Please enter x-coordinates of the tile to move the hero to: "))
                                    y: int = int(input("Please enter y-coordinates of the tile to move the hero to: "))
                                    while not whose_turn.move(x, y, battlefield):
                                        # Ask the user to input x and y coordinates of tile to move the hero to
                                        print("Invalid move! Please try again!")
                                        x = int(input("Please enter x-coordinates of the tile to move the hero to: "))
                                        y = int(input("Please enter y-coordinates of the tile to move the hero to: "))

                                    # Checking whether the hero can attack or not
                                    if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y)
                                        print("Enter 'Y' for yes.")
                                        print("Enter anything else for no.")
                                        attack_ask: str = input(
                                            "Do you want to attack the game character or building at "
                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                        if attack_ask == "Y":
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y)
                                        print("Enter 'Y' for yes.")
                                        print("Enter anything else for no.")
                                        attack_ask: str = input(
                                            "Do you want to attack the game character or building at "
                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                        if attack_ask == "Y":
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1)
                                        print("Enter 'Y' for yes.")
                                        print("Enter anything else for no.")
                                        attack_ask: str = input(
                                            "Do you want to attack the game character or building at "
                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                        if attack_ask == "Y":
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1)
                                        print("Enter 'Y' for yes.")
                                        print("Enter anything else for no.")
                                        attack_ask: str = input(
                                            "Do you want to attack the game character or building at "
                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                        if attack_ask == "Y":
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                elif isinstance(whose_turn.controlling_player, CPUPlayer):
                                    # Making the CPU controlled player decide whether to buy a rune or not
                                    curr_player: Player = whose_turn.controlling_player
                                    if random.random() <= 0.75:
                                        rune_index: int = random.randint(0, len(battlefield_shop.get_runes_sold()) - 1)
                                        while rune_index < 0 or rune_index >= len(battlefield_shop.get_runes_sold()):
                                            rune_index = random.randint(0, len(battlefield_shop.get_runes_sold()) - 1)

                                        to_buy: Rune = battlefield_shop.get_runes_sold()[rune_index]
                                        if curr_player.battle_coins >= to_buy.purchase_battle_coin_cost:
                                            curr_player.buy_rune(to_buy)

                                    x: int = random.randint(0, 19)
                                    y: int = random.randint(0, 19)
                                    while not whose_turn.move(x, y, battlefield):
                                        x = random.randint(0, 19)
                                        y = random.randint(0, 19)

                                    # Checking whether the hero can attack or not
                                    if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y)
                                        will_attack: bool = random.random() <= 0.75
                                        if will_attack:
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0, len(
                                                            whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0, len(
                                                                whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y)
                                        will_attack: bool = random.random() <= 0.75
                                        if will_attack:
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                            whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1)
                                        will_attack: bool = random.random() <= 0.75
                                        if will_attack:
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                            whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1)
                                        will_attack: bool = random.random() <= 0.75
                                        if will_attack:
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                            whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                            # Make all the villagers in the team move.
                            for villager_index in range(5):
                                whose_turn: Villager = team1.battle_squad.get_villagers()[villager_index]
                                x: int = random.randint(0, 19)
                                y: int = random.randint(0, 19)
                                while not whose_turn.move(x, y, battlefield):
                                    x = random.randint(0, 19)
                                    y = random.randint(0, 19)

                                # Checking whether the hero can attack or not
                                if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            whose_turn.attack(curr_tile.building, battlefield)

                                        elif curr_tile.game_character is not None:
                                            whose_turn.attack(curr_tile.game_character, battlefield)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            whose_turn.attack(curr_tile.building, battlefield)

                                        elif curr_tile.game_character is not None:
                                            whose_turn.attack(curr_tile.game_character, battlefield)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            whose_turn.attack(curr_tile.building, battlefield)

                                        elif curr_tile.game_character is not None:
                                            whose_turn.attack(curr_tile.game_character, battlefield)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            whose_turn.attack(curr_tile.building, battlefield)

                                        elif curr_tile.game_character is not None:
                                            whose_turn.attack(curr_tile.game_character, battlefield)

                            for hero in team1.battle_squad.get_heroes():
                                hero.restore_moved_status()
                                hero.restore_attacked_status()
                                battle_coin_production_rate *= (mpf("10") ** turn)
                                hero.controlling_player.battle_coins += battle_coin_production_rate
                                hero.heal()

                            for hero in team2.battle_squad.get_heroes():
                                if not hero.get_is_alive():
                                    x: int = random.randint(0, 19)
                                    y: int = random.randint(0, 19)
                                    curr_tile: Tile = battlefield.get_tiles()[y][x]
                                    while curr_tile.game_character is not None and curr_tile.building is not None:
                                        x = random.randint(0, 19)
                                        y = random.randint(0, 19)
                                        curr_tile = battlefield.get_tiles()[y][x]

                                    hero.respawn(x, y, battlefield)

                        else:
                            print("Current representation of the battlefield is as below:\n", str(battlefield))
                            print("It is team two's turn to make moves.")
                            for hero_index in range(5):
                                whose_turn: Hero = team2.battle_squad.get_heroes()[hero_index]
                                # Checking whether the player controlling the hero  is a human player or not
                                if isinstance(whose_turn.controlling_player, HumanPlayer):
                                    # Ask the user whether he/she wants to buy a rune from the battlefield shop or not.
                                    curr_player: Player = whose_turn.controlling_player
                                    print("Below is a list of runes sold in the battlefield shop:\n")
                                    for rune in battlefield_shop.get_runes_sold():
                                        print(str(rune) + "\n")

                                    print("Enter 'Y' for yes.")
                                    print("Enter anything else for no.")
                                    buy_ask: str = input("Do you want to buy a rune? ")
                                    if buy_ask == "Y":
                                        rune_index: int = int(
                                            input("Please enter the index of the rune you want to buy: "))
                                        while rune_index < 0 or rune_index >= len(battlefield_shop.get_runes_sold()):
                                            rune_index = int(input("Sorry, invalid input! "
                                                                   "Please enter the index of the rune you want to buy: "))

                                        to_buy: Rune = battlefield_shop.get_runes_sold()[rune_index]
                                        if curr_player.battle_coins >= to_buy.purchase_battle_coin_cost:
                                            print("You have successfully purchased " + str(to_buy.name) + ".")
                                            curr_player.buy_rune(to_buy)
                                        else:
                                            print("Sorry, insufficient battle coins!")

                                    # Ask the user to input x and y coordinates of tile to move the hero to
                                    x: int = int(input("Please enter x-coordinates of the tile to move the hero to: "))
                                    y: int = int(input("Please enter y-coordinates of the tile to move the hero to: "))
                                    while not whose_turn.move(x, y, battlefield):
                                        # Ask the user to input x and y coordinates of tile to move the hero to
                                        print("Invalid move! Please try again!")
                                        x = int(input("Please enter x-coordinates of the tile to move the hero to: "))
                                        y = int(input("Please enter y-coordinates of the tile to move the hero to: "))

                                    # Checking whether the hero can attack or not
                                    if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y)
                                        print("Enter 'Y' for yes.")
                                        print("Enter anything else for no.")
                                        attack_ask: str = input(
                                            "Do you want to attack the game character or building at "
                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                        if attack_ask == "Y":
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y)
                                        print("Enter 'Y' for yes.")
                                        print("Enter anything else for no.")
                                        attack_ask: str = input(
                                            "Do you want to attack the game character or building at "
                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                        if attack_ask == "Y":
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1)
                                        print("Enter 'Y' for yes.")
                                        print("Enter anything else for no.")
                                        attack_ask: str = input(
                                            "Do you want to attack the game character or building at "
                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                        if attack_ask == "Y":
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1)
                                        print("Enter 'Y' for yes.")
                                        print("Enter anything else for no.")
                                        attack_ask: str = input(
                                            "Do you want to attack the game character or building at "
                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                        if attack_ask == "Y":
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                elif isinstance(whose_turn.controlling_player, CPUPlayer):
                                    # Making the CPU controlled player decide whether to buy a rune or not
                                    curr_player: Player = whose_turn.controlling_player
                                    if random.random() <= 0.75:
                                        rune_index: int = random.randint(0, len(battlefield_shop.get_runes_sold()) - 1)
                                        while rune_index < 0 or rune_index >= len(battlefield_shop.get_runes_sold()):
                                            rune_index = random.randint(0, len(battlefield_shop.get_runes_sold()) - 1)

                                        to_buy: Rune = battlefield_shop.get_runes_sold()[rune_index]
                                        if curr_player.battle_coins >= to_buy.purchase_battle_coin_cost:
                                            curr_player.buy_rune(to_buy)

                                    x: int = random.randint(0, 19)
                                    y: int = random.randint(0, 19)
                                    while not whose_turn.move(x, y, battlefield):
                                        x = random.randint(0, 19)
                                        y = random.randint(0, 19)

                                    # Checking whether the hero can attack or not
                                    if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y)
                                        will_attack: bool = random.random() <= 0.75
                                        if will_attack:
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0, len(
                                                            whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0, len(
                                                                whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y)
                                        will_attack: bool = random.random() <= 0.75
                                        if will_attack:
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                            whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1)
                                        will_attack: bool = random.random() <= 0.75
                                        if will_attack:
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                            whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1)
                                        will_attack: bool = random.random() <= 0.75
                                        if will_attack:
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                            whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                            # Make all the villagers in the team move.
                            for villager_index in range(5):
                                whose_turn: Villager = team1.battle_squad.get_villagers()[villager_index]
                                x: int = random.randint(0, 19)
                                y: int = random.randint(0, 19)
                                while not whose_turn.move(x, y, battlefield):
                                    x = random.randint(0, 19)
                                    y = random.randint(0, 19)

                                # Checking whether the hero can attack or not
                                if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y),
                                              Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1,
                                                                              whose_turn.y)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            whose_turn.attack(curr_tile.building, battlefield)

                                        elif curr_tile.game_character is not None:
                                            whose_turn.attack(curr_tile.game_character, battlefield)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y),
                                                Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1,
                                                                              whose_turn.y)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            whose_turn.attack(curr_tile.building, battlefield)

                                        elif curr_tile.game_character is not None:
                                            whose_turn.attack(curr_tile.game_character, battlefield)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1),
                                                Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x,
                                                                              whose_turn.y - 1)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            whose_turn.attack(curr_tile.building, battlefield)

                                        elif curr_tile.game_character is not None:
                                            whose_turn.attack(curr_tile.game_character, battlefield)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1),
                                                Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x,
                                                                              whose_turn.y + 1)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            whose_turn.attack(curr_tile.building, battlefield)

                                        elif curr_tile.game_character is not None:
                                            whose_turn.attack(curr_tile.game_character, battlefield)

                            for hero in team2.battle_squad.get_heroes():
                                hero.restore_moved_status()
                                hero.restore_attacked_status()
                                battle_coin_production_rate *= (mpf("10") ** turn)
                                hero.controlling_player.battle_coins += battle_coin_production_rate
                                hero.heal()

                            for hero in team1.battle_squad.get_heroes():
                                if not hero.get_is_alive():
                                    x: int = random.randint(0, 19)
                                    y: int = random.randint(0, 19)
                                    curr_tile: Tile = battlefield.get_tiles()[y][x]
                                    while curr_tile.game_character is not None and curr_tile.building is not None:
                                        x = random.randint(0, 19)
                                        y = random.randint(0, 19)
                                        curr_tile = battlefield.get_tiles()[y][x]

                                    hero.respawn(x, y, battlefield)

                    if team1.battle_squad.all_died():
                        print("Team 2 wins the battle!")
                        # Give awards to all team 1 and team 2 players
                        for hero in team1.battle_squad.get_heroes():
                            corresponding_player: Player = hero.controlling_player
                            corresponding_player.global_coins += mpf("10") ** (hero.kills // 5)

                        for hero in team2.battle_squad.get_heroes():
                            corresponding_player: Player = hero.controlling_player
                            corresponding_player.global_coins += mpf("10") ** hero.kills

                    elif team2.battle_squad.all_died():
                        print("Team 1 wins the battle!")
                        # Give awards to all team 1 and team 2 players
                        for hero in team1.battle_squad.get_heroes():
                            corresponding_player: Player = hero.controlling_player
                            corresponding_player.global_coins += mpf("10") ** hero.kills

                        for hero in team2.battle_squad.get_heroes():
                            corresponding_player: Player = hero.controlling_player
                            corresponding_player.global_coins += mpf("10") ** (hero.kills // 5)

                    for hero in team1.battle_squad.get_heroes():
                        hero.restore_to_initial()
                        hero.controlling_player.restore_battle_coins()
                        curr_player: Player = hero.controlling_player
                        curr_player.update_rank()

                    for hero in team2.battle_squad.get_heroes():
                        hero.restore_to_initial()
                        hero.controlling_player.restore_battle_coins()
                        curr_player: Player = hero.controlling_player
                        curr_player.update_rank()
                else:
                    # Add CPU players
                    num_cpu_players_to_add: int = 10 - len(selected_human_players)
                    cpu_players: list = []  # initial value
                    for i in range(num_cpu_players_to_add):
                        curr_cpu_player: CPUPlayer = CPUPlayer()
                        hero_to_control: Hero = generate_random_hero(curr_cpu_player.name)
                        hero_to_control.controlling_player = curr_cpu_player
                        curr_cpu_player.hero_to_control = hero_to_control
                        cpu_players.append(curr_cpu_player)

                    team_1_battle_heroes: list = []  # initial value
                    team_2_battle_heroes: list = []  # initial value
                    for i in range(len(selected_human_players)):
                        if random.random() <= 0.5:
                            team_1_battle_heroes.append(selected_human_players[i].hero_to_control)
                        else:
                            team_2_battle_heroes.append(selected_human_players[i].hero_to_control)

                    cpu_player_index: int = 0  # initial value
                    while len(team_1_battle_heroes) < 5:
                        team_1_battle_heroes.append(cpu_players[cpu_player_index].hero_to_control)
                        cpu_player_index += 1

                    while len(team_2_battle_heroes) < 5:
                        team_2_battle_heroes.append(cpu_players[cpu_player_index].hero_to_control)
                        cpu_player_index += 1

                    team_1_villagers: list = []  # initial value
                    team_2_villagers: list = []  # initial value
                    for i in range(5):
                        team_1_villagers.append(generate_random_game_character(generate_random_name()))
                        team_2_villagers.append(generate_random_game_character(generate_random_name()))

                    team_1_battle_towers: list = []  # initial value
                    team_2_battle_towers: list = []  # initial value
                    for i in range(3):
                        team_1_battle_towers.append(generate_random_battle_tower(generate_random_name()))
                        team_2_battle_towers.append(generate_random_battle_tower(generate_random_name()))

                    team_1_town_center: TownCenter = generate_random_building(generate_random_name())
                    team_2_town_center: TownCenter = generate_random_building(generate_random_name())
                    team1: Team = Team(BattleSquad(team_1_battle_heroes, team_1_villagers, team_1_battle_towers,
                                                   team_1_town_center))
                    team2: Team = Team(BattleSquad(team_2_battle_heroes, team_2_villagers, team_2_battle_towers,
                                                   team_2_town_center))
                    for hero in team1.battle_squad.get_heroes():
                        player: Player = hero.controlling_player
                        player.corresponding_team = team1

                    for hero in team2.battle_squad.get_heroes():
                        player: Player = hero.controlling_player
                        player.corresponding_team = team2

                    print("Team 1:\n" + str(team1))
                    print("Team 2:\n" + str(team2))

                    # Starting the battle by spawning the heroes, villagers, battle towers, and town centers
                    battlefield: Battlefield = Battlefield(generate_random_name())
                    for hero in team1.battle_squad.get_heroes():
                        x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                        while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                            x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                            y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                            curr_tile = battlefield.get_tiles()[y][x]

                        hero.spawn(x, y, battlefield)

                    for hero in team2.battle_squad.get_heroes():
                        x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                        while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                            x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                            y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                            curr_tile = battlefield.get_tiles()[y][x]

                        hero.spawn(x, y, battlefield)

                    for villager in team1.battle_squad.get_villagers():
                        x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                        while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                            x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                            y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                            curr_tile = battlefield.get_tiles()[y][x]

                        villager.spawn(x, y, battlefield)

                    for villager in team2.battle_squad.get_villagers():
                        x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                        while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                            x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                            y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                            curr_tile = battlefield.get_tiles()[y][x]

                        villager.spawn(x, y, battlefield)

                    for defense_tower in team1.battle_squad.get_defense_towers():
                        x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                        while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                            x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                            y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                            curr_tile = battlefield.get_tiles()[y][x]

                        defense_tower.spawn(x, y, battlefield)

                    for defense_tower in team2.battle_squad.get_defense_towers():
                        x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                        while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                            x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                            y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                            curr_tile = battlefield.get_tiles()[y][x]

                        defense_tower.spawn(x, y, battlefield)

                    x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                    y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                    curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                    while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                        x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile = battlefield.get_tiles()[y][x]

                    team1.battle_squad.town_center.spawn(x, y, battlefield)
                    x: int = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                    y: int = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                    curr_tile: Tile or None = battlefield.get_tiles()[y][x]
                    while curr_tile is None or curr_tile.building is not None or curr_tile.game_character is not None:
                        x = random.randint(0, battlefield.BATTLEFIELD_WIDTH - 1)
                        y = random.randint(0, battlefield.BATTLEFIELD_HEIGHT - 1)
                        curr_tile = battlefield.get_tiles()[y][x]

                    team2.battle_squad.town_center.spawn(x, y, battlefield)

                    # Initialising the battlefield shop and the rate at which battle coins are added to each player
                    runes: list = []  # initial value
                    for i in range(20):
                        curr_rune: Rune = Rune("Rune #" + str(i + 1), mpf("0.2") * (i + 1), mpf("0.2") * (i + 1),
                                               mpf("0.2") * (i + 1), mpf("0.2") * (i + 1), mpf("150") * (i + 1),
                                               mpf("150") * (i + 1), mpf("0.2") * (i + 1),
                                               mpf("1e5") * (mpf("10") ** i))
                        runes.append(curr_rune)

                    battlefield_shop: BattlefieldShop = BattlefieldShop(runes)
                    battle_coin_production_rate: mpf = mpf("1e5")
                    turn: int = 0  # initial value
                    while not team1.battle_squad.all_died() and not team2.battle_squad.all_died():
                        turn += 1
                        if turn % 2 == 1:
                            print("Current representation of the battlefield is as below:\n", str(battlefield))
                            print("It is team one's turn to make moves.")
                            for hero_index in range(5):
                                whose_turn: Hero = team1.battle_squad.get_heroes()[hero_index]
                                # Checking whether the player controlling the hero  is a human player or not
                                if isinstance(whose_turn.controlling_player, HumanPlayer):
                                    # Ask the user whether he/she wants to buy a rune from the battlefield shop or not.
                                    curr_player: Player = whose_turn.controlling_player
                                    print("Below is a list of runes sold in the battlefield shop:\n")
                                    for rune in battlefield_shop.get_runes_sold():
                                        print(str(rune) + "\n")

                                        # Ask the user whether he/she wants to buy a rune from the battlefield shop or not.
                                        curr_player: Player = whose_turn.controlling_player
                                        print("Below is a list of runes sold in the battlefield shop:\n")
                                        for rune in battlefield_shop.get_runes_sold():
                                            print(str(rune) + "\n")

                                    print("Enter 'Y' for yes.")
                                    print("Enter anything else for no.")
                                    buy_ask: str = input("Do you want to buy a rune? ")
                                    if buy_ask == "Y":
                                        rune_index: int = int(
                                            input("Please enter the index of the rune you want to buy: "))
                                        while rune_index < 0 or rune_index >= len(battlefield_shop.get_runes_sold()):
                                            rune_index = int(input("Sorry, invalid input! "
                                                                   "Please enter the index of the rune you want to buy: "))

                                        to_buy: Rune = battlefield_shop.get_runes_sold()[rune_index]
                                        if curr_player.battle_coins >= to_buy.purchase_battle_coin_cost:
                                            print("You have successfully purchased " + str(to_buy.name) + ".")
                                            curr_player.buy_rune(to_buy)
                                        else:
                                            print("Sorry, insufficient battle coins!")

                                    # Ask the user to input x and y coordinates of tile to move the hero to
                                    x: int = int(input("Please enter x-coordinates of the tile to move the hero to: "))
                                    y: int = int(input("Please enter y-coordinates of the tile to move the hero to: "))
                                    while not whose_turn.move(x, y, battlefield):
                                        # Ask the user to input x and y coordinates of tile to move the hero to
                                        print("Invalid move! Please try again!")
                                        x = int(input("Please enter x-coordinates of the tile to move the hero to: "))
                                        y = int(input("Please enter y-coordinates of the tile to move the hero to: "))

                                    # Checking whether the hero can attack or not
                                    if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y)
                                        print("Enter 'Y' for yes.")
                                        print("Enter anything else for no.")
                                        attack_ask: str = input(
                                            "Do you want to attack the game character or building at "
                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                        if attack_ask == "Y":
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y)
                                        print("Enter 'Y' for yes.")
                                        print("Enter anything else for no.")
                                        attack_ask: str = input(
                                            "Do you want to attack the game character or building at "
                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                        if attack_ask == "Y":
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1)
                                        print("Enter 'Y' for yes.")
                                        print("Enter anything else for no.")
                                        attack_ask: str = input(
                                            "Do you want to attack the game character or building at "
                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                        if attack_ask == "Y":
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1)
                                        print("Enter 'Y' for yes.")
                                        print("Enter anything else for no.")
                                        attack_ask: str = input(
                                            "Do you want to attack the game character or building at "
                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                        if attack_ask == "Y":
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                elif isinstance(whose_turn.controlling_player, CPUPlayer):
                                    # Making the CPU controlled player decide whether to buy a rune or not
                                    curr_player: Player = whose_turn.controlling_player
                                    if random.random() <= 0.75:
                                        rune_index: int = random.randint(0, len(battlefield_shop.get_runes_sold()) - 1)
                                        while rune_index < 0 or rune_index >= len(battlefield_shop.get_runes_sold()):
                                            rune_index = random.randint(0, len(battlefield_shop.get_runes_sold()) - 1)

                                        to_buy: Rune = battlefield_shop.get_runes_sold()[rune_index]
                                        if curr_player.battle_coins >= to_buy.purchase_battle_coin_cost:
                                            curr_player.buy_rune(to_buy)

                                    x: int = random.randint(0, 19)
                                    y: int = random.randint(0, 19)
                                    while not whose_turn.move(x, y, battlefield):
                                        x = random.randint(0, 19)
                                        y = random.randint(0, 19)

                                    # Checking whether the hero can attack or not
                                    if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y)
                                        will_attack: bool = random.random() <= 0.75
                                        if will_attack:
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0, len(
                                                            whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0, len(
                                                                whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y)
                                        will_attack: bool = random.random() <= 0.75
                                        if will_attack:
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                            whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1)
                                        will_attack: bool = random.random() <= 0.75
                                        if will_attack:
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                            whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1)
                                        will_attack: bool = random.random() <= 0.75
                                        if will_attack:
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                            whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                            # Make all the villagers in the team move.
                            for villager_index in range(5):
                                whose_turn: Villager = team1.battle_squad.get_villagers()[villager_index]
                                x: int = random.randint(0, 19)
                                y: int = random.randint(0, 19)
                                while not whose_turn.move(x, y, battlefield):
                                    x = random.randint(0, 19)
                                    y = random.randint(0, 19)

                                # Checking whether the hero can attack or not
                                if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            whose_turn.attack(curr_tile.building, battlefield)

                                        elif curr_tile.game_character is not None:
                                            whose_turn.attack(curr_tile.game_character, battlefield)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            whose_turn.attack(curr_tile.building, battlefield)

                                        elif curr_tile.game_character is not None:
                                            whose_turn.attack(curr_tile.game_character, battlefield)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            whose_turn.attack(curr_tile.building, battlefield)

                                        elif curr_tile.game_character is not None:
                                            whose_turn.attack(curr_tile.game_character, battlefield)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1), Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            whose_turn.attack(curr_tile.building, battlefield)

                                        elif curr_tile.game_character is not None:
                                            whose_turn.attack(curr_tile.game_character, battlefield)

                            for hero in team1.battle_squad.get_heroes():
                                hero.restore_moved_status()
                                hero.restore_attacked_status()
                                battle_coin_production_rate *= (mpf("10") ** turn)
                                hero.controlling_player.battle_coins += battle_coin_production_rate
                                hero.heal()

                            for hero in team2.battle_squad.get_heroes():
                                if not hero.get_is_alive():
                                    x: int = random.randint(0, 19)
                                    y: int = random.randint(0, 19)
                                    curr_tile: Tile = battlefield.get_tiles()[y][x]
                                    while curr_tile.game_character is not None and curr_tile.building is not None:
                                        x = random.randint(0, 19)
                                        y = random.randint(0, 19)
                                        curr_tile = battlefield.get_tiles()[y][x]

                                    hero.respawn(x, y, battlefield)

                        else:
                            print("Current representation of the battlefield is as below:\n", str(battlefield))
                            print("It is team two's turn to make moves.")
                            for hero_index in range(5):
                                whose_turn: Hero = team2.battle_squad.get_heroes()[hero_index]
                                # Checking whether the player controlling the hero  is a human player or not
                                if isinstance(whose_turn.controlling_player, HumanPlayer):
                                    # Ask the user whether he/she wants to buy a rune from the battlefield shop or not.
                                    curr_player: Player = whose_turn.controlling_player
                                    print("Below is a list of runes sold in the battlefield shop:\n")
                                    for rune in battlefield_shop.get_runes_sold():
                                        print(str(rune) + "\n")

                                    print("Enter 'Y' for yes.")
                                    print("Enter anything else for no.")
                                    buy_ask: str = input("Do you want to buy a rune? ")
                                    if buy_ask == "Y":
                                        rune_index: int = int(
                                            input("Please enter the index of the rune you want to buy: "))
                                        while rune_index < 0 or rune_index >= len(battlefield_shop.get_runes_sold()):
                                            rune_index = int(input("Sorry, invalid input! "
                                                                   "Please enter the index of the rune you want to buy: "))

                                        to_buy: Rune = battlefield_shop.get_runes_sold()[rune_index]
                                        if curr_player.battle_coins >= to_buy.purchase_battle_coin_cost:
                                            print("You have successfully purchased " + str(to_buy.name) + ".")
                                            curr_player.buy_rune(to_buy)
                                        else:
                                            print("Sorry, insufficient battle coins!")

                                    # Ask the user to input x and y coordinates of tile to move the hero to
                                    x: int = int(input("Please enter x-coordinates of the tile to move the hero to: "))
                                    y: int = int(input("Please enter y-coordinates of the tile to move the hero to: "))
                                    while not whose_turn.move(x, y, battlefield):
                                        # Ask the user to input x and y coordinates of tile to move the hero to
                                        print("Invalid move! Please try again!")
                                        x = int(input("Please enter x-coordinates of the tile to move the hero to: "))
                                        y = int(input("Please enter y-coordinates of the tile to move the hero to: "))

                                    # Checking whether the hero can attack or not
                                    if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y)
                                        print("Enter 'Y' for yes.")
                                        print("Enter anything else for no.")
                                        attack_ask: str = input(
                                            "Do you want to attack the game character or building at "
                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                        if attack_ask == "Y":
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y)
                                        print("Enter 'Y' for yes.")
                                        print("Enter anything else for no.")
                                        attack_ask: str = input(
                                            "Do you want to attack the game character or building at "
                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                        if attack_ask == "Y":
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1)
                                        print("Enter 'Y' for yes.")
                                        print("Enter anything else for no.")
                                        attack_ask: str = input(
                                            "Do you want to attack the game character or building at "
                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                        if attack_ask == "Y":
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1)
                                        print("Enter 'Y' for yes.")
                                        print("Enter anything else for no.")
                                        attack_ask: str = input(
                                            "Do you want to attack the game character or building at "
                                            "(" + str(curr_tile.x) + ", " + str(curr_tile.y) + ")? ")
                                        if attack_ask == "Y":
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    print("Enter 'Y' for yes.")
                                                    print("Enter anything else for no.")
                                                    use_skill_ask: str = input("Do you want to use a skill? ")
                                                    if use_skill_ask == "Y":
                                                        print("Below is a list of skills the hero has:\n")
                                                        for skill in whose_turn.get_skills():
                                                            print(str(skill) + "\n")

                                                        skill_index: int = int(input("Please enter index of skill to "
                                                                                     "use: "))
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = int(input("Sorry, invalid input! "
                                                                                    "Please enter index of skill to use: "))

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                elif isinstance(whose_turn.controlling_player, CPUPlayer):
                                    # Making the CPU controlled player decide whether to buy a rune or not
                                    curr_player: Player = whose_turn.controlling_player
                                    if random.random() <= 0.75:
                                        rune_index: int = random.randint(0, len(battlefield_shop.get_runes_sold()) - 1)
                                        while rune_index < 0 or rune_index >= len(battlefield_shop.get_runes_sold()):
                                            rune_index = random.randint(0, len(battlefield_shop.get_runes_sold()) - 1)

                                        to_buy: Rune = battlefield_shop.get_runes_sold()[rune_index]
                                        if curr_player.battle_coins >= to_buy.purchase_battle_coin_cost:
                                            curr_player.buy_rune(to_buy)

                                    x: int = random.randint(0, 19)
                                    y: int = random.randint(0, 19)
                                    while not whose_turn.move(x, y, battlefield):
                                        x = random.randint(0, 19)
                                        y = random.randint(0, 19)

                                    # Checking whether the hero can attack or not
                                    if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y)
                                        will_attack: bool = random.random() <= 0.75
                                        if will_attack:
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0, len(
                                                            whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0, len(
                                                                whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y)
                                        will_attack: bool = random.random() <= 0.75
                                        if will_attack:
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                            whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1)
                                        will_attack: bool = random.random() <= 0.75
                                        if will_attack:
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                            whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                                    elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1), Tile):
                                        curr_tile: Tile = battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1)
                                        will_attack: bool = random.random() <= 0.75
                                        if will_attack:
                                            if curr_tile.building is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= skill_index < len(
                                                            whose_turn.get_skills()) and whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.building, battlefield, skill_to_use)

                                            elif curr_tile.game_character is not None:
                                                skill_to_use: Skill or None = None  # initial value
                                                has_usable_skill: bool = False  # initial value
                                                for skill in whose_turn.get_skills():
                                                    if skill.magic_points_cost <= whose_turn.curr_magic_points:
                                                        has_usable_skill = True

                                                if has_usable_skill:
                                                    will_use_skill: bool = random.random() <= 0.75
                                                    if will_use_skill:
                                                        skill_index: int = random.randint(0,
                                                                                          len(
                                                                                              whose_turn.get_skills()) - 1)
                                                        while skill_index < 0 or skill_index >= \
                                                                len(whose_turn.get_skills()) or (0 <= \
                                                                                                 skill_index < len(
                                                                    whose_turn.get_skills()) and \
                                                                                                 whose_turn.get_skills()[
                                                                                                     skill_index].magic_points_cost > \
                                                                                                 whose_turn.curr_magic_points):
                                                            skill_index = random.randint(0,
                                                                                         len(
                                                                                             whose_turn.get_skills()) - 1)

                                                        skill_to_use = whose_turn.get_skills()[skill_index]

                                                whose_turn.attack(curr_tile.game_character, battlefield, skill_to_use)

                            # Make all the villagers in the team move.
                            for villager_index in range(5):
                                whose_turn: Villager = team1.battle_squad.get_villagers()[villager_index]
                                x: int = random.randint(0, 19)
                                y: int = random.randint(0, 19)
                                while not whose_turn.move(x, y, battlefield):
                                    x = random.randint(0, 19)
                                    y = random.randint(0, 19)

                                # Checking whether the hero can attack or not
                                if isinstance(battlefield.get_tile_at(whose_turn.x - 1, whose_turn.y),
                                              Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x - 1,
                                                                              whose_turn.y)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            whose_turn.attack(curr_tile.building, battlefield)

                                        elif curr_tile.game_character is not None:
                                            whose_turn.attack(curr_tile.game_character, battlefield)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x + 1, whose_turn.y),
                                                Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x + 1,
                                                                              whose_turn.y)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            whose_turn.attack(curr_tile.building, battlefield)

                                        elif curr_tile.game_character is not None:
                                            whose_turn.attack(curr_tile.game_character, battlefield)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y - 1),
                                                Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x,
                                                                              whose_turn.y - 1)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            whose_turn.attack(curr_tile.building, battlefield)

                                        elif curr_tile.game_character is not None:
                                            whose_turn.attack(curr_tile.game_character, battlefield)

                                elif isinstance(battlefield.get_tile_at(whose_turn.x, whose_turn.y + 1),
                                                Tile):
                                    curr_tile: Tile = battlefield.get_tile_at(whose_turn.x,
                                                                              whose_turn.y + 1)
                                    will_attack: bool = random.random() <= 0.75
                                    if will_attack:
                                        if curr_tile.building is not None:
                                            whose_turn.attack(curr_tile.building, battlefield)

                                        elif curr_tile.game_character is not None:
                                            whose_turn.attack(curr_tile.game_character, battlefield)

                            for hero in team2.battle_squad.get_heroes():
                                hero.restore_moved_status()
                                hero.restore_attacked_status()
                                battle_coin_production_rate *= (mpf("10") ** turn)
                                hero.controlling_player.battle_coins += battle_coin_production_rate
                                hero.heal()

                            for hero in team1.battle_squad.get_heroes():
                                if not hero.get_is_alive():
                                    x: int = random.randint(0, 19)
                                    y: int = random.randint(0, 19)
                                    curr_tile: Tile = battlefield.get_tiles()[y][x]
                                    while curr_tile.game_character is not None and curr_tile.building is not None:
                                        x = random.randint(0, 19)
                                        y = random.randint(0, 19)
                                        curr_tile = battlefield.get_tiles()[y][x]

                                    hero.respawn(x, y, battlefield)

                    if team1.battle_squad.all_died():
                        print("Team 2 wins the battle!")
                        # Give awards to all team 1 and team 2 players
                        for hero in team1.battle_squad.get_heroes():
                            corresponding_player: Player = hero.controlling_player
                            corresponding_player.global_coins += mpf("10") ** (hero.kills // 5)

                        for hero in team2.battle_squad.get_heroes():
                            corresponding_player: Player = hero.controlling_player
                            corresponding_player.global_coins += mpf("10") ** hero.kills

                    elif team2.battle_squad.all_died():
                        print("Team 1 wins the battle!")
                        # Give awards to all team 1 and team 2 players
                        for hero in team1.battle_squad.get_heroes():
                            corresponding_player: Player = hero.controlling_player
                            corresponding_player.global_coins += mpf("10") ** hero.kills

                        for hero in team2.battle_squad.get_heroes():
                            corresponding_player: Player = hero.controlling_player
                            corresponding_player.global_coins += mpf("10") ** (hero.kills // 5)

                    for hero in team1.battle_squad.get_heroes():
                        hero.restore_to_initial()
                        hero.controlling_player.restore_battle_coins()
                        curr_player: Player = hero.controlling_player
                        curr_player.update_rank()

                    for hero in team2.battle_squad.get_heroes():
                        hero.restore_to_initial()
                        hero.controlling_player.restore_battle_coins()
                        curr_player: Player = hero.controlling_player
                        curr_player.update_rank()

        # Display all the human players in the saved game data
        print("Below is a list of human players in the saved game data:\n")
        for human_player in new_game.get_human_players():
            print(str(human_player) + "\n")

        human_player_name: str = input("Please enter name of human player you want to play as: ")
        curr_human_player: HumanPlayer or None = new_game.get_human_player_by_name(human_player_name)
        while curr_human_player is None:
            human_player_name: str = input("Sorry, that player does not exist! "
                                           "Please enter another name of human player you want to play as: ")
            curr_human_player: HumanPlayer or None = new_game.get_human_player_by_name(human_player_name)

        selected_human_player: HumanPlayer = curr_human_player
        upgrades: list = []  # initial value
        for i in range(20):
            curr_upgrade: Upgrade = Upgrade("Upgrade #" + str(i + 1), mpf("0.2") * (i + 1), mpf("0.2") * (i + 1),
                                            mpf("0.2") * (i + 1), mpf("0.2") * (i + 1), mpf("150") * (i + 1),
                                            mpf("150") * (i + 1), mpf("0.2") * (i + 1), mpf("1e5") * (mpf("10") ** i))
            upgrades.append(curr_upgrade)

        global_shop: GlobalShop = GlobalShop(upgrades)
        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        buy_from_global_shop: str = input("Do you want to buy an upgrade from the global shop? ")
        if buy_from_global_shop == "Y":
            print("Below is a list of upgrades sold in the global shop:\n")
            for upgrade in global_shop.get_upgrades_sold():
                print(str(upgrade) + "\n")

            upgrade_index: int = int(input("Please enter index of upgrade you want to purchase: "))
            while upgrade_index < 0 or upgrade_index >= len(global_shop.get_upgrades_sold()):
                upgrade_index = int(input("Sorry, invalid input! "
                                          "Please enter index of upgrade you want to purchase: "))

            to_buy: Upgrade = global_shop.get_upgrades_sold()[upgrade_index]
            if selected_human_player.global_coins >= to_buy.purchase_global_coin_cost:
                print("Congratulations! You have successfully bought " + str(to_buy.name) + ".")
                selected_human_player.buy_upgrade(to_buy)
            else:
                print("Sorry, insufficient global coins!")

        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_ask = input("Do you want to continue playing 'Battleland'? ")

    # Automatically save game data
    save_game_data(new_game, file_name)
    sys.exit()


if __name__ == '__main__':
    main()

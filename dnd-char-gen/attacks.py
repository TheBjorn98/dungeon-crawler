from constants import Abilities
from dataclasses import dataclass
from enum import Enum
from rolls import d20, roll_dice, Roll

class Damage_types(Enum):
    piercing = 0
    bludgeoning = 1
    slashing = 2
    fire = 3
    lightning = 4
    thunder = 5
    frost = 6
    acid = 7
    force = 8


class Weapon_types(Enum):
    simple = 0
    martial = 1
    simple_ranged = 2
    martial_ranged = 3
    special = 4


# beoran.attack_with(beoran.inventory[0])

@dataclass
class Weapon:
    name: str
    bonus_mod: Abilities
    damage: Roll
    damage_type: Damage_types
    weapon_type: Weapon_types
    range: int

    def roll_damage(self):
        return self.damage.roll()


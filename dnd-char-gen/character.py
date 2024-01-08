from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from rolls import d20, Roll
from attacks import Weapon, Weapon_types, Damage_types
from constants import Abilities, Skills, get_governing_ability

class CharacterClasses(Enum):
    fighter = 0
    paladin = 1
    rogue = 2
    wizard = 3


class Races(Enum):
    human = 0
    elf = 1
    orc = 2
    dwarf = 3
    dragonborn = 4


class Backgrounds(Enum):
    soldier = 0
    urchin = 1
    sage = 2
    outlander = 3


@dataclass
class Appearance:
    age: int
    height: float
    weight: float
    skin: str
    hair: str
    eyes: str


@dataclass
class Personality:
    traits: List[str]
    ideals: List[str]
    bonds: List[str]
    flaws: List[str]


def get_prof_bonus_from_level(level: int) -> int:
    return 2 + ((level - 1) // 4)


def get_modifier_from_score(score: int) -> int:
    return ((score - 10) // 2)


@dataclass
class Character:
    name: str
    race: Races
    character_class: CharacterClasses
    level: int
    abl_scores: List[int]
    trained_skills: List[Skills]
    trained_saves: List[Abilities]
    armor_class: int
    speed: int
    hit_points: int
    is_dying: bool = False
    inventory: List[Weapon] = field(default_factory=list)
    trained_weapon_types: List[Weapon_types] = field(default_factory=list)
    resistances: List[Damage_types] = field(default_factory=list)
    abl_mods: List[int] = field(init=False)
    initiative: int = field(init=False)
    prof_bonus: int = field(init=False)
    appearance: Optional[Appearance] = None
    personality: Optional[Personality] = None

    def __post_init__(self):
        self.abl_mods = [get_modifier_from_score(self.abl_scores[skill.value]) for skill in Abilities]
        self.initiative = self.abl_scores[Abilities.dexterity.value]
        self.prof_bonus = get_prof_bonus_from_level(self.level)

    def get_ability_mod(self, abl: Abilities):
        return self.abl_mods[abl.value]
    def get_skill_mod(self, skill: Skills):
        mod = self.abl_mods[get_governing_ability(skill).value]
        if skill in self.trained_skills:
            mod += self.prof_bonus
        return mod

    def ability_check(self, abl: Abilities):
        return d20(self.get_ability_mod(abl))
    def skill_check(self, skill: Skills):
        return d20(self.get_skill_mod(skill))

    def _register_appearance(self, app: Appearance):
        self.appearance = app
    def _register_personality(self, pers: Personality):
        self.personality = pers

    def damages_with(self, weapon: Weapon) -> int:
        dmg = weapon.roll_damage() + self.abl_mods[weapon.bonus_mod.value]
        # if weapon.weapon_type in self.trained_weapon_types:
        #     dmg += self.prof_bonus
        return dmg
    def takes_damage(self, damage: int, dmg_type: Damage_types):
        dmg = damage
        # reduce damage if it can be resisted
        if dmg_type in self.resistances:
            dmg = dmg // 2
        # if damage is too great, character is about to die
        if dmg >= self.hit_points:
            self.hit_points = 0
            self.is_dying = True
        else:
            self.hit_points -= dmg


def successful_hit(defender: Character, attacker: Character, weapon: Weapon):
    attack_roll = attacker.ability_check(weapon.bonus_mod)
    if weapon.weapon_type in attacker.trained_weapon_types:
        attack_roll += attacker.prof_bonus
    return attack_roll > defender.armor_class  # TODO: make a "effective AC" function 


def attack(defender: Character, attacker: Character, weapon: Weapon):
    if successful_hit(defender, attacker, weapon):
        weapon_damage = attacker.damages_with(weapon)
        defender.takes_damage(weapon_damage, weapon.damage_type)


if __name__ == "__main__":
    beoran = Character(
        "Beoran", Races.human, CharacterClasses.fighter, 1,
        [15, 12, 14, 13, 10, 8],
        [Skills.atheltics, Skills.history, Skills.perception],
        [Abilities.strength, Abilities.wisdom],
        16, 30, 18
    )
    kerr_grash = Character(
        "Kerr'Grash", Races.dragonborn, CharacterClasses.paladin, 1,
        [15, 8, 13, 12, 10, 14],
        [Skills.religion, Skills.intimidation, Skills.animal_handling],
        [Abilities.charisma, Abilities.intelligence],
        18, 30, 27
    )
    beoran._register_appearance(Appearance(24, 1.85, 98, 
                                           "fair", "brown", "blue"))
    beoran._register_personality(Personality(
        ["Proud"],
        ["Justice"],
        ["Family"],
        ["Hates exploitation"],
    ))

    kerr_grash._register_appearance(Appearance(
        32, 2.15, 137, "metallic red", "brown-red", "piercing yellow"
    ))
    kerr_grash._register_personality(Personality(
        ["Often says 'tsk-tsk-tsk'"],
        ["Law and order"],
        ["Society"],
        ["Quick to anger"],
    ))
    sword = Weapon(
        "sword", Abilities.strength, Roll(1, 6),
        Damage_types.slashing, Weapon_types.simple, 0
    )


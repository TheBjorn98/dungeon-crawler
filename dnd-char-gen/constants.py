from enum import Enum
from dataclasses import dataclass

class Abilities(Enum):
    strength = 0
    dexterity = 1
    constitution = 2
    intelligence = 3
    wisdom = 4
    charisma = 5


class Skills(Enum):
    acrobatics = 0
    animal_handling = 1
    arcana = 2
    atheltics = 3
    deception = 4
    history = 5
    insight = 6
    intimidation = 7
    investigation = 8
    medicine = 9
    nature = 10
    perception = 11
    performance = 12
    persuasion = 13
    religion = 14
    sleight_of_hand = 15
    stealth = 16
    survival = 17


skill_to_ability_map = {
    Skills.acrobatics: Abilities.dexterity,
    Skills.animal_handling: Abilities.wisdom,
    Skills.arcana: Abilities.intelligence,
    Skills.atheltics: Abilities.strength,
    Skills.deception: Abilities.charisma,
    Skills.history: Abilities.intelligence,
    Skills.insight: Abilities.wisdom,
    Skills.intimidation: Abilities.charisma,
    Skills.investigation: Abilities.intelligence,
    Skills.medicine: Abilities.wisdom,
    Skills.nature: Abilities.intelligence,
    Skills.perception: Abilities.wisdom,
    Skills.performance: Abilities.charisma,
    Skills.persuasion: Abilities.charisma,
    Skills.religion: Abilities.intelligence,
    Skills.sleight_of_hand: Abilities.dexterity,
    Skills.stealth: Abilities.dexterity,
    Skills.survival: Abilities.wisdom,
}


def get_governing_ability(skill: Skills):
    return skill_to_ability_map[skill]
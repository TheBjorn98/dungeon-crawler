from random import randint
from dataclasses import dataclass

@dataclass
class Roll:
    num_dices: int
    num_sides: int
    # bias: int

    def roll(self, bias=0):
        return roll_dice(self.num_dices, self.num_sides, bias)


def roll_dice(n_dices, n_sides, bias = 0):
    """Rolls <n_dices> d <n_sides> + <bias>"""
    return sum([randint(1, n_sides) for i in range(n_dices)]) + bias

def d20(bias=0):
    return roll_dice(1, 20, bias)
def dice_count(dice):
    """Count the number of each dice value in the given roll"""
    return {x: dice.count(x) for x in range(1, 6)}


def full_house(dice):
    """Score the given roll in the 'Full House' Yatzi category"""

    counts = dice_count(dice)
    if 2 in counts.values() and 3 in counts.values():
        return sum(dice)
    return 0

if __name__ == '__main__':
    full_house([1, 2, 3, 4, 5])
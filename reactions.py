from ingredients import RECIPES
import random


def get_reaction(ing1, ing2):
    key = (ing1, ing2)
    reverse_key = (ing2, ing1)
    if key in RECIPES:
        return RECIPES[key]
    elif reverse_key in RECIPES:
        return RECIPES[reverse_key]
    else:
        return random.choice(["😐 Неутрално лице", "🤢 Бљак!", "🤔 Што е ова?"])

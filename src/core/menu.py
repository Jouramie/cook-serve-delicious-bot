import enum
from dataclasses import dataclass


class Booster(enum.Enum):
    STAPLE_FOOD = "Staple Food"
    """Will always remain "fresh" on the active menu, and 
    never decline in popularity!"""
    THE_BIG_TIPPER = "The Big Tipper"
    """Customers have a higher chance of leaving a big tip for
     this food with any perfect order (Tip Jar required)."""
    CATERING = "Catering"
    """This is a perfect food for opening up catering
    opportunities when they become available!"""
    RAINY_COMPANION = "Rainy Companion"
    """Makes for a great rainy-day dish! Have this food on
    your active menu during a rainy day for an immediate
    +5% buzz boost (per "Rainy Companon" food)!"""
    LATE_NIGHT_CHOW = "Late Night Chow"
    """Makes for a great late night meal. Have this food on
    your active menu for an immediate +5% buzz boost (per 
    "Late Night Chow" food) in the evenings!"""
    HEALTH_NUTS = "Health Nuts"
    """A healthy food that is somehow not gross. Having two
    of these "Health Nuts" foods on the active menu at
    once results in +5% buzz, with +5% buzz for each 
    additional "Health Nuts" food on the active menu!"""
    THE_COMPETITION = "The Competition"
    """This food is classified as a competition-level food item
    by the famous Iron Cooks. Get good at making this,
    and who knows where that will take you once the time
    is right..."""
    SIMPLY_FOOD = "Simply Food"
    """A generally easy food to make, with only one to five
    recipes and little prep work to do!"""
    TO_GO = "To Go!"
    """A food that is well suited for ordering to-go. Have this
    on your active menu for a +2.5% buzz boost for each
    "To Go!" food (Carry Out service required)."""
    GREEN_TECH = "Green Tech"
    """This food has little to no increased impact on dishes,
     trash or rodents!"""
    VIP_ALLURE = "VIP Allure"
    """This food is known to attract VIPs (once at the
    four star restaurant level or above)."""
    AFTERNOON_DELIGHT = "Afternoon Delight"
    """A great mid-day pick me up, which adds +2.5% buzz per
    "Afternoon Delight" food on the active menu during the
    afternoons hours."""
    BREAKFAST = "Breakfast"
    """This food is a delicious breakfast treat, and adds 5%
    buzz to your early morning hours!"""
    RICH_DISH = "Rich Dish"
    """This food, when paired with restaurants that are four
    stars or higher, is a hit with customers, adding 5% total
    buzz! (It has no buzz effect for three star restaurants
    and below.)"""


class Detractor(enum.Enum):
    MUNCHIES = "Munchies"
    """Generally considered a snack food, and is not ordered
    during Rush Hours. (This does not apply to the Extreme
    Difficulty mode.)"""
    MENU_ROT = "Menu Rot"
    """Will decline in popularity each day it is on the active
    menu, eventually adding negative buzz. Replace it on
    the active menu every two days for maximum
    effectiveness, or your buzz will suffer! Requires one
    day of "rest" to gain back neutral buzz."""
    SLOW_COOKER = "Slow Cooker"
    """This food generally takes a long time to cook before
    you can serve or continue preparations."""
    COMPLEX_BITS = "Complex Bits"
    """Prep work and creating the order is generally much
    more time consuming with this food compared with
    others."""
    UNAPPRECIATED = "Unappreciated"
    """Customers never tip with this food."""
    PEASANT_FOOD = "Peasant Food"
    """This food is never ordered in restaurants classified as
    two star or higher."""
    FATTY_MCFATS = "Fatty McFats"
    """A fatty food frowned upon by weirdos. Having three of
    there "Fatty McFats" foods on the active menu at once
    results in -5% buzz, with -5% buzz for each additional 
    "Fatty McFats" food on the active menu."""
    TRASHY_FOOD = "Trashy Food"
    """This food has a lot of waste byproducts when
    preparing/serving, which leads to an increase in trash
    chores."""
    PLATE_SPINNER = "Plate Spinner"
    """Served on a plate, which increases the amount of times
    necessary todo the dishes during the day."""
    FAST_COOKER = "Fast Cooker"
    """This food cooks extremely quickly, and can easily be 
    burned without some lightning fast reflexes."""
    MORNING_AROMA = "Morning Aroma"
    """There are some foods that are considered unpleasant
    to smell in the mornings by some strange people.
    Results in -5% buzz "Morning Aroma" food on the 
    active menu, but for the morning hours only."""
    AH_RATS = "Ah Rats"
    """Attracts rodents, which increases the amount of traps
    needed to be set during the day."""
    PERFECTION = "Perfection"
    """Customers demand perfection for this food...one
    mistake will automatically make it a bad order. Be
    careful!"""
    WORK_LIQUOR = "Work Liquor"
    """Liquor served in an office tower like this one is
    generally frowned upon for some reason, and results in
    -5% buzz when on the active menu."""


@dataclass
class MenuItem:
    name: str
    prices_per_star: list[int]
    boosters: set[Booster]
    detractors: set[Detractor]

    def get_price_for_unlocks(self, unlocked_food_levels: dict[str, int]) -> int:
        return self.get_price_at_stars(unlocked_food_levels[self.name])

    def get_price_at_stars(self, stars: int) -> int:
        return self.prices_per_star[stars - 1]

    def __eq__(self, other):
        if not isinstance(other, MenuItem):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


def optimize_menu(
    menu_items: list[MenuItem],
    unlocked_food_levels: dict[str, int],
    deactivated_foods: set[str],
    current_stars: int,
    menu_size: int,
) -> dict[MenuItem, int]:
    """Returns a list of the best foods to have on the menu based on the current restaurant stars, deactivated foods, and unlocked food levels."""
    food_choice_and_price: dict[MenuItem, int] = {}
    for item in menu_items:
        if item.name in deactivated_foods:
            continue

        unlocked_stars = unlocked_food_levels[item.name]
        if unlocked_stars == 0:
            continue

        food_choice_and_price[item] = unlocked_stars

    selected_food = sorted(
        food_choice_and_price.items(),
        key=(lambda item_and_stars: item_and_stars[0].get_price_at_stars(item_and_stars[1])),
        reverse=True,
    )[:menu_size]
    return dict(selected_food)

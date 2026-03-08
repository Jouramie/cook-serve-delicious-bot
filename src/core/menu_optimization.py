import enum
import itertools
import math
from dataclasses import dataclass

from ortools.linear_solver.python import model_builder
from ortools.linear_solver.python.model_builder import Model
from ortools.linear_solver.python.model_builder_helper import LinearExpr, Variable

BUZZ_HOURS_WEIGHT = 0.333
PRICE_WEIGHT = 1.0
TIP_WEIGHT = 5.0

UTILITY_SCORE_WEIGHT = 6
PRICE_DIFF_WEIGHT = 1.5
MONEY_LEFT_WEIGHT = 0.01


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
    +5% buzz boost (per "Rainy Companion" food)!"""
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

    @staticmethod
    def meaningful_boosters() -> set["Booster"]:
        return {
            Booster.BREAKFAST,
            Booster.AFTERNOON_DELIGHT,
            Booster.LATE_NIGHT_CHOW,
            Booster.HEALTH_NUTS,
            Booster.TO_GO,
            Booster.THE_BIG_TIPPER,
            Booster.RAINY_COMPANION,
        }

    def __lt__(self, other):
        if not isinstance(other, Booster):
            return NotImplemented
        return self.value < other.value

    def __str__(self):
        return self.value


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

    @staticmethod
    def meaningful_detractors() -> set["Detractor"]:
        return {
            Detractor.MORNING_AROMA,
            Detractor.FATTY_MCFATS,
            Detractor.WORK_LIQUOR,
            Detractor.UNAPPRECIATED,
            Detractor.MUNCHIES,
        }

    def __lt__(self, other):
        if not isinstance(other, Detractor):
            return NotImplemented
        return self.value < other.value

    def __str__(self):
        return self.value


@dataclass
class MenuOption:
    name: str
    prices_per_star: list[int]
    boosters: set[Booster]
    detractors: set[Detractor]

    def get_price_for_unlocks(self, unlocked_food_levels: dict[str, int]) -> int:
        return self.get_price_at_stars(unlocked_food_levels[self.name])

    def get_price_at_stars(self, stars: int) -> int:
        return self.prices_per_star[stars - 1]

    @property
    def morning_buzz(self) -> float:
        if Booster.BREAKFAST in self.boosters:
            return 5.0
        elif Detractor.MORNING_AROMA in self.detractors:
            return -5.0

        return 0.0

    @property
    def afternoon_buzz(self) -> float:
        if Booster.AFTERNOON_DELIGHT in self.boosters:
            return 2.5
        return 0.0

    @property
    def evening_buzz(self) -> float:
        if Booster.LATE_NIGHT_CHOW in self.boosters:
            return 5.0
        return 0.0

    @property
    def is_healthy(self) -> bool:
        return Booster.HEALTH_NUTS in self.boosters

    @property
    def is_to_go(self) -> bool:
        return Booster.TO_GO in self.boosters

    @property
    def is_fatty(self) -> bool:
        return Detractor.FATTY_MCFATS in self.detractors

    @property
    def meaningful_boosters(self) -> list[Booster]:
        return sorted(b for b in self.boosters if b in Booster.meaningful_boosters())

    @property
    def meaningful_distractors(self) -> list[Detractor]:
        return sorted(d for d in self.detractors if d in Detractor.meaningful_detractors())

    @property
    def utility_score(self) -> float:
        return len(self.meaningful_boosters) - len(self.meaningful_distractors)

    def __eq__(self, other):
        if not isinstance(other, MenuOption):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


@dataclass
class UnlockedMenuOption:
    menu_option: MenuOption
    stars: int
    is_menu_rot: bool = False

    @property
    def name(self):
        return self.menu_option.name

    @property
    def price(self):
        if self.stars == 0:
            return 0

        return self.menu_option.get_price_at_stars(self.stars)

    @property
    def next_star_price(self):
        return self.menu_option.get_price_at_stars(self.stars + 1)

    @property
    def morning_buzz(self) -> float:
        return self.menu_option.morning_buzz

    @property
    def afternoon_buzz(self) -> float:
        return self.menu_option.afternoon_buzz

    @property
    def evening_buzz(self) -> float:
        return self.menu_option.evening_buzz

    @property
    def is_healthy(self) -> bool:
        return self.menu_option.is_healthy

    @property
    def is_to_go(self) -> bool:
        return self.menu_option.is_to_go

    @property
    def is_fatty(self) -> bool:
        return self.menu_option.is_fatty

    @property
    def boosters(self) -> set[Booster]:
        return self.menu_option.boosters

    @property
    def detractors(self) -> set[Detractor]:
        return self.menu_option.detractors

    def __str__(self):
        boosters = ", ".join(str(b) for b in self.menu_option.meaningful_boosters)
        detractors = ", ".join(str(b) for b in self.menu_option.meaningful_distractors)
        return (
            f"{self.menu_option.name}: ${self.price} [{boosters}]"
            + (f" [{detractors}]" if detractors else "")
            + (" !MENU ROT!" if self.is_menu_rot else "")
        )


@dataclass
class PurchaseOption:
    unlocked_menu_option: UnlockedMenuOption
    unlock_price: int

    @property
    def name(self):
        return self.unlocked_menu_option.name

    @property
    def is_healthy(self) -> bool:
        return self.unlocked_menu_option.is_healthy

    @property
    def is_to_go(self) -> bool:
        return self.unlocked_menu_option.is_to_go

    @property
    def is_fatty(self) -> bool:
        return self.unlocked_menu_option.is_fatty

    @property
    def morning_buzz(self) -> float:
        return self.unlocked_menu_option.morning_buzz

    @property
    def afternoon_buzz(self) -> float:
        return self.unlocked_menu_option.afternoon_buzz

    @property
    def evening_buzz(self) -> float:
        return self.unlocked_menu_option.evening_buzz

    @property
    def is_menu_rot(self) -> bool:
        return self.unlocked_menu_option.is_menu_rot

    @property
    def boosters(self) -> set[Booster]:
        return self.unlocked_menu_option.boosters

    @property
    def detractors(self) -> set[Detractor]:
        return self.unlocked_menu_option.detractors

    @property
    def utility_score(self):
        return self.unlocked_menu_option.menu_option.utility_score

    @property
    def food_price(self):
        return self.unlocked_menu_option.price

    @property
    def upgraded_food_price(self):
        return self.unlocked_menu_option.next_star_price

    @property
    def food_price_difference(self):
        return self.unlocked_menu_option.next_star_price - self.unlocked_menu_option.price

    @property
    def value_per_dollar(self):
        if self.unlock_price == 0:
            return math.inf
        return (
            self.utility_score * UTILITY_SCORE_WEIGHT + self.food_price_difference * PRICE_DIFF_WEIGHT
        ) / self.unlock_price

    def __str__(self):
        boosters = ", ".join(str(b) for b in self.unlocked_menu_option.menu_option.meaningful_boosters)
        detractors = ", ".join(str(b) for b in self.unlocked_menu_option.menu_option.meaningful_distractors)
        return (
            f"!UPGRADE! {self.name}: ${self.upgraded_food_price} [{boosters}]"
            + (f" [{detractors}]" if detractors else "")
            + (" !MENU ROT!" if self.unlocked_menu_option.is_menu_rot else "")
        )


@dataclass
class OptimizedMenu:
    unlocked_food: list[UnlockedMenuOption]
    to_purchase_food: list[PurchaseOption]

    @property
    def all_food(self) -> list[UnlockedMenuOption | PurchaseOption]:
        return self.unlocked_food + self.to_purchase_food

    @property
    def healthy_buzz(self) -> float:
        return max(0, sum(5 for food in self.all_food if food.is_healthy) - 5)

    @property
    def to_go_buzz(self) -> float:
        return sum(2.5 for food in self.all_food if food.is_to_go)

    @property
    def fatty_buzz(self) -> float:
        return min(0, sum(-5 for food in self.all_food if food.is_fatty) + 10)

    @property
    def all_day_buzz(self) -> float:
        liquor_buzz = sum(-5 for food in self.all_food if Detractor.WORK_LIQUOR in food.detractors)
        rot_buzz = sum(-5 for food in self.all_food if food.is_menu_rot)
        return self.healthy_buzz + self.to_go_buzz + self.fatty_buzz + liquor_buzz + rot_buzz

    @property
    def morning_buzz(self) -> float:
        return sum(food.morning_buzz for food in self.all_food) + self.all_day_buzz

    @property
    def afternoon_buzz(self) -> float:
        return sum(food.afternoon_buzz for food in self.all_food) + self.all_day_buzz

    @property
    def evening_buzz(self) -> float:
        return sum(food.evening_buzz for food in self.all_food) + self.all_day_buzz

    @property
    def rain_buzz(self) -> float:
        return sum(Booster.RAINY_COMPANION in food.boosters for food in self.all_food) * 5

    @property
    def total_price(self) -> int:
        current_food_price = sum(option.price for option in self.unlocked_food)
        to_upgrade_food_price = sum(option.upgraded_food_price for option in self.to_purchase_food)
        return current_food_price + to_upgrade_food_price

    def __str__(self):
        return f"""
Chosen menu:
  - {(chr(10)+'  - ').join(str(option) for option in self.all_food)}
  
Total price: ${self.total_price}
Buzz: {self.morning_buzz}% Morning | {self.afternoon_buzz}% Afternoon | {self.evening_buzz}% Evening ({self.all_day_buzz}% Permanent) {self.rain_buzz}% Rain
Budget used: ${sum(option.unlock_price for option in self.to_purchase_food)}
"""


def choose_best_menu(
    menu_items: dict[str, MenuOption],
    unlocked_food_levels: dict[str, int],
    current_stars: int,
    menu_rot: list[str],
    mandatory_food: list[str],
    raining_hours: int,
    available_purchases: dict[str, int],
    budget: int,
) -> OptimizedMenu:
    unlocked_food = _create_unlocked_food(menu_items, unlocked_food_levels, current_stars, menu_rot)
    purchasable_food = _create_purchasable_food(available_purchases, menu_items, unlocked_food_levels)

    model = model_builder.Model()

    is_using_unlocked_foods = {name: model.new_bool_var(name=name) for name, food in unlocked_food.items()}
    is_using_purchasable_foods = {name: model.new_bool_var(name=name) for name, food in purchasable_food.items()}

    model.add_linear_constraint(
        sum(itertools.chain(is_using_unlocked_foods.values(), is_using_purchasable_foods.values())), lb=3, ub=6
    )

    model.add_linear_constraint(
        sum(
            is_using_purchasable_food * purchasable_food[name].unlock_price
            for name, is_using_purchasable_food in is_using_purchasable_foods.items()
        ),
        ub=budget,
    )

    is_using_foods: dict[str, LinearExpr | Variable] = {}
    for name, is_using_unlocked_food in is_using_unlocked_foods.items():
        try:
            is_using_purchasable_food = is_using_purchasable_foods[name]
            is_using_food = is_using_unlocked_food + is_using_purchasable_food
            is_using_foods[name] = is_using_food

            model.add_linear_constraint(is_using_food, lb=0, ub=1)

        except KeyError:
            is_using_foods[name] = is_using_unlocked_food

    for name, is_using_purchasable_food in is_using_purchasable_foods.items():
        if name in is_using_foods:
            continue

        is_using_foods[name] = is_using_purchasable_food

    for name, is_using_food in is_using_foods.items():
        if name in mandatory_food:
            model.add_linear_constraint(is_using_food, lb=1, ub=1)

    menu_price = sum(
        is_using_unlocked_food * unlocked_food[name].price
        for name, is_using_unlocked_food in is_using_unlocked_foods.items()
    )
    menu_price += sum(
        is_using_purchasable_food * purchasable_food[name].upgraded_food_price
        for name, is_using_purchasable_food in is_using_purchasable_foods.items()
    )

    buzz_hours = _build_buzz_equation(model, is_using_foods, menu_items, menu_rot, raining_hours)
    tip_bonus = _build_tip_equation(is_using_foods, menu_items)

    model.maximize(buzz_hours * BUZZ_HOURS_WEIGHT + menu_price * PRICE_WEIGHT + tip_bonus * TIP_WEIGHT)

    solver = model_builder.ModelSolver("sat")
    status = solver.solve(model)

    if status != model_builder.SolveStatus.OPTIMAL:
        print("Could not find an optimal menu, but will return something anyway.")

    print(
        f"Optimal menu has a score of {solver.objective_value}.\n"
        f"Price score = {solver.value(menu_price)} * {PRICE_WEIGHT} = {solver.value(menu_price)*PRICE_WEIGHT}\n"
        f"Buzz hours score = {solver.value(buzz_hours)} * {BUZZ_HOURS_WEIGHT} = {solver.value(buzz_hours)*BUZZ_HOURS_WEIGHT}\n"
        f"Tip score = {solver.value(tip_bonus)} * {TIP_WEIGHT} = {solver.value(tip_bonus)*TIP_WEIGHT}\n"
    )

    return OptimizedMenu(
        [
            unlocked_food[name]
            for name, is_using_unlocked_food in is_using_unlocked_foods.items()
            if solver.value(is_using_unlocked_food) == 1
        ],
        [
            purchasable_food[name]
            for name, is_using_purchasable_food in is_using_purchasable_foods.items()
            if solver.value(is_using_purchasable_food) == 1
        ],
    )


def _create_unlocked_food(
    menu_items: dict[str, MenuOption],
    unlocked_food_levels: dict[str, int],
    current_stars: int = 0,
    menu_rot: list[str] | None = None,
    filter_unpurchased: bool = True,
) -> dict[str, UnlockedMenuOption]:
    if menu_rot is None:
        menu_rot = []

    unlocked_food: dict[str, UnlockedMenuOption] = {}
    for name, food in menu_items.items():
        if current_stars >= 2 and Detractor.PEASANT_FOOD in food.detractors:
            continue

        unlocked_stars = unlocked_food_levels[name]
        if filter_unpurchased and unlocked_stars == 0:
            continue

        unlocked_food[name] = UnlockedMenuOption(food, unlocked_stars, is_menu_rot=(name in menu_rot))

    return unlocked_food


def _create_purchasable_food(
    available_purchases: dict[str, int],
    menu_items: dict[str, MenuOption],
    unlocked_food_levels: dict[str, int],
    current_stars: int = 0,
    menu_rot: list[str] | None = None,
) -> dict[str, PurchaseOption]:
    unlocked_items_by_name = _create_unlocked_food(
        menu_items, unlocked_food_levels, current_stars, menu_rot, filter_unpurchased=False
    )
    return {
        purchase: PurchaseOption(unlocked_items_by_name[purchase], price)
        for purchase, price in available_purchases.items()
    }


def _build_buzz_equation(
    model: Model,
    is_using_foods: dict[str, LinearExpr | Variable],
    menu_items: dict[str, MenuOption],
    menu_rot: list[str],
    raining_hours: int,
) -> LinearExpr | Variable:
    morning_buzz = sum(
        is_using_food * menu_items[name].morning_buzz
        for name, is_using_food in is_using_foods.items()
        if menu_items[name].morning_buzz != 0
    )

    afternoon_buzz = sum(
        is_using_food * menu_items[name].afternoon_buzz
        for name, is_using_food in is_using_foods.items()
        if menu_items[name].afternoon_buzz != 0
    )

    evening_buzz = sum(
        is_using_food * menu_items[name].evening_buzz
        for name, is_using_food in is_using_foods.items()
        if menu_items[name].evening_buzz != 0
    )

    # The model does not allow less than 1 healthy food. That's probably fine since it tries to maximize the amount of
    # healthy food anyway.
    sum_healthy = sum(is_using_food for name, is_using_food in is_using_foods.items() if menu_items[name].is_healthy)
    healthy_bonus = model.new_num_var(lb=0, ub=math.inf, name="healthy_bonus")
    model.add_linear_constraint(healthy_bonus - sum_healthy + 1, ub=0)
    healthy_buzz = healthy_bonus * 5.0

    sum_fatty = sum(is_using_food for name, is_using_food in is_using_foods.items() if menu_items[name].is_fatty)
    fatty_bonus = model.new_num_var(lb=0, ub=math.inf, name="fatty_bonus")
    model.add_linear_constraint(fatty_bonus - sum_fatty + 2, lb=0)
    fatty_buzz = fatty_bonus * -5.0

    to_go_buzz = sum(is_using_food for name, is_using_food in is_using_foods.items() if menu_items[name].is_to_go) * 2.5

    liquor_buzz = (
        sum(
            is_using_food
            for name, is_using_food in is_using_foods.items()
            if Detractor.WORK_LIQUOR in menu_items[name].detractors
        )
        * -5.0
    )

    menu_rot_buzz = sum(is_using_food for name, is_using_food in is_using_foods.items() if name in menu_rot) * -5.0

    day_long_buzz = healthy_buzz + fatty_buzz + to_go_buzz + liquor_buzz + menu_rot_buzz

    raining_buzz = (
        sum(
            is_using_food
            for name, is_using_food in is_using_foods.items()
            if Booster.RAINY_COMPANION in menu_items[name].boosters
        )
        * 5.0
    )

    # Restaurant is opened from 9 am to 10 pm.
    # Rush hours are from 12 pm to 1 pm and from 6 pm to 7 pm.
    # Morning buzz is 3 hours long, from 9 am to 12 pm.
    # Afternoon buzz is 5 hours long, from 1 pm to 6 pm.
    # Evening buzz is 3 hours long, from 7 pm to 10 pm.

    return morning_buzz * 3 + afternoon_buzz * 5 + evening_buzz * 3 + day_long_buzz * 11 + raining_buzz * raining_hours


def _build_tip_equation(
    is_using_foods: dict[str, LinearExpr | Variable], menu_items: dict[str, MenuOption]
) -> LinearExpr | int:
    tip_boosted = sum(
        is_using_food
        for name, is_using_food in is_using_foods.items()
        if Booster.THE_BIG_TIPPER in menu_items[name].boosters
    )

    tip_detracted = sum(
        is_using_food
        for name, is_using_food in is_using_foods.items()
        if Detractor.UNAPPRECIATED in menu_items[name].detractors
    )

    return tip_boosted - tip_detracted

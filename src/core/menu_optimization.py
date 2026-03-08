import enum
import math
from dataclasses import dataclass

from ortools.linear_solver.python import model_builder
from ortools.linear_solver.python.model_builder import Model
from ortools.linear_solver.python.model_builder_helper import LinearExpr, Variable

BUZZ_HOURS_WEIGHT = 1.0
PRICE_WEIGHT = 1.5
TIP_WEIGHT = 3.0

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
        return Booster.HEALTH_NUTS in self.menu_option.boosters

    @property
    def is_to_go(self) -> bool:
        return Booster.TO_GO in self.menu_option.boosters

    @property
    def is_fatty(self) -> bool:
        return Detractor.FATTY_MCFATS in self.menu_option.detractors

    def __str__(self):
        boosters = ", ".join(str(b) for b in self.menu_option.meaningful_boosters)
        detractors = ", ".join(str(b) for b in self.menu_option.meaningful_distractors)
        return (
            f"{self.menu_option.name}: ${self.price} [{boosters}]"
            + (f" [{detractors}]" if detractors else "")
            + (" !MENU ROT!" if self.is_menu_rot else "")
        )


@dataclass
class OptimizedMenu:
    menu_options: list[UnlockedMenuOption]

    @property
    def healthy_buzz(self) -> float:
        return sum(5.0 for option in self.menu_options if option.is_healthy)

    @property
    def to_go_buzz(self) -> float:
        return sum(2.5 for option in self.menu_options if option.is_to_go)

    @property
    def fatty_buzz(self) -> float:
        return sum(-5.0 for option in self.menu_options if option.is_fatty)

    @property
    def all_day_buzz(self) -> float:
        return self.healthy_buzz + self.fatty_buzz

    @property
    def morning_buzz(self) -> float:
        return sum(option.morning_buzz for option in self.menu_options) + self.all_day_buzz

    @property
    def afternoon_buzz(self) -> float:
        return sum(option.afternoon_buzz for option in self.menu_options) + self.all_day_buzz

    @property
    def evening_buzz(self) -> float:
        return sum(option.evening_buzz for option in self.menu_options) + self.all_day_buzz

    @property
    def total_price(self) -> int:
        return sum(option.price for option in self.menu_options)

    def __str__(self):
        return f"""
Chosen menu:
  - {(chr(10)+'  - ').join(str(option) for option in self.menu_options)}
Total price: ${self.total_price}
Morning buzz: {self.morning_buzz}%
Afternoon buzz: {self.afternoon_buzz}%
Evening buzz: {self.evening_buzz}%
Permanent buzz: {self.healthy_buzz + self.to_go_buzz}%
"""


def choose_best_menu(
    menu_items: list[MenuOption],
    unlocked_food_levels: dict[str, int],
    current_stars: int,
    menu_rot: list[str],
    mandatory_food: list[str],
) -> OptimizedMenu:
    unlocked_food = _create_unlocked_food(menu_items, unlocked_food_levels, current_stars, menu_rot)

    model = model_builder.Model()

    food_enabled = _build_food_variables(model, unlocked_food, mandatory_food)

    menu_price = sum(food_enabled[i] * food.price for i, food in enumerate(unlocked_food))
    buzz_hours = _build_buzz_equation(model, food_enabled, unlocked_food)
    tip_bonus = _build_tip_equation(food_enabled, unlocked_food)

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

    return OptimizedMenu([food for i, food in enumerate(unlocked_food) if solver.value(food_enabled[i]) == 1])


@dataclass
class PurchaseOption:
    unlocked_menu_option: UnlockedMenuOption
    purchase_price: int

    @property
    def name(self):
        return self.unlocked_menu_option.name

    @property
    def utility_score(self):
        return self.unlocked_menu_option.menu_option.utility_score

    @property
    def food_price(self):
        return self.unlocked_menu_option.price

    @property
    def next_food_price(self):
        return self.unlocked_menu_option.next_star_price

    @property
    def food_price_difference(self):
        return self.unlocked_menu_option.next_star_price - self.unlocked_menu_option.price

    @property
    def value_per_dollar(self):
        if self.purchase_price == 0:
            return math.inf
        return (
            self.utility_score * UTILITY_SCORE_WEIGHT + self.food_price_difference * PRICE_DIFF_WEIGHT
        ) / self.purchase_price

    def __str__(self):
        return f"{self.name}: ${self.purchase_price}, Utility: {self.utility_score}, ${self.food_price} -> ${self.next_food_price} ({self.value_per_dollar:.4f})"


def advise_purchases(
    menu_items: list[MenuOption], budget: int, available_purchases: dict[str, int], unlocked_food_levels: dict[str, int]
) -> list[str]:

    unlocked_items = _create_unlocked_food(menu_items, unlocked_food_levels, filter_unpurchased=False)
    unlocked_items_by_name = {item.name: item for item in unlocked_items}
    purchase_options = [
        PurchaseOption(unlocked_items_by_name[purchase], price) for purchase, price in available_purchases.items()
    ]

    model = model_builder.Model()

    is_purchased = [model.new_bool_var(name=purchase.name) for purchase in purchase_options]
    model.add_linear_constraint(
        sum(purchase.purchase_price * is_purchased[i] for i, purchase in enumerate(purchase_options)),
        ub=budget,
    )

    purchase_utility_score = sum(
        is_purchased[i] * purchase.utility_score for i, purchase in enumerate(purchase_options)
    )

    price_increase = sum(
        is_purchased[i] * purchase.food_price_difference for i, purchase in enumerate(purchase_options)
    )

    money_left = budget - sum(is_purchased[i] * purchase.purchase_price for i, purchase in enumerate(purchase_options))

    model.maximize(
        purchase_utility_score * UTILITY_SCORE_WEIGHT
        + price_increase * PRICE_DIFF_WEIGHT
        + money_left * MONEY_LEFT_WEIGHT
    )

    solver = model_builder.ModelSolver("sat")
    status = solver.solve(model)

    if status != model_builder.SolveStatus.OPTIMAL:
        print("Could not find an optimal solution, but will return something anyway.")

    print(
        f"Optimal purchases has a score of {solver.objective_value}.\n"
        f"Utility score = {solver.value(purchase_utility_score)} * {UTILITY_SCORE_WEIGHT} = {solver.value(purchase_utility_score) * UTILITY_SCORE_WEIGHT}\n"
        f"Price increase score = {solver.value(price_increase)} * {PRICE_DIFF_WEIGHT} = {solver.value(price_increase) * PRICE_DIFF_WEIGHT}\n"
        f"Money left score = {solver.value(money_left)} * {MONEY_LEFT_WEIGHT} = {solver.value(money_left) * MONEY_LEFT_WEIGHT}\n"
    )

    optimal_purchases = []
    for i, purchase in enumerate(purchase_options):
        if solver.value(is_purchased[i]) == 1:
            print(purchase)
            optimal_purchases.append(purchase)

    print(f"Total spent: ${sum(purchase.purchase_price for purchase in optimal_purchases)}\n")
    return [purchase.name for purchase in optimal_purchases]


def _create_unlocked_food(
    menu_items: list[MenuOption],
    unlocked_food_levels: dict[str, int],
    current_stars: int = 0,
    menu_rot: list[str] | None = None,
    filter_unpurchased: bool = True,
) -> list[UnlockedMenuOption]:
    if menu_rot is None:
        menu_rot = []

    unlocked_food: list[UnlockedMenuOption] = []
    for menu_option in menu_items:
        if current_stars >= 2 and Detractor.PEASANT_FOOD in menu_option.detractors:
            continue

        unlocked_stars = unlocked_food_levels[menu_option.name]
        if filter_unpurchased and unlocked_stars == 0:
            continue

        unlocked_food.append(
            UnlockedMenuOption(menu_option, unlocked_stars, is_menu_rot=(menu_option.name in menu_rot))
        )
    return unlocked_food


def _build_buzz_equation(
    model: Model, food_enabled: list[Variable], unlocked_food: list[UnlockedMenuOption]
) -> LinearExpr | Variable:
    morning_buzz = sum(
        food_enabled[i] * item.morning_buzz for i, item in enumerate(unlocked_food) if item.morning_buzz != 0
    )

    afternoon_buzz = sum(
        food_enabled[i] * item.afternoon_buzz for i, item in enumerate(unlocked_food) if item.afternoon_buzz != 0
    )

    evening_buzz = sum(
        food_enabled[i] * item.evening_buzz for i, item in enumerate(unlocked_food) if item.evening_buzz != 0
    )

    # The model does not allow less than 1 healthy food. That's probably fine since it tries to maximize the amount of
    # healthy food anyway.
    sum_healthy = sum(food_enabled[i] for i, item in enumerate(unlocked_food) if item.is_healthy)
    healthy_bonus = model.new_num_var(lb=0, ub=math.inf, name="healthy_bonus")
    model.add_linear_constraint(healthy_bonus - sum_healthy + 1, ub=0)
    healthy_buzz = healthy_bonus * 5.0

    sum_fatty = sum(food_enabled[i] for i, item in enumerate(unlocked_food) if item.is_fatty)
    fatty_bonus = model.new_num_var(lb=0, ub=math.inf, name="fatty_bonus")
    model.add_linear_constraint(fatty_bonus - sum_fatty + 2, lb=0)
    fatty_buzz = fatty_bonus * -5.0

    to_go_buzz = (
        sum(food_enabled[i] for i, item in enumerate(unlocked_food) if Booster.TO_GO in item.menu_option.boosters) * 2.5
    )

    liquor_buzz = (
        sum(
            food_enabled[i]
            for i, item in enumerate(unlocked_food)
            if Detractor.WORK_LIQUOR in item.menu_option.detractors
        )
        * -5.0
    )

    menu_rot_buzz = sum(food_enabled[i] for i, item in enumerate(unlocked_food) if item.is_menu_rot) * -5.0

    day_long_buzz = healthy_buzz + fatty_buzz + to_go_buzz + liquor_buzz + menu_rot_buzz

    # Restaurant is opened from 9 am to 10 pm.
    # Rush hours are from 12 pm to 1 pm and from 6 pm to 7 pm.
    # Morning buzz is 3 hours long, from 9 am to 12 pm.
    # Afternoon buzz is 6 hours long, from 1 pm to 7 pm.
    # Evening buzz is 3 hours long, from 7 pm to 10 pm.

    buzz_hours = morning_buzz + afternoon_buzz * 2 + evening_buzz + day_long_buzz * 4
    return buzz_hours


def _build_tip_equation(food_enabled: list[Variable], unlocked_food: list[UnlockedMenuOption]) -> LinearExpr | int:
    tip_boosted = sum(
        food_enabled[i] for i, item in enumerate(unlocked_food) if Booster.THE_BIG_TIPPER in item.menu_option.boosters
    )

    tip_detracted = sum(
        food_enabled[i]
        for i, item in enumerate(unlocked_food)
        if Detractor.UNAPPRECIATED in item.menu_option.detractors
    )

    tip_bonus = tip_boosted + tip_detracted
    return tip_bonus


def _build_food_variables(
    model: Model, unlocked_food: list[UnlockedMenuOption], mandatory_food: list[str]
) -> list[Variable]:
    food_enabled = [model.new_bool_var(name=food.name) for food in unlocked_food]
    model.add_linear_constraint(sum(food_enabled), lb=3, ub=6)
    for i, food in enumerate(unlocked_food):
        if food.name in mandatory_food:
            model.add_linear_constraint(food_enabled[i], lb=1, ub=1)
    return food_enabled

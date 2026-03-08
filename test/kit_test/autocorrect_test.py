from unittest import skip

from botkit.text import autocorrect
from core import brain


def test_tombo_jumbo():
    text = 'A"Tombo Cola with Ice, please.'
    dictionary = set(brain.EQUIPMENTS["Soda Fountain"].steps[0].autocorrect_dictionary)
    expected = "a jumbo cola with ice please"

    corrected = autocorrect(text, dictionary)

    assert corrected == expected


def test_cherry_vanilla():
    text = "Two Vanilla Scoops with a Cherry, please."
    dictionary = set(brain.EQUIPMENTS["Ice Cream"].steps[0].autocorrect_dictionary)
    expected = "two vanilla scoops with cherry please"

    corrected = autocorrect(text, dictionary)

    assert corrected == expected


@skip("Onions is too far from Onidhy in terms of edit distance.")
def test_olives_and_onions_pizza():
    text = "Tomato Sauce, Cheese, Olives and Onidhy"
    dictionary = set(brain.EQUIPMENTS["Pizza"].steps[0].autocorrect_dictionary)
    expected = "tomato sauce cheese olives and onions"

    corrected = autocorrect(text, dictionary)

    assert corrected == expected

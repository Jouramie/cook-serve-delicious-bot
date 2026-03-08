import logging

import pytest

import suite_utils
from botkit.text import autocorrect
from core import brain

suite_utils.enable_stdout_logs(logging.DEBUG)


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


@pytest.mark.skip(reason="Onions is too far from Onidhy in terms of edit distance.")
def test_olives_and_onions_pizza():
    text = "Tomato Sauce, Cheese, Olives and Onidhy"
    dictionary = set(brain.EQUIPMENTS["Pizza"].steps[0].autocorrect_dictionary)
    expected = "tomato sauce cheese olives and onions"

    corrected = autocorrect(text, dictionary)

    assert corrected == expected


def test_bacon_extra_brocoli_salad():
    text = "Vinaigrette, Cheese, � zon and Croutons."
    dictionary = set(brain.EQUIPMENTS["Salad"].steps[0].autocorrect_dictionary)
    expected = "vinaigrette cheese bacon and croutons"

    corrected = autocorrect(text, dictionary)

    assert corrected == expected

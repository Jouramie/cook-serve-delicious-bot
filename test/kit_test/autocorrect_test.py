from core import brain
from kit.text import autocorrect


def test_tombo_jumbo():
    text = 'A"Tombo Cola with Ice, please.'
    dictionary = set(brain.EQUIPMENTS["Soda Fountain"].steps[0].autocorrect_dictionary)
    expected = "a jumbo cola with ice please"

    corrected = autocorrect(text, dictionary)

    assert corrected == expected


def test_cherry_vanilla():
    text = "Two Vanilla Scoops with a Cherry, please."
    dictionary = set(brain.EQUIPMENTS["Ice Cream"].steps[0].autocorrect_dictionary)
    expected = "two vanilla scoops with a cherry please"

    corrected = autocorrect(text, dictionary)

    assert corrected == expected

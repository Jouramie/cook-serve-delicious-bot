import logging
from collections.abc import Iterable
from functools import reduce

import inflect
import jellyfish

logger = logging.getLogger(__name__)

punctuation_to_remove = ['"', "'", ",", "."]
p = inflect.engine()


def create_dictionary_from_text(texts: Iterable[str]) -> set[str]:
    """
    Create a set of words from the given text, removing duplicates and normalizing case.
    :param texts: Iterable of text strings to create the dictionary from.
    :return: A set of unique words in lowercase.
    """
    words = set()
    for text in texts:
        text = normalize_text(text)
        for word in text.split():
            words.add(word)
            words.add(p.plural(word))
    return words


def autocorrect(text: str, dictionary: set[str]) -> str:
    """
    Autocorrect the given text using the provided dictionary.
    :param text: Text to autocorrect. Expected to be a single line of text.
    :param dictionary: Words dictionary to use for autocorrection. Expected to be single words only, lowercase.
    :return: The corrected text stripped from punctuation, in lowercase.
    """
    text = normalize_text(text)

    corrected_text = text
    words = text.split()
    for word in words:
        if word and word not in dictionary:
            # Find the closest word in the dictionary
            closest_word, distance = min(
                (
                    (candidate, jellyfish.damerau_levenshtein_distance(word.lower(), candidate))
                    for candidate in dictionary
                ),
                key=lambda x: x[1],
            )

            if (normalized_distance := 1 - (distance / max(len(word), len(closest_word)))) >= 0.6:
                logger.debug(f"Replacing '{word}' with '{closest_word}'")
                corrected_text = corrected_text.replace(word, closest_word)
            else:
                logger.debug(
                    f"Keeping '{word}' as is, distance from '{closest_word}' is too high: {normalized_distance:.2f}"
                )

    logger.info(f"Autocorrected text: {corrected_text}")
    return corrected_text


def normalize_text(text: str) -> str:
    """
    Normalize the text by removing punctuation and extra spaces.
    :param text: Text to normalize.
    :return: The normalized text.
    """
    text = text.lower()
    text = reduce(lambda x, c: x.replace(c, " "), punctuation_to_remove, text).strip()
    while (updated := text.replace("  ", " ")) != text:
        text = updated
    return text

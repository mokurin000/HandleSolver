INITIAL_SIGN = [
    "b",
    "p",
    "m",
    "f",
    "d",
    "t",
    "z",
    "c",
    "s",
    "n",
    "l",
    "zh",
    "ch",
    "sh",
    "r",
    "j",
    "q",
    "x",
    "g",
    "k",
    "h",
    "y",
    "w",
]
INITIAL_SIGN.sort(key=lambda s: len(s), reverse=True)

VOWEL_SIGN = [
    "a",
    "o",
    "e",
    "i",
    "u",
    "v",
    "ai",
    "ei",
    "ui",
    "ao",
    "ou",
    "iu",
    "ie",
    "ve",
    "er",
    "an",
    "en",
    "in",
    "un",
    "vn",
    "ang",
    "eng",
    "ing",
    "ong",
]
VOWEL_SIGN.sort(key=lambda s: len(s), reverse=True)

PRENUCLEAR_GLIDE = ["i", "u", "v"]

STANDALONE = ["er"]

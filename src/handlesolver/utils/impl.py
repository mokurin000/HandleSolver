import unicodedata
from string import ascii_letters

from handlesolver.utils.exception import PinyinException
from handlesolver.utils.const import (
    INITIAL_SIGN,
    VOWEL_SIGN,
    PRENUCLEAR_GLIDE,
    STANDALONE,
)


def split_pinyin(pinyin: str) -> dict[str, str | None]:
    _pinyin = pinyin

    add_comma = False
    if pinyin.endswith(","):
        add_comma = True
        pinyin = pinyin.removesuffix(",")

    if pinyin in STANDALONE or pinyin in VOWEL_SIGN:
        return (None, None, pinyin)

    initial = None
    for sign in INITIAL_SIGN:
        if pinyin.startswith(sign):
            initial = sign
            pinyin = pinyin.removeprefix(sign)
            break
    else:
        raise PinyinException(f"Unknown initial for pinyin {_pinyin}")

    vowel = None
    for sign in VOWEL_SIGN:
        if pinyin.endswith(sign):
            vowel = sign
            pinyin = pinyin.removesuffix(sign)
            break
    else:
        raise PinyinException(f"Unknown vowel for pinyin {_pinyin}")

    prenuclear = None
    if pinyin:
        if pinyin in PRENUCLEAR_GLIDE:
            prenuclear = pinyin
        else:
            raise PinyinException(
                f"Unknown prenuclear {prenuclear} for pinyin {_pinyin}"
            )

    if add_comma:
        vowel += ","

    return {
        "initial": initial,
        "prenuclear": prenuclear,
        "vowel": vowel,
    }


def rec_pinyin(pinyin: str) -> dict[str, int | dict[str, str | None]]:
    result = ""
    pinyin_level = None
    for c in pinyin:
        if c in ascii_letters + ",":
            result += c.lower()
        elif not c.isalpha():
            continue
        else:
            name = unicodedata.name(c)
            info = name.removeprefix("LATIN SMALL LETTER ")

            if info.startswith("SCRIPT "):
                alpha = info.split()[-1].lower()
                result += alpha.lower()
                continue

            try:
                alpha, detail = info.split(" WITH ")
            except ValueError:
                print(name)
                raise PinyinException(f"Failed to process {c} in {pinyin}")
            for word in detail.split(" AND "):
                match word:
                    case "MACRON":
                        pinyin_level = 1
                    case "ACUTE":
                        pinyin_level = 2
                    case "CARON":
                        pinyin_level = 3
                    case "GRAVE":
                        pinyin_level = 4
                    case "DIAERESIS":
                        pinyin_level = 4
                        alpha = "v"
                    case _:
                        raise PinyinException(f"Unknown detail {detail} of {c}")

                result += alpha.lower()
    result = {
        "level": pinyin_level,
        "parts": split_pinyin(result),
    }
    return result


def clean_entry(entry: dict[str, str]):
    input_pinyin = entry["pinyin"].replace("，", ", ").replace(",", ", ").split()
    try:
        pinyin = list(map(rec_pinyin, input_pinyin))
    except PinyinException as e:
        print("failed to process entry:", e)
        print(f"word: {entry['word']}, pinyin: {entry['pinyin']}")
        return None

    return {"word": entry["word"], "pinyin": pinyin}

import json
from functools import partial
from collections.abc import Callable


def match_remain_pinyin(index: int, remain: str) -> Callable[[dict], bool]:
    def is_match(index: int, remain: str, entry: dict):
        pren = entry["pinyin"][index]["parts"]["prenuclear"] or ""
        vowel = entry["pinyin"][index]["parts"]["vowel"]
        return pren + vowel == remain

    return partial(is_match, index, remain)


def match_initial_pinyin(index: int, initial: str) -> Callable[[dict], bool]:
    def is_match(index: int, initial: str, entry: dict):
        return entry["pinyin"][index]["parts"]["initial"] == initial

    return partial(is_match, index, initial)


def match_pinyin_level(index: int, level: int) -> Callable[[dict], bool]:
    def is_match(index: int, level: int, entry: dict):
        return entry["pinyin"][index]["level"] == level

    return partial(is_match, index, level)


def main():
    with open("idiom_clean.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    length = 4
    known_parts = [(None, None)] * length
    known_level = [None, None, None, 1]

    filtered = filter(lambda e: len(e["word"]) == 4, data)

    for ind, (initial, remain) in enumerate(known_parts):
        match initial, remain:
            case None, None:
                continue
            case _, None:
                filtered = filter(match_initial_pinyin(ind, initial), filtered)
            case None, _:
                filtered = filter(match_remain_pinyin(ind, remain), filtered)

    for ind, level in enumerate(known_level):
        if level is None:
            continue
        filtered = filter(match_pinyin_level(ind, level), filtered)

    print(*map(lambda e: e["word"], filtered), sep="\n")


if __name__ == "__main__":
    main()

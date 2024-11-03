import json

from handlesolver.utils.impl import clean_entry


def main():
    with open("idiom.json", "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    result_data = list(filter(lambda r: r is not None, map(clean_entry, raw_data)))

    with open("idiom_clean.json", "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()

import re
import json


def preprocess(card):
    text = card["text"]
    flavour = card["flavor"]

    text = text.lower()
    flavour = flavour.lower()

    text = re.sub(r"(<b>|<\/b>|<i>|<\/i>|\\n|\\t|\\r|$|_|#)", " ", text)
    flavour = re.sub(r"(<b>|<\/b>|<i>|<\/i>|\\n|\\t|\\r|$|_|#)", " ", flavour)

    text = re.findall(r"\w+|[^\w\s]", text)
    flavour = re.findall(r"\w+|[^\w\s]", flavour)

    for token in text:
        if token == "":
            text.remove(token)

    for token in flavour:
        if token == "":
            flavour.remove(token)

    return {
        "name": card["name"],
        "type": card["type"],
        "set": card["set"],
        "rule": " ".join(text),
        "flavour": " ".join(flavour)
    }


def main():
    cards_data = None
    with open('../../data/json/hearthstone_data/final_hearthstone_data.json') as f:
        cards_data = json.load(f)

    for year in cards_data.keys():
        new_cards_data = list()
        for card in cards_data[year]:
            new_cards_data.append(preprocess(card))
        cards_data[year] = new_cards_data

    with open('../../data/preprocessed/hearthstone/hearthstone_preprocessed_basic.json', 'w', encoding='utf-8') as f:
        json.dump(cards_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()

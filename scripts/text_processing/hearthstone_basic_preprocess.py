import json
import nltk
import re
from nltk import word_tokenize


def preprocess(card):
    text = card["text"]
    flavour = card["flavor"]

    text = text.lower()
    flavour = flavour.lower()

    text = re.sub(r"(<b>|<\/b>|<i>|<\/i>|\\n|\\t|\\r|\$|_|#)", " ", text)
    flavour = re.sub(r"(<b>|<\/b>|<i>|<\/i>|\\n|\\t|\\r|\$|_|#)", " ", flavour)

    text = word_tokenize(text)
    flavour = word_tokenize(flavour)

    text = clean_tokens(text)
    flavour = clean_tokens(flavour)

    return {
        "name": card["name"],
        "type": card["type"],
        "set": card["set"],
        "rule": " ".join(text),
        "flavour": " ".join(flavour)
    }


def clean_tokens(raw):
    for index, token in enumerate(raw):
        if token == "":
            raw.remove(token)
        if token == "''":
            raw[index] = '"'
        if token == "``":
            raw[index] = '"'
        if re.search(r"\d", token) is not None and len(token) > 1:
            raw[index] = " ".join(re.findall(r"\w+|[^\w\s]", token))
        if re.search(r"^'\w+", token) is not None:
            token_list = token.split("'")
            if len(token_list[1]) > 2:
                raw[index] = "' " + token_list[1]
    return raw


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

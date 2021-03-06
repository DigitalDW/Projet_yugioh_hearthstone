import json
import nltk
import re
from nltk import word_tokenize


def preprocess(card):
    text = card["text"]
    flavor = card["flavor"]

    text = text.lower()
    flavor = flavor.lower()

    text = re.sub(r"(<b>|<\/b>|<i>|<\/i>|\\n|\\t|\\r)", "", text)
    flavor = re.sub(r"(<b>|<\/b>|<i>|<\/i>|\\n|\\t|\\r)", "", flavor)

    text = word_tokenize(text)
    flavor = word_tokenize(flavor)

    text = clean_tokens(text)
    flavor = clean_tokens(flavor)

    return {
        "name": card["name"],
        "type": card["type"],
        "set": card["set"],
        "rule": " ".join(text),
        "flavor": " ".join(flavor)
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
        if re.search(r"^\*\w+", token) is not None:
            raw[index] = re.sub(r"^\*(\w+)", r"* \1", token)
        if re.search(r"\w+/\w+", token) is not None:
            token_list = token.split("/")
            if token_list[1] != "d":
                raw[index] = " ".join(re.findall(r"\w+|[^\w\s]", token))
    return raw


def main():
    cards_data = None
    with open('../../data/json/yugioh_data/final_yugioh_data.json') as f:
        cards_data = json.load(f)

    for year in cards_data.keys():
        new_cards_data = list()
        for card in cards_data[year]:
            new_cards_data.append(preprocess(card))
        cards_data[year] = new_cards_data

    with open('../../data/preprocessed/yugioh/yugioh_preprocessed_basic.json', 'w', encoding='utf-8') as f:
        json.dump(cards_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()

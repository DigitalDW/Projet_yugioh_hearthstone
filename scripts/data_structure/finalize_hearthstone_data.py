import json


def create_corpus_ready_json_file(cards_data, sets_data):
    corpus_ready_data = dict()
    for set_info in sets_data:
        cards = list()
        for card in cards_data[set_info["name"]]:
            if "collectible" in card.keys():
                if "text" in card.keys():
                    if "flavor" in card.keys():
                        cards.append({
                            "name": card["name"],
                            "type": card["type"],
                            "set": card["cardSet"],
                            "text": card["text"],
                            "flavor": card["flavor"]
                        })
                    else:
                        cards.append({
                            "name": card["name"],
                            "type": card["type"],
                            "set": card["cardSet"],
                            "text": card["text"],
                            "flavor": ""
                        })
                elif "flavor" in card.keys():
                    cards.append({
                        "name": card["name"],
                        "type": card["type"],
                        "set": card["cardSet"],
                        "text": "",
                        "flavor": card["flavor"]
                    })

        seen = set()
        new_cards = []
        for card in cards:
            tup = tuple(sorted(card.items()))
            if tup not in seen:
                seen.add(tup)
                new_cards.append(card)

        if set_info["date"] not in corpus_ready_data.keys():
            corpus_ready_data[set_info["date"]] = new_cards
        else:
            corpus_ready_data[set_info["date"]].extend(new_cards)

    sorted_corpus = dict()
    for key in sorted(corpus_ready_data):
        sorted_corpus[key] = corpus_ready_data[key]

    with open('../../data/json/hearthstone_data/corpus_oriented_hearthstone_data.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_corpus, f, ensure_ascii=False, indent=4)

    with open('../../data/json/hearthstone_data/final_hearthstone_data.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_corpus, f, ensure_ascii=False, indent=4)


def main():
    cards_data = None
    with open('../../data/json/hearthstone_data/hearthstone_raw_cards_data.json') as f:
        cards_data = json.load(f)

    sets_data = None
    with open('../../data/json/hearthstone_data/hearthstone_sets.json') as f:
        sets_data = json.load(f)

    create_corpus_ready_json_file(cards_data, sets_data)


if __name__ == "__main__":
    main()

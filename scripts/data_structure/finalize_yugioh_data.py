import json
import datetime
import re

def find_earliest_date(sets):
    date_list = list()
    
    for set_ in sets:
        date_list.append(set_['release_date'])
    
    formated_dates = list()
    for date in date_list:
        if date == "to be determined":
            date = "2020-07-22"
        date_text = date.split("-")
        formated_dates.append(datetime.datetime(int(date_text[0]), int(date_text[1]), int(date_text[2])))
    
    min_date = min(formated_dates).strftime("%Y-%m-%d")

    for set_data in sets:
        if set_data['release_date'] == "to be determined" and min_date == "2020-07-22":
            return set_data
        elif set_data['release_date'] == min_date:
            return set_data

def create_corpus_oriented_json_file(cards_data):
    corpus = dict()
    for card in cards_data:
        if 'card_sets' in card.keys():
            earliest = find_earliest_date(card['card_sets'])
            if earliest['release_date'] not in corpus.keys():
                corpus[earliest['release_date']] = [{
                    "name": card["name"],
                    "desc": card["desc"],
                    "origin_set": earliest["set_name"],
                    "type": card["type"]
                }]
            else:
                corpus[earliest['release_date']].append({
                    "name": card["name"],
                    "desc": card["desc"],
                    "origin_set": earliest["set_name"],
                    "type": card["type"]
                })

    sorted_corpus = dict()
    for key in sorted(corpus):
        sorted_corpus[key] = corpus[key]

    with open('../../data/json/yugioh_data/corpus_oriented_yugioh_data.json', 'w', encoding='utf-8') as f:
            json.dump(sorted_corpus, f, ensure_ascii=False, indent=4)

def harmonize_with_HS_datastructure():
    corpus_data = None
    with open('../../data/json/yugioh_data/corpus_oriented_yugioh_data.json') as f:
        corpus_data = json.load(f)

    new_corpus = dict()
    for date in corpus_data.keys():
        reorganized_data = list()
        for card in corpus_data[date]:
            if (card["type"] == "Normal Monster" or 
                card["type"] == "Normal Tuner Monster"):
                reorganized_data.append({
                    "name": card["name"],
                    "type": card["type"],
                    "set": card["origin_set"],
                    "text": "",
                    "flavor": card["desc"]
                })
            elif card["type"] == "Pendulum Normal Monster":
                description = re.split(r"\r\n", card["desc"])
                if len(description) > 1:
                    text = description[1]
                    flavor = description[len(description)-1]
                else:
                    text = ""
                    flavor = description[0]
                reorganized_data.append({
                    "name": card["name"],
                    "type": card["type"],
                    "set": card["origin_set"],
                    "text": text,
                    "flavor": flavor
                })
            elif re.search(r"Pendulum", card["type"]):
                description = re.split(r"\r\n", card["desc"])
                if len(description) == 1:
                    text = description[0]
                elif len(description) == 4:
                    text = description[1] + " " + description[len(description)-1]
                elif len(description) > 4:
                    text = description[1]
                    for i in range(3, len(description)-1):
                        text += " " + description[i]
                reorganized_data.append({
                    "name": card["name"],
                    "type": card["type"],
                    "set": card["origin_set"],
                    "text": text,
                    "flavor": ""
                })
            else:
                reorganized_data.append({
                    "name": card["name"],
                    "type": card["type"],
                    "set": card["origin_set"],
                    "text": card["desc"],
                    "flavor": ""
                })
        new_corpus[date] = reorganized_data
    sorted_corpus = dict()
    for key in sorted(new_corpus):
        sorted_corpus[key] = new_corpus[key]

    with open('../../data/json/yugioh_data/final_yugioh_data.json', 'w', encoding='utf-8') as f:
            json.dump(sorted_corpus, f, ensure_ascii=False, indent=4)


def main():
    cards_data = None
    with open('../../data/json/yugioh_data/yugioh_completed_data.json') as f:
        cards_data = json.load(f)
    
    create_corpus_oriented_json_file(cards_data)
    harmonize_with_HS_datastructure()


if __name__ == "__main__":
    main()
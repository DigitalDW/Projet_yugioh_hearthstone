import json
import re
import datetime

def add_dates(sets_data):
    date_conversion = {
        "January" : 1,
        "February" : 2,
        "March" : 3,
        "April" : 4,
        "May" : 5,
        "June" : 6,
        "July" : 7,
        "August" : 8,
        "September" : 9,
        "October" : 10,
        "November" : 11,
        "December" : 12,
    }

    for key, value in sets_data.items():
        if value != "unspecified" and len(value.split(" ")) >= 3:
            value = value.split(" ")
            value[0] = re.sub(r'[^\w\s]','',value[0])
            value[1] = re.sub(r'[^\w\s]','',value[1])
            value[0] = str(date_conversion[value[0]])
            value.insert(0, value.pop(-1))
            date = datetime.datetime(int(value[0]), int(value[1]), int(value[2]))
            sets_data[key] = date.strftime("%Y-%m-%d")
    
    return sets_data

def create_new_cards_json(yugioh_cards_data, sets_data):
    for card in yugioh_cards_data:
        if 'card_sets' in card.keys():
            for sets in card['card_sets']:
                if sets.get('release_date') is None:
                    if sets_data.get(sets['set_name']) is not None:
                        if sets_data[sets['set_name']] != "unspecified":
                            if len(sets_data[sets['set_name']].split("-")) >= 3:
                                sets['release_date'] = sets_data[sets['set_name']]
                            else:
                                sets['release_date'] = "to be determined"
                        else:
                            sets['release_date'] = "to be determined"
                    else:
                        sets['release_date'] = "to be determined"
                    

    with open('../../data/json/yugioh_data/yugioh_completed_data.json', 'w', encoding='utf-8') as f:
            json.dump(yugioh_cards_data, f, ensure_ascii=False, indent=4)

def main():
    sets_data = None
    with open('../../data/json/yugioh_data/yugioh_sets_filled.json') as f:
        sets_data = json.load(f)

    yugioh_cards_data = None
    with open('../../data/json/yugioh_data/yugioh_raw_cards_data.json') as f:
        yugioh_cards_data = json.load(f)
    
    new_sets_data = add_dates(sets_data)
    create_new_cards_json(yugioh_cards_data, new_sets_data)

if __name__ == "__main__":
    main()
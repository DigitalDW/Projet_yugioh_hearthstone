import requests
import json

def main():
    url = "https://db.ygoprodeck.com/api/v6/cardinfo.php"

    try:
        r = requests.get(url)
        with open('../../data/json/yugioh_data/yugioh_raw_cards_data.json', 'w', encoding='utf-8') as f:
            json.dump(r.json(), f, ensure_ascii=False, indent=4)
        
        set_list = []
        for card in r.json():
            if 'card_sets' in card.keys():
                for sets in card['card_sets']:
                    if sets['set_name'] not in set_list:
                        set_list.append(sets['set_name'])
        
        cards_without_sets = []
        for card in r.json():
            if 'card_sets' not in card.keys():
                cards_without_sets.append(card)
        
        try:
            output_file = open("../../data/txt/cards_without_set.txt", mode="w", encoding="utf-8")
            for sets in cards_without_sets:
                output_file.write(str(sets) + "\n")
            output_file.close()
        except IOError:
            print("Error in opening file")


        try:
            output_file = open("../../data/txt/sets.txt", mode="w", encoding="utf-8")
            for sets in set_list:
                output_file.write(sets + "\n")
            output_file.close()
        except IOError:
            print("Error in opening file")
    except requests.exceptions.Timeout as err:
        # Maybe set up for a retry, or continue in a retry loop
        print(err)
    except requests.exceptions.TooManyRedirects as err:
        # Tell the user their URL was bad and try a different one
        print(err)
    except requests.exceptions.RequestException as err:
        # catastrophic error. bail.
        print(err)

if __name__ == "__main__":
    main()
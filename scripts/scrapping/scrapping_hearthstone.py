import requests
import json


def main():
    # https://omgvamp-hearthstone-v1.p.rapidapi.com/cards
    # https://api.hearthstonejson.com/v1/25770/enUS/cards.json
    url = "https://omgvamp-hearthstone-v1.p.rapidapi.com/cards"
    headers = {
        'x-rapidapi-host': "omgvamp-hearthstone-v1.p.rapidapi.com",
        'x-rapidapi-key': "fff83ba25emsh8bd2ecbeccf17edp1c113bjsnc57735d6d858"
    }

    try:
        r = requests.request("GET", url, headers=headers)
        with open('../../data/json/hearthstone_data/hearthstone_raw_cards_data.json', 'w', encoding='utf-8') as f:
            json.dump(r.json(), f, ensure_ascii=False, indent=4)

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

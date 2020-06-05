import json

with open("../../../data/preprocessed/hearthstone/hearthstone_preprocessed_basic.json") as f:
    cards_info = json.load(f)

input_file = open("./ygo_important_years.txt", "r")
ygo_important_years = input_file.read()
input_file.close()

dates = list()
sets = list()
for year in cards_info.keys():
    if year not in dates:
        dates.append(year)

for year in cards_info.keys():
    for card in cards_info[year]:
        if card["set"] not in sets:
            sets.append(card["set"])

cards_totals = dict()
years = dict()
for set_ in sets:
    if set_ not in years.keys():
        years[set_] = dict()
        years[set_]["rule"] = 0
        years[set_]["flavor"] = 0
    sets_of_interest = [sets[i]
                        for i in range(0, sets.index(set_)+1)]
    for _set in sets_of_interest:
        for year in cards_info.keys():
            for card in cards_info[year]:
                if card["set"] == _set:
                    for token in card["rule"].split(" "):
                        years[set_]["rule"] += 1
                    for token in card["flavor"].split(" "):
                        years[set_]["flavor"] += 1

with open("./hs_tokens_per_date.json", "w") as f:
    json.dump(years, f)

output = open("./hs_important_years.txt", "w")
# output.write(sets)
output.close()


with open("../../../data/preprocessed/yugioh/yugioh_preprocessed_basic.json") as f:
    ygo = json.load(f)

dates = list()
for year in ygo.keys():
    if year not in dates:
        dates.append(year)

years = dict()
ygo_important_years = [i for i in ygo_important_years.split("\n")]
for date in ygo_important_years:
    if date not in years.keys():
        years[date] = dict()
        years[date]["rule"] = 0
        years[date]["flavor"] = 0
    dates_of_interest = [dates[i] for i in range(0, dates.index(date)+1)]
    for date_of_interest in dates_of_interest:
        for card in ygo[date_of_interest]:
            for token in card["rule"].split(" "):
                years[date]["rule"] += 1
            for token in card["flavor"].split(" "):
                years[date]["flavor"] += 1

with open("./ygo_words_per_dates.json", "w") as f:
    json.dump(years, f)

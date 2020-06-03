import json

with open("../data/preprocessed/hearthstone/hearthstone_preprocessed_basic.json") as f:
    cards_info = json.load(f)

dates = list()
sets = ""
for year in cards_info.keys():
    if year not in dates:
        dates.append(year)
        sets += year + "\n"

cards_totals = dict()
for date in dates:
    dates_of_interest = [dates[i]
                         for i in range(0, dates.index(date)+1)]
    for year in dates_of_interest:
        for card in cards_info[year]:
            if date not in cards_totals:
                cards_totals[date] = 1
            else:
                cards_totals[date] += 1

with open("./hs_cards_totals.json", "w") as f:
    json.dump(cards_totals, f)

output = open("./hs_important_years.txt", "w")
output.write(sets)
output.close()

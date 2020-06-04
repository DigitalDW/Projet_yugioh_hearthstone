import json

with open("../../../data/preprocessed/hearthstone/hearthstone_preprocessed_basic.json") as f:
    cards_info = json.load(f)

input_file = open("./ygo_important_years.txt", "r")
ygo_important_years = input_file.read()
input_file.close()

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


with open("../../../data/preprocessed/yugioh/yugioh_preprocessed_basic.json") as f:
    ygo = json.load(f)

dates = list()
for year in ygo.keys():
    if year not in dates:
        dates.append(year)

years = dict()
counter = 0
for date in dates:
    year = date.split("-")[0]
    if year not in years.keys():
        years[year] = counter
    for card in ygo[date]:
        counter += 1
        years[year] += 1

with open("./ygo_cards_per_year.json", "w") as f:
    json.dump(years, f)

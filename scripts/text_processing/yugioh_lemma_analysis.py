import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def main():
  cards_info = None
  with open("../../data/preprocessed/yugioh/yugioh_preprocessed_basic.json") as f:
    cards_info = json.load(f)

  stop_words = set(stopwords.words('english'))
  lemmatizer = WordNetLemmatizer()

  new_cards_info = dict()
  for year in cards_info.keys():
    new_cards = list()
    for card in cards_info[year]:
      rule = list()
      if card["rule"] != "":
        tokens = word_tokenize(card["rule"])
        rule = [lemmatizer.lemmatize(i) for i in tokens if not i in stop_words]
      flavour = list()
      if card["flavour"] != "":
        tokens = word_tokenize(card["flavour"])
        flavour = [lemmatizer.lemmatize(i) for i in tokens if not i in stop_words]
      new_cards.append({
        "name": card["name"],
        "type": card["type"],
        "set": card["set"],
        "rule": " ".join(rule),
        "flavour": " ".join(flavour)
      })
    new_cards_info[year] = new_cards
  
  with open('../../data/preprocessed/yugioh/yugioh_preprocessed_lemma.json', 'w', encoding='utf-8') as f:
    json.dump(new_cards_info, f, ensure_ascii=False, indent=4)
  


if __name__ == "__main__":
  main()

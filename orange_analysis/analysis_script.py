import json
from LTTL.Segmentation import Segmentation
from LTTL.Input import Input
from LTTL.Segment import Segment
import LTTL.Segmenter as Segmenter

with open("/Users/DigitalDW/Desktop/Projet_yugioh_hearthstone/data/preprocessed/hearthstone/hearthstone_preprocessed_basic.json") as f:
    hearthstone_data = json.load(f)

with open("/Users/DigitalDW/Desktop/Projet_yugioh_hearthstone/data/preprocessed/yugioh/yugioh_preprocessed_basic.json") as f:
    yugioh_data = json.load(f)


def main():
    hs_inputs, hs_annotations = create_inputs("Hearthstone", hearthstone_data)
    ygo_inputs, ygo_annotations = create_inputs("Yu-Gi-Oh", yugioh_data)

    inputs = list()
    annotations = list()

    inputs.extend(hs_inputs)
    inputs.extend(ygo_inputs)

    annotations.extend(hs_annotations)
    annotations.extend(ygo_annotations)

    segmentation = Segmenter.concatenate(
        inputs,
        import_labels_as=None
    )

    for index, segment in enumerate(segmentation):
        segment.annotations.update(annotations[index])
        segmentation[index] = segment

    out_object = segmentation


def create_inputs(game, data):
    inputs = list()
    inputs_annotations = list()

    for year in data.keys():
        for card in data[year]:
            if len(card["rule"]) > 0:
                input_rule = Input(card["rule"])
                inputs.append(input_rule)
                inputs_annotations.append({
                    "release_date": year,
                    "game": game,
                    "card_name": card["name"],
                    "set": card["set"],
                    "card_type": card["type"],
                    "text_type": "rule",
                })
            if len(card["flavour"]) > 0:
                input_flavour = Input(card["flavour"])
                inputs.append(input_flavour)
                inputs_annotations.append({
                    "release_date": year,
                    "game": game,
                    "card_name": card["name"],
                    "set": card["set"],
                    "card_type": card["type"],
                    "text_type": "flavour",
                })

    return inputs, inputs_annotations


if __name__ == "builtins":
    main()

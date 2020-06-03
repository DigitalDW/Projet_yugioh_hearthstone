import json
from LTTL.Segmentation import Segmentation
from LTTL.Input import Input
from LTTL.Segment import Segment
import LTTL.Segmenter as Segmenter

# Parametres...
CURRENT_DATE = "2005-03-01"

def main():
    global out_object

    dates = list()
    for segment in in_object:
        date = segment.annotations["release_date"]
        if date not in dates:
            dates.append(date)
    segmentation = list()
    dates_of_interest = [dates[i] for i in range(0, dates.index(CURRENT_DATE)+1)]
    for segment in in_object:
        annotations = segment.annotations
        if segment.annotations["release_date"] in dates_of_interest:
        #     annotations["_"] = "current or previous"
        # else:
        #     annotations["_"] = "following"
        #  segment.annotations.update(annotations)
            segmentation.append(segment)
    
    out_object = Segmentation(segmentation)

if __name__ == "builtins":
    main()
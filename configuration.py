import string

_BASE = {
    "name": "base",
    "dataset": {
        "name": "american-english",
        "to_clean": True,
    },
    "keys": {
        "before": ["1", "left", "minus"],
        "after": ["2", "right", "plus"],
        "start": "5",
    },
    "screen": {
        "size": [800, 600],
        "color": "black",
        "monitor": "testMonitor",
    },
    "tasks": {
        "icons": {
            "left": u"\u2190",
            "right":  u"\u2192",
            "correction": u"\u2A2F",
            "fixation": '+',
        },
        "colors": {
            "inactive": "gray",
            "active": "white",
        },
        "distance": 0.58,
        "height": 0.07,
    },
    "alphabet": {
        "letters" : string.ascii_uppercase,
        "length": 0.53, #percent of screen size
        "y_position": 0.8,
        "height": 0.07,
    },
    "classifier": {
        "acceptance_treshold": 0.2,
        "directions":{
            -1: "before",
             1: "after",
        },
    }
}

_RUN = _BASE.update({
    "timing": {
        "first_fixation": 20,
        "previous_classification": 2,
        "plan": 3,
        "answer": 10,
        "rest": 5,
        "last_fixation": 20,
    },
})


_PARTICIPANT = _RUN.update({
  "participant": "0023",
  "input_method": "network_long", # Can be: auto, manual, network_long, network_short
  "target_word": "respectfulness", # To be used for method "auto"
})

CONF = _PARTICIPANT
import json
import string

_BASE = {
    'name': 'base',
    'datalog_folder': 'datalog',
    'dataset': {
        'name': 'american-english',
        'to_clean': True,
    },
    'keys': {
        'before': ['1', 'left', 'minus'],
        'correction': ['2', 'down'],
        'after': ['3', 'right', 'plus'],
    },
    'screen': {
        'size': [800, 600],
        'color': 'black',
        'monitor': 'testMonitor',
    },
    'tasks': {
        'icons': {
            'before': u'\u2190',
            'after':  u'\u2192',
            'correction': u'\u2A2F',
            'fixation': '+',
        },
        'colors': {
            'inactive': '#C7C7C7',
            'active': 'red',
        },
        'distance': 0.58,
        'height': 0.12,
        'side_words_height': 0.08,
    },
    'alphabet': {
        'letters' : string.ascii_uppercase,
        'length': 0.53, #percent of screen size
        'y_position': 0.8,
        'height': 0.07,
    },
    'classifier': {
        'acceptance_treshold': 0.2,
        'directions':{
            -1: 'before',
             1: 'after',
        },
    }
}

_BASE.update({
    'positions':{
        'center': [0,0],
        'before_word': [0, 0.2],
        'after_word': [0, -0.2],
        'correction_icon': [0, 0.4],
        'before_icon': [0-_BASE['tasks']['distance'], 0],
        'after_icon': [_BASE['tasks']['distance'], 0],
    }
})


# Per run config
_BASE.update({
    'timing': {
        'first_fixation': 20,
        'previous_classification': 2,
        'plan': 3,
        'answer': 10,
        'rest': 25,
        'last_fixation': 20,
    },
})


# debug config
_BASE.update({
    'timing': {
        'first_fixation': 3,
        'previous_classification': 3,
        'plan': 5,
        'answer': 5,
        'rest': 5,
        'last_fixation': 1,
        'missing_prediction_timeout': 0.1,
    },
})

_BASE.update({
  'satori': {
      'filepath': 'bettina_files/NIRS-2018-05-15_001_BCI_output.txt',
      'port_address': [0xD010, None][1],
      'predictor': ['beta', 'b', 'tValue', 'r'][0],
      'discriminator': max,
  },
})


_BASE.update({
  'participant': '0023',
  'input': {
      'method': ['manual', 'auto', 'satori' ][0], 
      'target': 'respectfulness', # Used in method 'auto'
  }
})

CONF = _BASE


def serialize_conf():
    def myconverter(o):
        if True:
            return o.__str__()

    return json.dumps(CONF, indent=2, sort_keys=True, default=myconverter)
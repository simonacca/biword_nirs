import json
import string

DEBUG = False

REMOTE_FOLDER = "\\\\fdpmob0162\Users\B.Sorger\Documents\TSIData\BCI_Output\\"

_BASE = {
    'debug': DEBUG,
    'name': 'base',
    'datalog_folder': REMOTE_FOLDER + "StimulationOutput\\",
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
		'fullscr': not DEBUG,
        'color': 'black',
        'monitor': 'testMonitor',
    },
    'tasks': {
        'icons': {
            'before': u'\u2190',
            'after':  u'\u2192',
            'correction': 'x',
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
        'first_fixation': 1 if DEBUG else 60,
        'plan': 1 if DEBUG else 5,
        'answer': 1 if DEBUG else 5,
        'rest': 1 if DEBUG else 10,
        'previous_classification': 1 if DEBUG else 2,
        'rest2': 1 if DEBUG else 7,
        'last_fixation': 1 if DEBUG else 10,
        'missing_prediction_timeout': 0.1,
    },
})



_BASE.update({
  'satori': {
      'path': REMOTE_FOLDER,
      'port_address': [0x0378, None][0],
      'predictor': ['beta', 'b', 'tValue', 'r'][2],
      'discriminator': max,
  },
})


_BASE.update({
  'participant': '0001',
  'input': {
      'method': ['manual', 'auto', 'satori' ][2], 
      'target': 'respectfulness', # Used in method 'auto'
  }
})

CONF = _BASE


def serialize_conf():
    def myconverter(o):
        if True:
            return o.__str__()

    return json.dumps(CONF, indent=2, sort_keys=True, default=myconverter)
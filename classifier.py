import operator
from psychopy import event
from configuration import CONF
import satori

class Classifier:
    def __init__(self, dataset):
        self.dataset = dataset


    def get_prediction(self, sequence_number):
        "Calls the appropriate method according to CONF"
        return getattr(self, '_get_prediction_{}'.format(CONF['input']['method']))(sequence_number)

    def _get_prediction_manual(self, sequence_number):
        while True:
            key = event.waitKeys()
            for direction, keys in CONF['keys'].items():
                if key[0] in keys:
                    return direction

    def _get_prediction_auto(self, sequence_number):
        return 'before' if CONF['input']['target'] < self.dataset.middle_word()[1] else 'after'

    def _get_prediction_satori(self, sequence_number):
        data = satori.parse(CONF['satori']['filepath'])
        # Maybe try again here?
        try:
            prediction = data[sequence_number]
        except IndexError:
            return None

        options = list(map(lambda d: d[CONF['satori']['predictor']], prediction['options']))
        options.pop(0)

        index, value = CONF['satori']['discriminator'](enumerate(options), key=operator.itemgetter(1))

        mapping = {
            1: 'correction',
            2: 'before',
            3: 'after'
        }

        return mapping[index + 1]
        
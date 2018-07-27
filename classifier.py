import sys
import operator
from psychopy import event
from configuration import CONF
import satori


class Classifier:
    def __init__(self, dataset):
        self.dataset = dataset

    def _escape(self, keys=None):
        if not keys:
            keys = event.getKeys()
        if keys and keys[-1] == 'escape':
            print('User terminated run early')
            sys.exit(1)


    def get_prediction(self, sequence_number):
        "Calls the appropriate method according to CONF"
        return getattr(self, '_get_prediction_{}'.format(CONF['input']['method']))(sequence_number)

    def _get_prediction_manual(self, sequence_number):
        key = event.getKeys()
        self._escape(key)
        for direction, keys in CONF['keys'].items():
            if key and (key[-1] in keys):
                return direction
        return None

    def _get_prediction_auto(self, sequence_number):
        self._escape()
        return 'before' if CONF['input']['target'] < self.dataset.middle_word()[1] else 'after'

    def _get_prediction_satori(self, sequence_number):
        self._escape()
        data = satori.parse(CONF['satori']['filepath'])
        # Maybe try again here?
        try:
            prediction = data[sequence_number]
        except IndexError:
            return None

        options = [d[CONF['satori']['predictor']] for d in prediction['options']]
        options.pop(0)

        index, value = CONF['satori']['discriminator'](enumerate(options), key=operator.itemgetter(1))

        mapping = {
            1: 'correction',
            2: 'before',
            3: 'after'
        }

        return mapping[index + 1]
        
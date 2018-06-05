from psychopy import event
from configuration import CONF

class Classifier:
    def __init__(self, dataset):
        self.dataset = dataset


    def get_prediction(self):
        "Calls the appropriate method according to CONF"
        return getattr(self, '_get_prediction_{}'.format(CONF['input']['method']))()

    def _get_prediction_manual(self):
        while True:
            key = event.waitKeys()
            for direction, keys in CONF['keys'].items():
                if key[0] in keys:
                    return direction

    def _get_prediction_auto(self):
        return 'before' if CONF['input']['target'] < self.dataset.middle_word()[1] else 'after'

    def _get_prediction_satori(self):
        pass
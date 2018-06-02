from psychopy import event
from configuration import CONF

class Classifier:
    def get_prediction(self):
        return getattr(self, '_get_prediction_{}'.format(CONF['input']['method']))()

    def _get_prediction_manual(self):
        while True:
            key = event.waitKeys()
            for key_type, keys in CONF['keys'].items():
                if key[0] in keys:
                    return key_type

    def _get_prediction_auto(self):
        pass

    def _get_prediction_satori(self):
        pass
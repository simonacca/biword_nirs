from psychopy import visual, core, event
from configuration import CONF


class Screen:
    def __init__(self):
        self.window = visual.Window(fullscr=True, units="norm", **CONF["screen"])
        self._create_alphabet()


    def _icon(self, icon, position, active=False):
        positions = {
            'center': [0,0],
            'center_low': [0, 0.5], # TODO: adjust
            'left': [0-CONF['tasks']['distance'], 0],
            'right': [CONF['tasks']['distance'], 0],
        }
        shades = {
            True: 'active',
            False: 'inactive'
        }

        visual.TextStim(
            self.window,
            height=CONF['tasks']['height'],
            text=CONF['tasks']['icons'][icon],
            pos=positions[position],
            color=CONF['tasks']['color'][shades[active]]
        ).draw()

    def _word(self, word):
        visual.TextStim(self.window, text=word).draw()

    def _create_alphabet(self):
        self.alphabet = []
        spacing = CONF["alphabet"]["length"]*2/(len(CONF["alphabet"]["letters"])-1)
        for i, letter in enumerate(CONF["alphabet"]["letters"]):
            self.alphabet.append(
                visual.TextStim(self.window,
                    text=letter,
                    pos=[
                        0-CONF["alphabet"]["length"]+spacing*i,
                        CONF["alphabet"]["y_position"]
                    ],
                    height=CONF["alphabet"]["height"]))

    def _show_alphabet(self):
        for letter in self.alphabet:
            letter.draw()

    def show_fixation(self):
        self._icon('fixation', 'center', True)

    def show_previous_classification(self, direction):
        self._icon(direction, 'center', True).draw()
        self.window.flip()

    def show_word(self, word, active=None):
        self._icon('left', 'left', active == 'left')
        self._icon('right', 'right', active == 'right')
        self._icon('correction', 'center_low', active == 'correction')
        self._word(word)
        self.window.flip()
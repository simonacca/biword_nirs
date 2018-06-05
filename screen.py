from psychopy import visual, core, event
from configuration import CONF

shades = {
    True: 'active',
    False: 'inactive'
}


class Screen:
    def __init__(self):
        self.window = visual.Window(fullscr=True, units="norm", **CONF["screen"])
        self._create_alphabet()

    def _icon(self, icon, position, active=False):
        visual.TextStim(
            self.window,
            height=CONF['tasks']['height'],
            text=CONF['tasks']['icons'][icon],
            pos=CONF['positions'][position],
            color=CONF['tasks']['colors'][shades[active]]
        ).draw()

    def _word(self, word_range, finished):
        print(word_range)
        visual.TextStim(
            self.window,
            text= unicode(word_range[1] , "utf-8") + ('!!' if finished else ''),
            pos=CONF['positions']['center']
        ).draw()

        if not finished:
            visual.TextStim(
                self.window,
                text= unicode(word_range[0] , "utf-8"),
                color=CONF['tasks']['colors'][shades[False]],
                pos=CONF['positions']['before_word']
            ).draw()

            visual.TextStim(
                self.window,
                text=unicode(word_range[2] , "utf-8"),
                color=CONF['tasks']['colors'][shades[False]],
                pos=CONF['positions']['after_word']
            ).draw()

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
        self.window.flip()

    def show_previous_classification(self, direction):
        if not direction: return
        self._icon(direction, 'center', True).draw()
        self.window.flip()

    def show_word(self, word_range, active=None):
        finished = word_range[0] == word_range[1] == word_range[2]

        self._word(word_range, finished)

        if not finished:
            self._show_alphabet()
            self._icon('before', 'before_icon', active == 'before')
            self._icon('after', 'after_icon', active == 'after')
            self._icon('correction', 'correction_icon', active == 'correction')

        self.window.flip()
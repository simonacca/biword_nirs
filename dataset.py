import copy


class Dataset:
    "This class handles all of the datset manipulation."
    def __init__(self, dataset_name, to_clean=True):
        """
        When you create an instance of Dataset, this automatically loads the
        dataset, and unless you specify to_clean=False, it cleans the dataset.
        """
        self._load_dataset(dataset_name)
        if to_clean:
            self._clean_dataset()
        self.directions = []
        self.mistake_count = 0

    def _load_dataset(self, dataset_name):
        """
        This is used internally to load the dataset from the datsets folder,
        and makes the string into a list of words.
        """
        path = './datasets/{}'.format(dataset_name)
        with open(path, 'r') as f:
            self.dataset = f.read().split('\n')

    def _clean_dataset(self):
        """
        This is used internally to remove words with apostrophes, make uppercase
        words lowercase, and remove doubles. Happens automatically unless
        specified otherwise.
        """
        self.dataset = list(filter(lambda word: "'" not in word, self.dataset))
        self.dataset = list(map(lambda word: word.lower(), self.dataset))
        self.dataset = list(set(self.dataset))
        self.dataset = sorted(self.dataset)

    def _middle_word_position(self, dataset):
        "Internally used to get the position of the middle word."
        return int(len(dataset)/2)

    def middle_word(self):
        "Used to get the middle word of the dataset."
        t = copy.deepcopy(self.dataset)
        for direction in self.directions:
            if direction == 'before':
                t = t[:self._middle_word_position(t)]
            elif direction == 'after':
                t = t[self._middle_word_position(t):]
        return t[0], t[self._middle_word_position(t)], t[-1]


    def split(self, direction):
        "Splits the dataset based on answer."

        if direction == 'correction':
            try:
                old_direction = self.directions.pop()
                self.mistake_count += 1
            except IndexError:
                return
            
            if self.mistake_count == 1:
                self.directions.append(
                    'before' if old_direction == 'after' else 'after')
                return
            elif self.mistake_count == 2:
                self.mistake_count = 0
        else:
            self.directions.append(direction)
            self.mistake_count = 0

    def is_finished(self):
        "Checks for the end of the process, when there is only 1 word left."
        left, middle, right = self.middle_word()
        return left == middle == right

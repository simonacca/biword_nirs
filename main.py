import json
import logging
from psychopy import core
from dataset import Dataset
from screen import Screen
from classifier import Classifier
from trigger import Trigger
from datalog import Datalog

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s-%(levelname)s-%(message)s',
)

# Summon Configurations
from configuration import CONF, serialize_conf

print(serialize_conf())
# raw_input('Have you updated the config?') 

logging.info('Configuration loaded')

# Summon dataset
dataset = Dataset(CONF["dataset"]["name"], CONF["dataset"]["to_clean"])
logging.info('Dataset loaded')

# Initialize stuff
screen = Screen()
datalog = Datalog()
trigger = Trigger()
classifier = Classifier(dataset)
# TODO select input method
logging.info('Initialization completed')

# TODO: wait for spacebar to start experiment
# event.waitkey

# starts clock for timestamping events
clock = core.Clock()
logging.info('Starting experiment clock')
# Presents simple fixation
screen.show_fixation()
trigger.start_experiment()

core.wait(CONF['timing']['first_fixation'])

sequence_number = -1
direction = None
while not dataset.is_finished():
    sequence_number += 1
    logging.info('Iteration #%s', sequence_number)

    trigger.start_trial()

    logging.info('Phase: Show previous classification')
    screen.show_previous_classification(direction)

    core.wait(CONF['timing']['previous_classification'])

    logging.info('Phase: Plan')
    datalog.data['sequence'] = sequence_number
    datalog.data['word'] = dataset.middle_word()
    datalog.data['time_start_planning'] = clock.getTime()
    screen.show_word(dataset.middle_word())

    core.wait(CONF['timing']['plan'])

    for phase in ['correction', 'before', 'after']:
        logging.info('Phase: {}'.format(phase))
        datalog.data['time_start_correction'] = clock.getTime()
        screen.show_word(dataset.middle_word(), phase)

        core.wait(CONF['timing']['answer'])

    # Resting period
    logging.info('Phase: Rest')
    screen.show_fixation()
    core.wait(CONF['timing']['rest'])


    # Waits for answer to proceed to next word
    direction = classifier.get_prediction(sequence_number)
    logging.info('Classifier prediction: {}'.format(direction))

    datalog.data['time_answer'] = clock.getTime()
    datalog.data['direction'] = direction

    datalog.save()

    # splits dataset to start the next loop
    dataset.split(direction)

logging.info('Dictionary has lenght 1, end of iteration')
logging.info('Final word: %s', dataset.middle_word()[1])

screen.show_word(dataset.middle_word())
core.wait(CONF['timing']['plan'])

logging.info('Show fixation cross')

screen.show_fixation()
core.wait(CONF['timing']['last_fixation'])

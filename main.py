import json
import logging
from psychopy import core
from dataset import Dataset
from screen import Screen
from classifier import Classifier
from trigger import Trigger
from datalog import Datalog

# Summon Configurations
from configuration import CONF, serialize_conf
datalog = Datalog()

logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

fileHandler = logging.FileHandler("{}/{}.log".format(CONF['datalog_folder'], datalog.OUTPUT_FILE_NAME))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)


print(serialize_conf())
# raw_input('Have you updated the config?') 

logging.info('Configuration loaded')

# Summon dataset
dataset = Dataset(CONF["dataset"]["name"], CONF["dataset"]["to_clean"])
logging.info('Dataset loaded')

# Initialize stuff
screen = Screen()
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
# trigger.start_experiment()
trigger.arbitrary_trigger(1)

core.wait(max(0, CONF['timing']['first_fixation'] 
    - CONF['timing']['previous_classification']
    - CONF['timing']['rest2']
    ))

sequence_number = -1
direction = None
while not dataset.is_finished():
    sequence_number += 1
    logging.info('Iteration #%s', sequence_number)

    # trigger.start_trial()

    logging.info('Phase: Show previous classification')
    screen.show_previous_classification(direction)

    core.wait(CONF['timing']['previous_classification'])

    screen.show_fixation()
    core.wait(CONF['timing']['rest2'])

    logging.info('Phase: Plan')
    logging.info('Words are: {}'.format(dataset.middle_word()))
    datalog.data['sequence'] = sequence_number
    datalog.data['word'] = dataset.middle_word()
    datalog.data['time_start_planning'] = clock.getTime()
    screen.show_word(dataset.middle_word(), 'plan')
    trigger.arbitrary_trigger(2)

    core.wait(CONF['timing']['plan'])

    phase_count = 0
    for phase in ['correction', 'before', 'after']:
        logging.info('Phase: {}'.format(phase))
        datalog.data['time_start_correction'] = clock.getTime()
        screen.show_word(dataset.middle_word(), phase)

        trigger.arbitrary_trigger(3 + phase_count)
        core.wait(CONF['timing']['answer'])

        phase_count += 1

    # Resting period
    logging.info('Phase: Rest')
    screen.show_fixation()
    core.wait(CONF['timing']['rest'])


    # Waits for answer to proceed to next word
    direction = classifier.get_prediction(sequence_number)
    while direction == None:
        logging.warning('Prediction missing, waiting')
        core.wait(CONF['timing']['missing_prediction_timeout'])
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

import datetime
import json
import collections
import os
import csv

from configuration import CONF, serialize_conf

class Datalog:
    def __init__(self):
        'Initialize Logger'

        if not os.path.exists(CONF['datalog_folder']):
            os.makedirs(CONF['datalog_folder'])

        # Determines name for output fole
        self.OUTPUT_FILE_NAME = '{}_{}_{}_{}'.format(
            CONF['participant'],
            CONF['name'],
            CONF['input']['method'],
            datetime.datetime.now().strftime('%Y-%m-%d-%H-%M'))
        self.path = os.path.join(CONF['datalog_folder'], self.OUTPUT_FILE_NAME)

        # TODO: auto create output folder

        self.save_conf()

        # Initialize container for data and writes header to CSV file
        self.data = collections.OrderedDict([
            ['sequence', None],
            ['word', None],
            ['direction', None],
            ['time_start_planning', None],
            ['time_start_thinking', None],
            ['time_answer', None],
        ])
        self.append_row(self.data.keys())

    def save_conf(self):
        'Writes CONF used for current run to a file, for future reference'
        with open('{}_conf.json'.format(self.path), 'w+') as f:
            f.write(serialize_conf())

    def append_row(self, data):
        'Writes a generic row to the csv file (could be data or HEADER)'
        with open('{}.csv'.format(self.path), 'a+') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def save(self):
        'Writes accumulated data row to disk and clear the dictionary'
        self.append_row(self.data.values())
        for k in self.data:
            self.data[k] = None

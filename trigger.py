import logging
from psychopy import parallel
from psychopy import core
from configuration import CONF

class Trigger:
    def __init__(self,):
        if CONF['satori']['port_address']:
            parallel.setPortAddress(CONF['satori']['port_address'])
            # self.port = parallel.ParallelPort(address=CONF['satori']['port_address'])
            parallel.setData(0)
    
    def _send_data(self, trigger):
        triggers = {
            1: "00000001",
            2: "00000010",
            3: "00000011",
            4: "00000100",
            5: "00000101",
            6: "00000110",
        }
        if CONF['satori']['port_address']:
            parallel.setData( int(triggers[trigger], 2) ) 
            core.wait(0.01)
            parallel.setData(0)
    
    def arbitrary_trigger(self, number):
        self._send_data(number)

    # def start_trial(self):
    #     logging.info('Trigger send: start_trial')
    #     self._send_data(1)


    # def start_experiment(self):
    #     logging.info('Trigger send: start_experiment')
    #     self._send_data(1)
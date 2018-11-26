import json
import re
import os
from os.path import join
import logging
from datetime import datetime


def _parse_time(line, output):
    output.append({
        #'time': datetime.strptime(line, 'Time: %H:%M:%S\n'),
        'options': []
    })

def _parse_frame(line, output):
	pass
    
def _parse_beta(line, output):
    val = re.findall(r'Beta: ([\d\.\-]*)', line)
    if not val: raise Exception() # fail early
    output[-1]['options'].append({})
    output[-1]['options'][-1]['beta'] = float(val[0])

def _parse_b(line, output):
    val = re.findall(r'b: ([\d\.\-]*)', line)
    output[-1]['options'][-1]['b'] = float(val[0])

def _parse_tValue(line, output):
    val = re.findall(r't-Value: ([\d\.\-]*)', line)
    output[-1]['options'][-1]['tValue'] = float(val[0])

def _parse_r(line, output):
    val = re.findall(r'r: ([\d\.\-]*)', line)
    output[-1]['options'][-1]['r'] = float(val[0])

def _parse_ws1(line, output):
    if not line.isspace(): raise Exception()

def _parse_decision(line, output):
    val = re.findall(r'Decision: ([\d\.\-]*)', line)
    output[-1]['decision'] = int(val[0])

def _parse_ws2(line, output):
    if not line.isspace(): raise Exception()

def _parse_end(line, output):
    # end of file seems to have some junk, always accept it
    pass


FSM = {
    'BEGIN': [_parse_time],
    _parse_time: [_parse_frame],
	_parse_frame: [_parse_beta],
    _parse_beta: [_parse_b],
    _parse_b: [_parse_tValue],
    _parse_tValue: [_parse_r],
    _parse_r: [_parse_beta, _parse_ws1],
    _parse_ws1: [_parse_decision],
    _parse_decision: [_parse_ws2],
    _parse_ws2: [_parse_time, _parse_ws2, _parse_end],
    _parse_end: [_parse_end]
}

def parse(path):
    """
    sample_output = [{
        'time': datetime.now(),
        'decision': 1,
        'options': [
            {
                'beta': 1.1,
                'b': 1.1,
                'tValue': 1.1,
                'r': 1.1,

            },
            {
                'beta': 1.1,
                'b': 1.1,
                'tValue': 1.1,
                'r': 1.1,

            },
            {
                # ...
            }
        ]
    },
    {
        # ...
    }
    ]
    """

    files = os.listdir(path)
    files = list(sorted(filter(lambda x: x.endswith(".txt"), files)))
    files = list(sorted(filter(lambda x: not x.startswith("BCI"), files)))
    file = files[-1]
    print('Reading file', file)
	
	

    with open(join(path, file), 'r') as f:
        lines = f.readlines()
    
    output = []
    state = 'BEGIN'

    for line in lines:
        for parser in FSM[state]:
            #print('Trying parser {} on line: "{}"'.format(parser.__name__, repr(line)))
            try:
                parser(line, output)
                state = parser
                #print("it worked")
                break
            except Exception as e:
                #print('Last parser did not work')
                pass
        else:
            raise Exception('parsing error')
    
    if state not in [_parse_end, _parse_decision, _parse_ws2]:
        output.pop()
        logging.warning('parsing error, FSM terminated early')
    
    return output


if __name__ == '__main__':
    r = parse("\\\\fdpmob0162\Users\B.Sorger\Documents\TSIData\BCI_Output\\")
    print(json.dumps(r, indent=2))
    with open('temp.txt', 'w+') as f:
        f.write(json.dumps(r, indent=2))
import re
from datetime import datetime


def _parse_time(line, output):
    output.append({
        'time': datetime.strptime(line, 'Time: %H:%M:%S\n'),
        'options': []
    })
    
def _parse_beta(line, output):
    val = re.findall(r'Beta: ([\d\.\-]*)', line)
    output[-1]['options'].append({
        'beta': float(val[0])
    })

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
    output[-1]['options'][-1]['Decision'] = int(val[0])

def _parse_ws2(line, output):
    if not line.isspace(): raise Exception()

def _parse_end(line, output):
    # end of file seems to have some junk, always accept it
    pass


FSM = {
    'BEGIN': [_parse_time],
    _parse_time: [_parse_beta],
    _parse_beta: [_parse_b],
    _parse_b: [_parse_tValue],
    _parse_tValue: [_parse_r],
    _parse_r: [_parse_beta, _parse_ws1],
    _parse_ws1: [_parse_decision],
    _parse_decision: [_parse_ws2],
    _parse_ws2: [_parse_time, _parse_end],
    _parse_end: [_parse_end]
}

def parse(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    output = []
    state = 'BEGIN'

    for line in lines:
        for parser in FSM[state]:
            print('Trying parser {} on line: "{}"'.format(parser.__name__, repr(line)))
            try:
                parser(line, output)
                state = parser
                break
            except Exception as e:
                print(e)
                print('Did not work')
        else:
            raise Exception('parsing error')
    
    if state not in [_parse_end, _parse_decision]:
        raise Exception('parsing error')
    
    return output


if __name__ == '__main__':
    r = parse('bettina_files/NIRS-2018-05-15_001_BCI_output.txt')
    print(r)
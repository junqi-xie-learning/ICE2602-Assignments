# SJTU EE208

import sys, time

class Ticker(object):
    '''
    Output dots to the terminal, prompting the time consumed.
    '''
    def __init__(self, prompt):
        self.tick = True
        self.prompt = prompt

    def run(self):
        print(self.prompt)
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)
        print('Done')
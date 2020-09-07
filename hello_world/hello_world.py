# SJTU EE208
# This is a simple test file for learning how to use docker.

import os

print('Hello world!')
os.makedirs('test', exist_ok=True)
with open('test/output.txt', 'w') as f:
    f.write('Hello world from txt.')
with open('test/output.txt', 'r') as f:
    print(f.read())

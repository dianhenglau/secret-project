import json
import time
import random
import string

def get_random_name():
    return ''.join(random.choices(string.ascii_lowercase, k=5))

def get_random_time():
    int(time.time()) - random.randint(0, 7*24*60*60)

x = []

for i in range(8):
    x.append([])
    for j in range(8):
        x[i].append([])
        for k in range(50):
            x[i][j].append(None if random.random() >= 0.5 else [
                get_random_name(),
                get_random_time()
            ])


for j in range(4):
    for k in range(50):
        x[0][j][k] = [
            get_random_name(),
            get_random_time()
        ]

with open('data.json', 'w') as f:
    json.dump(x, f)

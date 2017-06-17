from sys import path

path.extend("./")
from presisto.presistentdict import PersistentDict
from time import time

iterations = 1000000
pd = PersistentDict()

start_time = time()

for i in range(iterations):
    pd[i] = i

print("Stored {} records in {} seconds ".format(iterations, time() - start_time))

start_time = time()
for i in range(iterations):
    if i not in pd:
        raise Exception("Record not found {}".format(str(i)))

print("Check existance of {} records in {} seconds ".format(iterations, time() - start_time))

start_time = time()
for i in range(iterations):
    pd[i]

print("read {} records in {} seconds ".format(iterations, time() - start_time))

from sys import path

path.extend("./")
from presisto.presistentdict import PersistentDict
from time import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

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

print("----- trying concurrent I/O -----")


def write(key, value, pd):
    pd[key] = value


def read(key, pd):
    return pd[key]


def check(key, pd):
    return key in pd


pd = PersistentDict('./.data2')
with ThreadPoolExecutor(max_workers=cpu_count() * 2) as executor:
    start_time = time()
    for i in range(iterations):
        executor.submit(write, i, i, pd)
print("Stored {} records in {} seconds ".format(iterations, time() - start_time))

with ThreadPoolExecutor(max_workers=cpu_count() * 2) as executor:
    start_time = time()
    for i in range(iterations):
        executor.submit(check, i, pd)
print("Check existance of {} records in {} seconds ".format(iterations, time() - start_time))

with ThreadPoolExecutor(max_workers=cpu_count() * 2) as executor:
    start_time = time()
    for i in range(iterations):
        executor.submit(read, i, pd)
print("read {} records in {} seconds ".format(iterations, time() - start_time))

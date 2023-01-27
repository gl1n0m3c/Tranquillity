from threading import *
from time import time, sleep

def one(num):
    k = 0
    while True:
        k += 1
        print(k)
        sleep(num)

def two(num):
    k = 0
    while True:
        k -= 1
        print(k)
        sleep(num)

t1 = Thread(target = one, args = (1,))
t2 = Thread(target = two, args = (1,))

t1.start()
t2.start()

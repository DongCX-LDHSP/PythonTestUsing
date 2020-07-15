from datetime import datetime
import time
from random import randint


def test_default_parameter(a: datetime = datetime.now()):
    print(a, id(a))


for i in range(10):
    test_default_parameter()
    time.sleep(0.5)


def test(a: int = randint(1, 10) * randint(2, 300)):
    print(a)


for i in range(10):
    test()

print("\n------------------------\n")

for i in range(10):
    test()
    time.sleep(0.5)

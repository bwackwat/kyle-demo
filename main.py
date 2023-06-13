import time
import sys

print("Hello, world!")

count = 0
while count < 60:
    time.sleep(1)
    print(f"Hello {count}", flush=True)
    # print("Hello " + count)
    count += 1

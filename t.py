import queue
import threading
import time


def worker():
    while True:
        item = q.get()
        if item is None:
            break
        time.sleep(2)
        q.task_done()

q = queue.Queue()
threads = []
for i in range(2):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for item in range(1,2):
    q.put(item)

# block until all tasks are done
q.join()

# stop workers
for i in range(2):
    q.put('123')
for t in threads:
    t.join()
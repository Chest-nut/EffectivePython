from threading import Thread

from thread_process.single_thread import handle


class MyThread(Thread):
    def __init__(self, cid):
        Thread.__init__(self)
        self.cid = cid
        self.lottery_type = {0: 'dlt-20', 1: 'fc3d-20', 2: 'pl3-20',
                             3: 'pl5-20', 4: 'qcl-20', 5: 'qxc-20',
                             6: 'ssq-20', 7: 'cqssc-20', 8: 'gd11x5-20',
                             9: 'bj11x5-20'}

    def run(self):
        handle(self.lottery_type[self.cid], self.cid)


if __name__ == '__main__':
    threads = []
    for i in range(10):
        t = MyThread(i)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print('main thread end')
from io import StringIO
import json
from queue import Queue
from threading import Thread
from xml.etree.ElementTree import Element, ElementTree

import requests

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


class DownloadThread(Thread):
    def __init__(self, lottery_type, index, q):
        Thread.__init__(self)
        self.lottery_type = lottery_type
        self.index = index
        self.q = q

    def download(self):
        print('Download... %s'%self.index)
        url = 'http://f.apiplus.net/%s.json'%self.lottery_type
        response = requests.get(url)
        if response.ok:
            return StringIO(response.content.decode())

    def run(self):
        res = self.download()
        if res:
            self.q.put((res, self.index))


class ConvertToXmlThread(Thread):
    def __init__(self, q):
        Thread.__init__(self)
        self.q = q

    def json_to_xml(self, res, index):
        print('Convert... %s to xml'%index)
        data = json.loads(res.read())['data']
        root = Element('Data')
        for row in data:
            erow = Element('Row')
            root.append(erow)
            for key, value in row.items():
                e = Element(key)
                e.text = str(value)
                erow.append(e)
        et = ElementTree(root)
        et.write('jsons/%s.xml'%index)

    def run(self):
        while True:
            res, index = self.q.get()
            if index == -1:
                break
            if res:
                self.json_to_xml(res, index)


if __name__ == '__main__':
    threads = []
    # for i in range(10):
    #     t = MyThread(i)
    #     t.start()
    #     threads.append(t)
    #
    # for t in threads:
    #     t.join()

    lottery_type = {0: 'dlt-20', 1: 'fc3d-20', 2: 'pl3-20',
                3: 'pl5-20', 4: 'qcl-20', 5: 'qxc-20',
                6: 'ssq-20', 7: 'cqssc-20', 8: 'gd11x5-20',
                9: 'bj11x5-20'}
    q = Queue()
    dthreads = (DownloadThread(lottery_type[i], i, q) for i in range(10))
    cthread = ConvertToXmlThread(q)
    for t in dthreads:
        t.start()
        threads.append(t)
    cthread.start()

    for t in threads:
        t.join()
    q.put((None, -1))

    cthread.join()

    print('main thread end')
from io import StringIO
import json
import os
from pathlib import Path
from queue import Queue
import tarfile
from threading import Thread, Event
from xml.etree.ElementTree import Element, ElementTree

import requests


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
    def __init__(self, q, c_event, t_event):
        Thread.__init__(self)
        self.queue = q
        self.c_event = c_event
        self.t_event = t_event
        self.count = 0

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
            res, index = self.queue.get()
            if index == -1:
                print('convert end')
                self.c_event.set()
                self.t_event.wait() # 必须等待，否则打包线程（守护线程）也会退出
                break
            if res:
                self.json_to_xml(res, index)
                self.count += 1
                if self.count == 5:
                    self.c_event.set()
                    self.t_event.wait()
                    self.t_event.clear()
                    self.count = 0

class TarXmlThread(Thread):
    def __init__(self, c_event, t_event):
        Thread.__init__(self)
        self.count = 0
        self.c_event = c_event
        self.t_event = t_event
        self.setDaemon(True)    # 设置为守护线程，其他线程退出后，守护线程自动退出

    def tarXML(self):
        self.count += 1
        file_path = './jsons/%s.tgz'%self.count
        tf = tarfile.open(file_path, 'w:gz')
        for fname in os.listdir('./jsons'):
            if fname.endswith('.xml'):
                fname = str(Path(__file__).parent/'jsons'/fname)
                tf.add(fname)
                os.remove(str(fname))
        tf.close()

        if not tf.members:
            os.remove(file_path)
        else:
            print('tar success')

    def run(self):
        while True:
            self.c_event.wait()
            self.tarXML()
            self.c_event.clear()
            self.t_event.set()
        print('这句话输出之前，该线程已经跟随其他线程一起退出')


if __name__ == '__main__':
    lottery_type = {0: 'dlt-20', 1: 'fc3d-20', 2: 'pl3-20',
                3: 'pl5-20', 4: 'qcl-20', 5: 'qxc-20',
                6: 'ssq-20', 7: 'cqssc-20', 8: 'gd11x5-20',
                9: 'bj11x5-20'}
    threads = []
    q = Queue()
    e1 = Event()
    e2 = Event()
    dthreads = (DownloadThread(lottery_type[i], i, q) for i in range(10))
    cthread = ConvertToXmlThread(q, e1, e2)
    tarthread = TarXmlThread(e1, e2)

    for t in dthreads:
        t.start()
        threads.append(t)
    cthread.start()
    tarthread.start()

    for t in threads:
        t.join()

    q.put((None, -1))

    cthread.join()

    print('main thread end')
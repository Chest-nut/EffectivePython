import json
from xml.etree.ElementTree import Element, ElementTree

import requests


def download(lottery_type, index):
    print('Download... %s'%index)
    url = 'http://f.apiplus.net/%s.json'%lottery_type
    response = requests.get(url)
    res = json.loads(response.content)
    with open('jsons/%s.json'%lottery_type, 'w') as f:
        json.dump(res, f, separators=[',',':'])

def json_to_xml(lottery_type, index):
    print('Convert... %s to xml'%index)
    with open('jsons/%s.json'%lottery_type, 'r') as f:
        res = json.load(f)
        data = res['data']
        root = Element('Data')
        for row in data:
            erow = Element('Row')
            root.append(erow)
            for key, value in row.items():
                e = Element(key)
                e.text = str(value)
                erow.append(e)
        et = ElementTree(root)
        et.write('jsons/%s.xml'%lottery_type)

def handle(lottery_type, index):
    download(lottery_type, index)
    json_to_xml(lottery_type, index)


if __name__ == '__main__':
    lottery_type = {0: 'dlt-20', 1: 'fc3d-20', 2: 'pl3-20',
                3: 'pl5-20', 4: 'qcl-20', 5: 'qxc-20',
                6: 'ssq-20', 7: 'cqssc-20', 8: 'gd11x5-20',
                9: 'bj11x5-20'}
    for i in range(10):
        handle(lottery_type[i], i)

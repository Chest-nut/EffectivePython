import csv
from xml.etree.ElementTree import Element, ElementTree


def xml_demo(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = reader.__next__()
        root = Element('Data')
        for row in reader:
            erow = Element('Row')
            root.append(erow)
            for tag, text in zip(headers, row):
                e = Element(tag)
                e.text = text
                erow.append(e)
    et = ElementTree(root)
    et.write(filename.replace('csv', 'xml'), encoding='utf-8')


if __name__ == '__main__':
    xml_demo('scores/score1.csv')
    pass

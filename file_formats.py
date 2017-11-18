import csv
from xml.etree.ElementTree import Element, ElementTree

def csv_demo():
    with open('test.csv', 'r') as f:
        reader = csv.reader(f)
        head = reader.__next__()
        with open('new_test.csv', 'w', newline='') as f2:   # newline=''防止出现多余行
            writer = csv.writer(f2)
            writer.writerow(head)
            for line in reader:
                if int(line[0]) > 3:
                    writer.writerow(line)
    print('end')

def xml_demo():
    with open('test.csv', 'r') as f:
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
    et.write('test.xml')


if __name__ == '__main__':
    xml_demo()
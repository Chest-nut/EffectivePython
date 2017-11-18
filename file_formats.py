import csv


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


if __name__ == '__main__':
    csv_demo()
import csv
from random import randint

from thread_process.surname import surname as sname


def random_char():
    head = hex(randint(0xb0, 0xf7))
    head = hex(randint(0xb0, 0xc0))
    body = hex(randint(0xa1, 0xfe))
    # char = f'{head:x}{body:x}'  # ??str类型
    char = (head + body).replace('0x', '')
    char = bytes.fromhex(char).decode('gb2312')
    return char

def generate_fullname():
    # 姓
    l = len(sname) - 1
    surname = sname[randint(0, l)]
    # 名
    flag = randint(1,1)
    if flag:
        firstname = random_char() + random_char()
    else:
        firstname = random_char()
    # 返回姓名
    return surname + firstname

def generate_row():
    row = [generate_fullname(),
           randint(0, 100), randint(0, 100), randint(0, 100)]
    return row

def generate_csv(filename, nrow=1):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for _ in range(nrow):
            writer.writerow(generate_row())
    print('end')

if __name__ == '__main__':
    # for i in range(10):
    #     generate_csv('scores/score%s.csv'%i, 20)
    pass

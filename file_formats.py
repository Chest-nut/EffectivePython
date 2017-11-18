"""操作csv、xml、excel文件"""

import csv
from xml.etree.ElementTree import Element, ElementTree
import xlrd, xlwt
import xlrd.sheet

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

def excel_demo():
    # 向原表中添加总分字段
    rbook = xlrd.open_workbook('demo.xlsx')
    rsheet = rbook.sheet_by_index(0)
    new_col = rsheet.ncols
    rsheet.put_cell(0, new_col, xlrd.XL_CELL_TEXT, '总分', None)
    for row in range(1, rsheet.nrows):
        total_score = sum(rsheet.row_values(row, 1))
        rsheet.put_cell(row, new_col, xlrd.XL_CELL_NUMBER, total_score, None)

    # 将原表中的数据写到新表中并保存
    wbook = xlwt.Workbook()
    wsheet = wbook.add_sheet(rsheet.name)
    style = xlwt.easyxf('align: vertical center, horizontal center')
    for row in range(rsheet.nrows):
        for col in range(rsheet.ncols):
            wsheet.write(row, col, rsheet.cell_value(row, col), style)

    wbook.save('new_demo.xls')  # xlwt模块生成的文件后缀为xls，不能用xlsx

if __name__ == '__main__':
    excel_demo()
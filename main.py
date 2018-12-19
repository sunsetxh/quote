# coding:utf-8
import xlrd
import xlwt
from xlutils import copy
import tkinter.filedialog
import tkinter.messagebox
import os
from tkinter import *
import product


# 设置单元格样式
def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6

    style.font = font
    # style.borders = borders

    return style


def readworkbook(path):
    wk = xlrd.open_workbook(path)  # 读取文件
    table = wk.sheet_by_index(0)  # 获取第一张表格
    nrows = table.nrows  # 获取总行数
    ncols = table.ncols  # 获取总列数
    products = []
    for i in range(nrows):  # 循环所有行
        row = table.row_values(i)  # 获取该行内容为列表
        if isinstance(row[0], float) or isinstance(row[0], int):  # 判断第一个元素是否为编号
            prod = product.Product(row)
            # prod.printprice()
            products.append(prod)
    return products


def writeworkbook(products, oldpath, path=None):
    if path is None:  # 生成文件名
        lst = oldpath.split('.')
        path = lst[0] + '-已报价.' + lst[1]
    rdwb = xlrd.open_workbook(oldpath)
    rds = rdwb.sheet_by_index(0)
    wtwb = copy.copy(rdwb)  # 将旧表复制到新表
    wts = wtwb.get_sheet(0)
    nrows = rds.nrows
    i = 0
    length = len(products)
    for r in range(nrows):
        if rds.cell(r, 0).value == products[i].coding:  # 判断编码
            wts.write(r, 15, products[i].UnitPrice)
            wts.write(r, 16, products[i].TotalPrice)
            wts.write(r, 17, products[i].DiscountPrice)
            i += 1
            if i == length:
                break
    wtwb.save(path)

    tkinter.messagebox.showinfo('通知', '报价已经生成至：' + path)


def browser():
    filename = tkinter.filedialog.askopenfilename(initialdir=os.getcwd(), title="选择文件",
                                                  filetypes=(("xls files", "*.xls"), ("all files", "*.*")))  # 打开文件浏览窗口
    pathEntry.delete(0, 'end')  # 删除文本框内容
    pathEntry.insert(0, filename)  # 将新的路径添加到文本框


def run():
    if len(pathEntry.get()) == 0:  # 判断文本框内是否有内容
        tkinter.messagebox.showwarning('警告', '请先选择文件')
    else:
        products = readworkbook(pathEntry.get())  # 读取产品信息文件
        writeworkbook(products, pathEntry.get())


def center_window(master, w, h):
    # 获取屏幕 宽、高
    ws = master.winfo_screenwidth()
    hs = master.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    master.geometry('%dx%d+%d+%d' % (w, h, x, y))


master = Tk()
master.title('报价')  # 更改窗口标题
center_window(master, 450, 70)
Label(master, text='文件路径').grid(row=0)  # 添加标签
pathEntry = Entry(master, width=50)
pathEntry.grid(row=0, column=1)  # 添加文本框
browserbtn = Button(master, text='浏览', command=browser)
browserbtn.grid(row=0, column=2)  # 添加浏览按钮
runbtn = Button(master, text='生成报价', command=run)
runbtn.grid(row=1, column=1, sticky=W + E + N + S)  # 添加按钮，位于第二行居中

master.mainloop()  # 开启主循环

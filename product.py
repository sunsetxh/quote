# coding=utf-8
class Product:
    def __init__(self, row):
        # 物品编码
        self.coding = row[0]
        # 物品名称
        self.name = row[1]
        # 物品型号
        self.model = row[2]
        # 料号 2=双面板 4=四面板 -1=无法识别
        if row[3][0].__eq__('D'):
            self.pnumber = 2
        elif row[3][0].__eq__('M'):
            self.pnumber = 4
        else:
            self.pnumber = -1
        # 长（mm）
        self.length = row[4] / 1000
        # 宽（mm）
        self.width = row[5] / 1000
        # 板厚（mm）
        self.thickness = float(row[6][0:2])
        # 基材铜厚
        strs = row[7].split('/')
        str1 = strs[int(len(strs) / 2)]
        if str1 == 'H':
            self.CopperThickness = 1.0
        else:
            self.CopperThickness = float(str1)
        # 油墨色 1=绿色 2=蓝色 3=黑色 -1=未知
        if row[8].find("绿色") != -1:
            self.color = 1
        elif row[8].find("蓝色") != -1:
            self.color = 2
        elif row[8].find("黑色") != -1:
            self.color = 3
        else:
            self.color = -1
        # 无铅 0=有铅 1=无铅 2=化金 -1=未知
        if row[9].find("有铅") != -1:
            self.lead = 0
        elif row[9].find("无铅") != -1:
            self.lead = 1
        elif row[9].find("化金") != -1:
            self.lead = 2
        else:
            self.lead = -1
        # 数量
        self.number = row[10]
        # 单价
        self.UnitPrice = 0
        if self.pnumber == 2:
            self.UnitPrice = self.length * self.width * 480
        elif self.pnumber == 4:
            self.UnitPrice = self.length * self.width * 1000
        print(self.UnitPrice)
        if self.thickness > 1.6:
            self.UnitPrice += 80
        if self.CopperThickness > 1:
            self.UnitPrice += 80
        self.UnitPrice = self.UnitPrice
        if self.UnitPrice < 0.3:
            self.UnitPrice = 0.3
        # 总面积
        self.area = self.length * self.width * self.number
        print(self.area)
        if 20 < self.area <= 50:
            self.discount = 0.95
        elif self.area > 50:
            self.discount = 0.925
        else:
            self.discount = 1
        # 金额
        self.TotalPrice = self.UnitPrice * self.number
        # 打折金额
        self.DiscountPrice = self.TotalPrice * self.discount
        # 下单次数
        self.OrderNumber = row[11]

    def printprice(self):
        print(
            '单价：' + self.UnitPrice.__str__() +
            ' 总价：' + self.TotalPrice.__str__() +
            ' 折扣价：' + self.DiscountPrice.__str__() +
            ' 折扣:' + (self.DiscountPrice / self.TotalPrice).__str__() + ' ' + self.discount.__str__())

import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_test_data()
        print("完成初始化")

    def init_ui(self):
        self.ui = uic.loadUi("./各地物价对照.ui")

        # 提取要操作的控件
        # comboBox
        self.location_comboBox = self.ui.comboBox  # 地点
        self.location_transfer_comboBox = self.ui.comboBox_2  # 转换地点

        # lineEdit
        self.item_name_lineEdit = self.ui.lineEdit  # 物价名称

        # pushButton
        self.search_btn = self.ui.pushButton  # 搜索按钮
        self.transfer_btn = self.ui.pushButton_2  # 转换按钮

        # table
        self.table = self.ui.tableWidget  # 结果表

        # 绑定信号与槽函数
        self.search_btn.clicked.connect(self.search)
        self.transfer_btn.clicked.connect(self.transfer)

    def transfer(self):
        """根据表格中搜索出的结果、转换地点，转换信息"""
        # to do 待抽象封装
        location_transfer = self.location_transfer_comboBox.currentText()
        print(location_transfer)
        if location_transfer == "上海":
            transfer_df = self.data_shanghai[
                self.data_shanghai["物价名称"].isin(self.search_df["对应规则"].str.split("_", expand=True)[
                    1])]
            print(transfer_df)
            row_count = transfer_df.shape[0]
            self.table.setRowCount(row_count)
            # 添加数据到表格中
            for row in range(row_count):
                for col in range(len(transfer_df.columns) - 1):
                    item = QTableWidgetItem(str(transfer_df.iloc[row, col]))
                    self.table.setItem(row, col + 3, item)

        elif location_transfer == "北京":
            pass


    def search(self):
        """根据地点、物价名称，搜索物价项目"""
        location = self.location_comboBox.currentText()
        item = self.item_name_lineEdit.text()
        if location == "北京":
            self.search_city_dataframe(self.data_beijing, location, item)
        elif location == "上海":
            self.search_city_dataframe(self.data_shanghai, location, item)

    def search_city_dataframe(self, city_dataframe, location, item):
        """在给定的城市表中搜索数据，并添加数据到表格中"""
        self.search_df = city_dataframe[city_dataframe["物价名称"]
                                        == item].reset_index(drop=True)
        print(self.search_df)
        row_count = self.search_df.shape[0]
        self.table.setRowCount(row_count)
        # 添加数据到表格中
        for row in range(row_count):
            for col in range(len(self.search_df.columns) - 1):
                item = QTableWidgetItem(str(self.search_df.iloc[row, col]))
                self.table.setItem(row, col, item)

    def load_test_data(self):
        """导入北京菜单、上海菜单"""
        self.data_beijing = pd.read_excel("测试资料/北京菜单.xlsx")
        self.data_shanghai = pd.read_excel("测试资料/上海菜单.xlsx")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyWindow()
    w.ui.show()

    app.exec()

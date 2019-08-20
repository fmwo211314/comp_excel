import sys, traceback
from form import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.comments import Comment


class MyPyQT_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.setupUi(self)
        self.excel_expect = ""
        self.excel_actual = ""

    def execute_compare(self):
        if self.excel_actual == "" or self.excel_expect == "":
            self.alert("请选择要比较的Excel文件")
            return

        self.textEdit.setText("比较开始...")
        try:
            self.compareExecute(self.excel_expect, self.excel_actual)
            self.textEdit.append("比较完成，详情请查看\n%s" % self.excel_actual)
            self.alert("执行完成")
        except:
            msg = traceback.format_exc()
            self.textEdit.setText(msg)

    def alert(self, str):
        msg_box = QtWidgets.QMessageBox
        msg_box.information(self, '提示', str, msg_box.Ok)

    def select_expect(self):
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'Excel files(*.xlsx , *.xls)')
        self.lineEdit.setText(openfile_name[0])
        self.excel_expect = openfile_name[0]

    def select_actual(self):
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'Excel files(*.xlsx , *.xls)')
        self.lineEdit_2.setText(openfile_name[0])
        self.excel_actual = openfile_name[0]

    def compareExecute(self, excel_expect, excel_actual):
        wb_expect = load_workbook(excel_expect, data_only=False)
        wb_actual = load_workbook(excel_actual, data_only=False)
        sheet_expect = wb_expect.active
        sheet_actual = wb_actual.active

        list = []
        for row in sheet_expect.rows:
            for cell in row:
                list.append(cell.value)

        fill = PatternFill("solid", fgColor="FF0000")

        for index_row, row in enumerate(sheet_actual.rows):
            for index_column, cell in enumerate(row):
                index = index_row * sheet_actual.max_column + index_column
                if cell.value != list[index]:
                    comment = Comment('预期是：{0},\n实际结果是：{1}'.format(list[index], cell.value), 'lxy')
                    comment.width = 400
                    comment.height = 400
                    cell.comment = comment
                    cell.fill = fill
                    self.textEdit.append(
                        '第{2}行第{3}列，\n预期是：{0},\n实际结果是：{1}'.format(list[index], cell.value, index_row + 1,
                                                                  index_column + 1))

        wb_actual.save(excel_actual)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())

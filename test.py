'''
	1. 异步写log到控件上 因为子线程无法直接控制UI 所以实现原理是
		主线程创建信号和槽函数，子线程发送信号,从而间接操控往UI上写log
'''


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class Winform(QWidget):
	button_clicked_signal = pyqtSignal()

	def __init__(self, parent=None):
		super().__init__()
		self.setWindowTitle("自定义信号和槽函数")
		self.resize(330,50)
		btn = QPushButton("关闭", self)
		# 连接信号与槽函数
		btn.clicked.connect(self.btn_clicked)
		# 接收信号，连接到自定义槽函数
		self.button_clicked_signal.connect(self.btn_close)
		
	def btn_clicked(self):
		# 发送信号
		self.button_clicked_signal.emit()

	def btn_close(self):
		self.close()
pass


if __name__ == '__main__':
	app = QApplication(sys.argv)
	win = Winform()
	win.show()
	sys.exit(app.exec_())
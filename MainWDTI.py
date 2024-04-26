'''
    1. 异步写log到控件上 因为子线程无法直接控制UI 所以实现原理是
        主线程创建信号和槽函数，子线程发送信号,从而间接操控往UI上写log
'''
import sys,os,time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import Ui_WDTI as ui


class ThreadEvent:
    def __init__(self,signal,into_path,out_path):
        self.signal = signal
        self.into_path = into_path
        self.out_path = out_path
    pass
    def main(self):
        self.signal.emit('0');time.sleep(1)
        self.signal.emit('开始处理--->Begin!');time.sleep(0.1)
        dat_list = self.Dat_files(self.into_path)  # 把路径文件夹下的dat文件以列表呈现
        lens = len(dat_list)
        if lens == 0:
            # print('没有dat文件')
            self.signal.emit(str('没有dat文件'));time.sleep(0.1)
            exit()

        num = 0
        for dat_file in dat_list:  # 逐步读取文件
            num += 1
            temp_path = self.into_path + '/' + dat_file  # 拼接路径：微信图片路径+图片名
            dat_file_name = dat_file[:-4]  # 截取字符串 去掉.dat
            self.imageDecode(temp_path, dat_file_name, self.out_path)  # 转码函数
            value = int((num / lens) * 100)             # 显示进度
            # print('正在处理--->{}%'.format(value))
            self.signal.emit('正在处理--->{}%'.format(value));time.sleep(0.1)
        pass
        self.signal.emit('处理结束--->End!');time.sleep(0.1)
        self.signal.emit('1');time.sleep(0.1)
    pass
    def Dat_files(self,file_dir):
        """
        :param file_dir: 寻找文件夹下的dat文件
        :return: 返回文件夹下dat文件的列表
        """
        dat = []
        for files in os.listdir(file_dir):
            if os.path.splitext(files)[1] == '.dat':
                dat.append(files)
        return dat
    pass
    def imageDecode(self,temp_path, dat_file_name, out_path):
        dat_read = open(temp_path, "rb")  # 读取.bat 文件
        xo, j = self.Format(temp_path)  # 判断图片格式 并计算返回异或值 函数

        if j == 1:
            mat = '.png'
        elif j == 2:
            mat = '.gif'
        else:
            mat = '.jpg'

        out = out_path + '/' + dat_file_name + mat  # 图片输出路径
        png_write = open(out, "wb")  # 图片写入
        dat_read.seek(0)  # 重置文件指针位置

        for now in dat_read:  # 循环字节
            for nowByte in now:
                newByte = nowByte ^ xo  # 转码计算
                png_write.write(bytes([newByte]))  # 转码后重新写入

        dat_read.close()
        png_write.close()
    pass
    def Format(self,f):
        """
        计算异或值
        各图片头部信息
        png：89 50 4e 47
        gif： 47 49 46 38
        jpeg：ff d8 ff
        """
        dat_r = open(f, "rb")

        try:
            a = [(0x89, 0x50, 0x4e), (0x47, 0x49, 0x46), (0xff, 0xd8, 0xff)]
            for now in dat_r:
                j = 0
                for xor in a:
                    j = j + 1  # 记录是第几个格式 1：png 2：gif 3：jpeg
                    i = 0
                    res = []
                    now2 = now[:3]      # 取前三组判断
                    for nowByte in now2:
                        res.append(nowByte ^ xor[i])
                        i += 1
                    if res[0] == res[1] == res[2]:
                        return res[0], j
        except:
            pass
        finally:
            dat_r.close()
    pass

pass

class UpdateThread(QThread):
    update_data = pyqtSignal(str)
    def __init__(self,into_path,out_path):
        super(UpdateThread,self).__init__()
        self.into_path = into_path
        self.out_path = out_path
    pass
    def run(self):
        te = ThreadEvent(self.update_data,self.into_path,self.out_path)
        te.main()
    pass
pass
class Winform(QMainWindow,ui.Ui_Form):
    def __init__(self, parent=None):
        super(Winform,self).__init__(parent)
        self.setupUi(self)
        
    def datToPic(self):
        dat_path = self.lineEdit.text()
        desk_path = self.lineEdit_2.text()
        self.subThread = UpdateThread(dat_path,desk_path)
        self.subThread.update_data.connect(self.textUpdate)
        self.subThread.start()
    pass
    def textUpdate(self, data):
        if data == '0':
            self.pushButton.setEnabled(False)
            return
        elif data == '1':
            self.pushButton.setEnabled(True)
            return
        pass
        self.textBrowser.append(data)   #文本框逐条添加数据
        self.textBrowser.moveCursor(self.textBrowser.textCursor().End)  #文本框显示到底部
    pass
pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Winform()
    win.show()
    sys.exit(app.exec_())
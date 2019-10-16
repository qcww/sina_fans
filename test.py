#coding=utf-8

from tkinter import *
import threading

class 界面类(Tk):
    def __init__(self):
        super().__init__()
        self.title('试验')
        self.int_n = IntVar()
        Label(self, textvariable=self.int_n, padx=250, pady=200).pack()
        self.mythread = threading.Thread(target=self.工作线程, name='线程_1')
        self.cond = threading.Condition() # 锁
        self.mythread.start()
        
    def 工作线程(self):
        n=0
        while True:
            with self.cond: # 锁
                n = (n+1)%100
                self.int_n.set(n) # 修改变量
                # self.int =
                self.cond.wait(5) # 可以改为 20秒

            
if __name__ == '__main__':
    界面 = 界面类()
    界面.mainloop()

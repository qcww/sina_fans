import tkinter as tk
import tkinter.messagebox
import time
import configparser
from sinafans import SinaFans
from tkinter import simpledialog
from tkinter import StringVar

window = tk.Tk()
 
window.title('添加新浪待采集粉丝用户')
 
window.geometry('400x270')  # 这里的乘是小x
 
# 第4步，在图形界面上设定输入框控件entry并放置控件
# tk.Label(window, text='昵称', font=('Arial', 14), ).place(x=30, y=20, anchor='nw')
# tk.Entry(window, show=None, font=('Arial', 14)).place(x=90, y=20)

# tk.Label(window, text='标签', font=('Arial', 14), ).place(x=30, y=70, anchor='nw')
# tk.Entry(window, show=None, font=('Arial', 14)).place(x=90, y=70)
_cookie = ''
sb = tk.Scrollbar(window)
sb.pack(side=tk.RIGHT,fill=tk.Y)
# 日志显示框与下滑块
lb = tk.Listbox(window, yscrollcommand=sb.set,width=36,height=12)
lb.insert(tk.END, '点击添加按钮添加粉丝')
lb.place(x=15, y=15)
sb.config(command=lb.yview)
script = SinaFans(window,lb)

select_label = StringVar()
select_label.set(script.collect_group)

def add_user():
    global script
    global submenu
    sc_user = simpledialog.askstring('添加待采集粉丝','')
    script.add_user_list(sc_user)

def scrap_user():
    # window.title('添加')
    global script
    _cookie = script.get_config('login','cookie')
    if _cookie != '':
        script.start()
        # lb.insert(tk.ACTIVE,'你好')
    else:
        login()

def login():
    global _cookie
    global script
    _cookie = simpledialog.askstring('登录账号','')
    script.set_config('login','cookie',_cookie)

def add_lable():
    global script
    lable = simpledialog.askstring('添加标签','')
    script.add_label(lable)
    submenu.add_radiobutton(label=lable,command=set_label,
                variable=select_label, value=lable)

def set_label():
    global select_label
    global script
    script.set_default_label(select_label.get())

def add_sub_menu():
    global script
    global select_label
    label = script.get_config_options('collect')
    for lab in label:
        submenu.add_radiobutton(label=lab,command=set_label,
                variable=select_label, value=lab)

tk.Button(window, text="添加", width=10, height=1, command=add_user).place(x=290, y=15)
tk.Button(window, text="采集", width=10, height=1, command=scrap_user).place(x=290, y=50)

menubar = tk.Menu(window)

editmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='设置', menu=editmenu)
editmenu.add_command(label='添加标签',command=add_lable)

submenu = tk.Menu(editmenu,tearoff=0)
editmenu.add_cascade(label='设置标签', menu=submenu, underline=0)
add_sub_menu()

filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='登录', menu=filemenu)
filemenu.add_command(label='登录新浪', command=login)

window.config(menu=menubar)

        
# 第5步，主窗口循环显示
window.resizable(0,0)
window.mainloop()
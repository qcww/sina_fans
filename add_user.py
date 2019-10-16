import tkinter as tk
import tkinter.messagebox

window = tk.Tk()
 
window.title('添加新浪待采集粉丝用户')
 
window.geometry('400x270')  # 这里的乘是小x
 
# 第4步，在图形界面上设定输入框控件entry并放置控件
# tk.Label(window, text='昵称', font=('Arial', 14), ).place(x=30, y=20, anchor='nw')
# tk.Entry(window, show=None, font=('Arial', 14)).place(x=90, y=20)

# tk.Label(window, text='标签', font=('Arial', 14), ).place(x=30, y=70, anchor='nw')
# tk.Entry(window, show=None, font=('Arial', 14)).place(x=90, y=70)

sb = tk.Scrollbar(window)
sb.pack(side=tk.RIGHT,fill=tk.Y)
# sb.place(x=270)
lb = tk.Listbox(window, yscrollcommand=sb.set,width=36,height=12)
lb.insert(tk.END, '点击添加按钮添加粉丝')
lb.place(x=15, y=15)
sb.config(command=lb.yview)


def hit_me():
    window.title('添加')
    lb.insert(tk.ACTIVE,'你好')

tk.Button(window, text="添加", width=10, height=1, command=hit_me).place(x=290, y=15)
tk.Button(window, text="采集", width=10, height=1, command=hit_me).place(x=290, y=50)

        
# 第5步，主窗口循环显示
window.resizable(0,0)
window.mainloop()
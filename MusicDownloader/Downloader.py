from tkinter import *
from platforms import *
import threading
from tkinter import messagebox
import os

class Download_Thread(threading.Thread):
	def __init__(self, *args, **kwargs):
		super(Download_Thread, self).__init__(*args, **kwargs)
		self.__pause = threading.Event()
		self.__pause.clear()
		self.__running = threading.Event()
		self.__running.set()
		self.flag = False
		self.engine = None
		self.songname = None
		self.downnum = 1
		self.savepath = './results'
	def run(self):
		while self.__running.isSet():
			self.__pause.wait()
			self.flag = True
			if self.engine == '1':
				self.show_start_info()
				try:
					downednum = qq.qq().get(self.songname, downnum=self.downnum, savepath=self.savepath)
					self.show_end_info(downednum, savepath=self.savepath)
				except:
					title = '资源不存在'
					msg = '所要下载的资源不存在！'
					messagebox.showerror(title, msg)
			elif self.engine == '2':
				self.show_start_info()
				try:
					downednum = kugou.kugou().get(self.songname, downnum=self.downnum, savepath=self.savepath)
					self.show_end_info(downednum, savepath=self.savepath)
				except:
					title = '资源不存在'
					msg = '所要下载的资源不存在！'
					messagebox.showerror(title, msg)
			else:
				title = '解析失败'
				msg = '平台选项参数解析失败！'
				messagebox.showerror(title, msg)
			self.pause()
	def pause(self):
		self.__pause.clear()
	def resume(self):
		self.__pause.set()
	def stop(self):
		self.__running.clear()
	def show_start_info(self):
		title = '开始下载'
		msg = '搜索平台: {}\n已开始下载{}，请耐心等待。'.format(self.engine, self.songname)
		messagebox.showinfo(title, msg)	
	def show_end_info(self, downednum, savepath='./results'):
		title = '下载成功'
		msg = '{}下载成功, 共{}歌曲被下载。\n歌曲保存在{}。'.format(self.songname, downednum, savepath)
		messagebox.showinfo(title, msg)
#声明一个下载音乐的线程
t_download = Download_Thread()
#下载歌曲功能
def downloader(options, op_engine_var, en_songname_var, en_num_var):
	if t_download.flag is False:
		t_download.start()
	try:
		engine = str(options.index(str(op_engine_var.get())) + 1)
		songname = str(en_songname_var.get())
		downnum = int(en_num_var.get())
	except:
		title = '输入错误'
		msg = '歌曲名或歌曲下载数量输入错误！'
		messagebox.showerror(title, msg)
		return None
	t_download.engine = engine
	t_download.songname = songname
	t_download.downnum = downnum
	t_download.resume()
#显示作者
def show_author():
	title = '关于作者'
	msg = '作者: Ji Dehao, Yan Ruyi and Jackie'
	messagebox.showinfo(title, msg)
#退出程序
def stopapp(root):
	t_download.stop()
	root.quit()
	root.destroy()
#创建下载器
def MusicDownloader(options):
	root = Tk()
	root.title('音乐下载器')
	root.resizable(False, False)
	root.geometry('480x368+400+120')
	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=False)
	filemenu.add_command(label='Author', command = show_author,font=('楷体', 10))
	menubar.add_cascade(label="Menu", menu=filemenu)
	root.config(menu=menubar)
	lb_songname = Label(root, text='歌名:   ', font=('楷体', 10), bg='white')
	lb_songname.place(relx=0.1, rely=0.05, anchor=CENTER)
	en_songname_var = StringVar()
	en_songname = Entry(root, textvariable=en_songname_var, width=15, fg='gray', relief=GROOVE, bd=3)
	en_songname.insert(0, '出山')
	lb_num = Label(root, text='下载数量:', font=('楷体', 10), bg='white')
	lb_num.place(relx=0.1, rely=0.15, anchor=CENTER)
	en_num_var = StringVar()
	en_num = Entry(root, textvariable=en_num_var, width=15, fg='gray', relief=GROOVE, bd=3)
	en_num.insert(0, '1')
	en_num.place(relx=0.3, rely=0.15, anchor=CENTER)
	en_songname.place(relx=0.3, rely=0.05, anchor=CENTER)
	lb_engine = Label(root, text='搜索平台:', font=('楷体', 10), bg='white')
	lb_engine.place(relx=0.1, rely=0.25, anchor=CENTER)
	op_engine_var = StringVar()
	op_engine_var.set(options[0])
	op_engine = OptionMenu(root, op_engine_var, *options)
	op_engine.place(relx=0.3, rely=0.25, anchor=CENTER)
	bt_download = Button(root, text='搜索并下载', bd=2, width=15, height=2, command=lambda: downloader(options, op_engine_var, en_songname_var, en_num_var), font=('楷体', 10))
	bt_download.place(relx=0.3, rely=0.40, anchor=CENTER)
	bt_quit = Button(root, text='退出程序', bd=2, width=15, height=2, command=lambda: stopapp(root), font=('楷体', 10))
	bt_quit.place(relx=0.3, rely=0.55, anchor=CENTER)
	root.mainloop()

options = ["1.QQ音乐", "2.酷狗音乐"]
MusicDownloader(options)
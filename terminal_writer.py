import subprocess
from sys import executable
from subprocess import Popen #, CREATE_NEW_CONSOLE

import Tkinter as tk
from ScrolledText import ScrolledText

def demo_label():
	# demo of labe outputters.
	# note: the main problem here is that label objects don't support scrolling. so you can work around this by placing a HUGE label
	# on a small frame and scroll the frame... or you can use a text object (or you can replace the label text rather than appending it).
	L = Outputter_lbl()
	L.title('Label based outputter')
	for j in xrange(250):
		L.writeln("writing some text: %d" % j)
	#
	# write a long string (to see how wrapping works):1
	L.write('\n\n')
	L.writeln('now, write a long string, to see how wrapping goes...')
	L.write(', '.join([str(x) for x in range(250)]))
	L.writeln()
	L.writeln('done...')
	
	
	#return handle
	
	return L

def demo_text():
	T=Outputter_tk()
	T.title('Text based outputter')
	
	T1=Outputter_tk()
	T1.title('Another outputter')
	#
	for j in xrange(250):
		T.writeln("writing some text: %d" % j)
	#
	# write a long string (to see how wrapping works):1
	T.write('\n\n')
	T.writeln('now, write a long string, to see how wrapping goes...')
	T.write(', '.join([str(x) for x in range(250)]))
	T.writeln()
	T.writeln('done...')
	
	T1.writeln('this is another outputter instance.')
	T1.writeln('it should work exactly the same as its brother.')
	
	return T

##################################
##################################

class Outputter_text(tk.Text):
	# this is a pretty simple script, so we'll leave it here for reference, but it suffers some problems (don't recall exactly what they are
	# at this time). see the outputter(tk.Tk) based classes below...
	#
	def __init__(self, master=None, width=50, height=50):
		#S = super(outputter_text, self)
		#S.__init__(master=master, width=width, height=height)
		
		tk.Text.__init__(self, master=master, width=width, height=height)
		self.pack()
		
		#self.grid()
		#self.createWidgets()
		#
		pass
	#
	def write(self, s=''):
		self.insert(tk.INSERT, s)
		self.pack()
	def writeln(self, s=''):
		self.write('%s\n' % s)
	#
	def createWidgets(self):
		self.quitButton = tk.Button(self, text='Quit',command=self.quit)
		self.quitButton.grid()
	


class Outputter_lbl(tk.Tk):
	'''
	# outputter class that uses a label object. this is nice because the label text is immutable, but i'm not sure it 
	# can be cut and pasted either.
	'''
	# this is mostly from:
	# http://stackoverflow.com/questions/24707308/get-command-window-output-to-display-in-widget-with-tkinter
	# use an immutable label object for text output.
	def __init__(self, master=None, x_size=512, y_size=512, title=None):
		# don't know what we're doing with this yet...
		tk.Tk.__init__(self,master)
		self.x_size=x_size
		self.y_size=y_size
		#
		self.parent=master
		if title!=None: self.wm_title(str(title))
		self.geometry('%sx%s' % (x_size, y_size))
		#
		#self.grid()
		self.createWidgets()
		#
		#self.write('')
		#self.set_wrap()
		self.initialized=0
	#
	def createWidgets(self):
		#
		self.text_var = tk.StringVar()
		self.display = tk.Label(master=self, textvariable=self.text_var, bg='yellow', fg='blue', justify=tk.LEFT, text='', width=25, height=10)
		self.display.pack(anchor="w", fill=tk.BOTH, expand=1)
		#
		self.btn_wrap = tk.Button(self, text='wrap', command=self.set_wrap)
		self.btn_wrap.pack(anchor="w")
		#
		self.btn_quit = tk.Button(self, text='Close', command=self.destroy)
		self.btn_quit.pack(anchor='w')
		
		#self.display.pack(fill=tk.BOTH, expand=1)
		#
	#
	def write(self, input_str=''):
		if self.initialized==0:
			# for some reason, the set_wrap() does not run properly until afet __init__ finishes.
			self.set_wrap()
			self.initialized=1
		#
		txt = self.text_var.get()
		self.text_var.set(txt + input_str)
	#
	def writeln(self, input_str=''):
		self.write(input_str + '\n')
	#
	def set_wrap(self, wrap_len=None):
		if wrap_len==None: wrap_len=self.display.winfo_width()
		self.display.config(wraplength=wrap_len)
		#

class Outputter_tk(tk.Tk):
	'''
	# outputter class that uses a Text() object. The text object is mutable, you can  you can cut and paste from the box, which is nice, but you
	# can also inadvertently delete text... which can be bad. as noted below, configure(state='DISABLED') can be used to disable editing,
	# but it also shutd down writing (insert() ), so it will be necessary to toggle this on/off as needed if we want a 'safe' text box.
	'''
	# this is mostly from:
	# http://stackoverflow.com/questions/24707308/get-command-window-output-to-display-in-widget-with-tkinter
	def __init__(self, master=None, x_size=512, y_size=512, title=None):
		# don't know what we're doing with this yet...
		tk.Tk.__init__(self,master)
		self.parent=master
		if title!=None: self.wm_title(str(title))
		self.geometry('%sx%s' % (x_size, y_size))
		#
		#self.grid()
		self.createWidgets()
		#
		#self.display.insert(tk.INSERT, "initial text")
	
	def write(self, input_str=''):
		self.text_var.set(input_str)
		self.display.insert(tk.END, self.text_var.get())
	#
	def writeln(self, input_str=''):	
		self.write(input_str + '\n')
	
	def createWidgets(self):
		#self.quitButton = tk.Button(self, text='Quit',command=self.quit)
		#self.quitButton.grid()
		
		#self.display = tk.Text(master=self, bg='yellow', fg='blue')
		self.display = ScrolledText(master=self, bg='yellow', fg='blue')
		self.display.pack(anchor="w", fill=tk.BOTH, expand=1)
		#
		self.text_var = tk.StringVar()
		#self.entry=tk.Entry(self, textvariable=self.text_var, bg='cyan')		# this is an input type text-box (i'm guessing a 1-line text).
																				# based on the sample source code, input text would go here, then
																				# you'd click an "add" button and it would append the big text box.
		#self.entry.pack(anchor='w')
		#
		self.btn_quit = tk.Button(self, text='Close', command=self.destroy)
		self.btn_quit.pack(anchor='w')
		#
		#self.btn_disable = tk.Button(self, text='enable', command=self.toggle_disable())
		#self.btn_disable.pack(anchor="w")
		#
		# this is (basically) how to add a scroll-bar to a text box, except it does not handle the length (height) of the bar correctly.
		#self.scroller = tk.Scrollbar(self.display, command=self.display.yview)
		#self.scroller.grid(row=0, column=1, sticky='nsew')
		#self.display['yscrollcommand'] = self.scroller.set
	#
	#
	#def toggle_disable(self):
	# 	# never mind. this is a little more complicated than i want to get into. set state='DISABLED' to restrict editing of the text file contents.
	#   # however, this also disables indert, etc. (aka, writing). so, we can do this, but then we need to keep track of the enabled/disabled
	# state, enable to write, then return to the user selected state between writes.
	#	if self.display

'''
class Base(object):
	def __init__(self):
		print "Base created"

class ChildA(Base):
	def __init__(self):
		Base.__init__(self)

class ChildB(Base):
	def __init__(self):
		super(ChildB, self).__init__()
'''

from Tkinter import *
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
from os import system, startfile
from msr_date_conv import *

class MyApp:
	def __init__(self, parent):
		self.myParent = parent
		#self.myParent.geometry("640x400")
		
		# Formatting variables
		obj_width = 12
		
		obj_padx = '2m'
		obj_pady = '1m'
		
		obj_frame_padx = '3m'
		obj_frame_pady = '2m'
		obj_frame_ipadx = '3m'
		obj_frame_ipady = '1m'
		
		self.mainFrame = Frame(parent)
		self.mainFrame.grid()
		
		# self.head_frame = Frame(self.mainFrame,borderwidth=1,relief=RIDGE)
		# self.head_frame.pack(
			# side = TOP,
			# expand = YES,
			# fill=BOTH
			# )
			
		# self.date_frame = Frame(self.mainFrame,borderwidth=1,relief=RIDGE)
		# self.date_frame.pack(
			# side = TOP,
			# expand = NO,
			# fill=NONE,
			# )
		
		# self.ffs_frame = Frame(self.mainFrame,borderwidth=1,relief=RIDGE)
		# self.ffs_frame.pack(
			# side = TOP,
			# expand = YES,
			# fill=BOTH,
			# )
			
		# self.crt_frame = Frame(self.mainFrame,borderwidth=1,relief=RIDGE)
		# self.crt_frame.pack(
			# side = TOP,
			# expand = YES,
			# fill=BOTH,
			# )
			
		# self.bottom_frame = Frame(self.mainFrame,borderwidth=1,relief=RIDGE)
		# self.bottom_frame.pack(
			# side = TOP,
			# expand = YES,
			# fill=BOTH,
			# )
			
		self.header_text = "MSR FILE GENERATOR"
		self.header = Label(self.mainFrame, text=self.header_text)
		self.header.grid(row=0,columnspan=4)
		
		self.date_label = Label(self.mainFrame, text="Select Month/Year: ")
		self.date_label.grid(row=1,column=0)
		
		self.select_month = Spinbox(self.mainFrame, from_=1, to=12,width=2)
		self.select_month.grid(row=1,column=1)
		
		self.slash = Label(self.mainFrame, text="/")
		self.slash.grid(row=1,column=2)
		
		self.select_year = Spinbox(self.mainFrame, from_=2015, to=2100, width=4)
		self.select_year.grid(row=1,column=3)
		
		
		
		# --- FFS Frame
		# self.ffs_frame_1 = Frame(self.ffs_frame)
		# self.ffs_frame_1.pack(side=TOP)
		
		# self.ffs_frame_2 = Frame(self.ffs_frame)
		# self.ffs_frame_2.pack(side=TOP)

		# self.ffs_frame_3 = Frame(self.ffs_frame)
		# self.ffs_frame_3.pack(side=TOP)
		
		self.ffs_head = Label(self.mainFrame,text='FFS Files')
		self.ffs_head.grid(row=2,columnspan=4)
		
		self.ffs_profile_label = Label(self.mainFrame,text='Load profile data: ',width=20)
		self.ffs_profile_label.grid(row=3,column=0)
		
		self.ffs_profile_button = Button(self.mainFrame, command=self.ffs_profile_buttonClick)
		self.ffs_profile_button.configure(text="Click Here",width=obj_width)
		self.ffs_profile_button.grid(row=3,column=1)
		
		self.ffs_services_label = Label(self.mainFrame,text='Load services data: ',width=20)
		self.ffs_services_label.grid(row=4,column=0)
		
		self.ffs_services_button = Button(self.mainFrame, command=self.ffs_services_buttonClick)
		self.ffs_services_button.configure(text='Click here',width=obj_width)
		self.ffs_services_button.grid(row=4,column=1)
		
		# --- CRT Frame --- #
		# self.crt_frame_1 = Frame(self.crt_frame)
		# self.crt_frame_1.pack(side=TOP)
		
		# self.crt_frame_2 = Frame(self.crt_frame)
		# self.crt_frame_2.pack(side=TOP)

		# self.crt_frame_3 = Frame(self.crt_frame)
		# self.crt_frame_3.pack(side=TOP)
		
		self.crt_head = Label(self.mainFrame,text='CRT Files')
		self.crt_head.grid(row=5,columnspan=2)
		
		self.crt_profile_label = Label(self.mainFrame,text='Load profile data: ',width=20)
		self.crt_profile_label.grid(row=6,column=0)
		
		self.crt_profile_button = Button(self.mainFrame, command=self.crt_profile_buttonClick,width=obj_width)
		self.crt_profile_button.configure(text="Click Here")
		self.crt_profile_button.grid(row=6,column=1)
		
		self.crt_services_label = Label(self.mainFrame,text='Load services data: ',width=20)
		self.crt_services_label.grid(row=7,column=0)
		
		self.crt_services_button = Button(self.mainFrame, command=self.crt_services_buttonClick,width=obj_width)
		self.crt_services_button.configure(text='Click here')
		self.crt_services_button.grid(row=7,column=1)
		
		# --- Bottom Frame --- #
		
		self.left_bottom = Frame(self.mainFrame, borderwidth=1,relief=RIDGE)
		self.left_bottom.grid()
		
		self.right_bottom = Frame(self.mainFrame,borderwidth=1,relief=RIDGE)
		self.right_bottom.grid()
		
		self.dest_label = Label(self.left_bottom, text="Select Destination")
		self.dest_label.grid(row=0)
		
		self.dest_button = Button(self.left_bottom, command=self.dest_buttonClick)
		self.dest_button.configure(text='Click here')
		self.dest_button.grid(row=1)
		
		self.run_button = Button(self.right_bottom, command=self.run_buttonClick)
		self.run_button.configure(text='RUN!',height=2,width=14)
		#self.run_button.grid()
		
		self.ffs_services_clicked = False
		self.ffs_profile_clicked = False
		self.crt_profile_clicked = False
		self.crt_services_clicked = False
		self.dest_button_clicked = False
		
	def run_button_refresh(self):
		if self.ffs_profile_clicked and self.ffs_services_clicked and self.crt_profile_clicked and self.crt_services_clicked and self.dest_button_clicked:
			self.run_button['background'] = 'green'	
			self.run_button.grid()
			
	def ffs_profile_buttonClick(self):
		self.ffs_profile_file = askopenfilename()
		self.ffs_profile_clicked = True
		self.run_button_refresh()	
		
	def ffs_services_buttonClick(self):
		self.ffs_services_file = askopenfilename()
		self.ffs_services_clicked = True
		self.run_button_refresh()
		
	def crt_profile_buttonClick(self):
		self.crt_profile_file = askopenfilename()
		self.crt_profile_clicked = True
		self.run_button_refresh()
		
	def crt_services_buttonClick(self):
		self.crt_services_file = askopenfilename()
		self.crt_services_clicked = True
		self.run_button_refresh()
		
	def dest_buttonClick(self):
		self.dest_location = askdirectory()
		self.dest_button_clicked = True
		self.run_button_refresh()
		
	def run_buttonClick(self):
		self.msr_begin = begin_month(self.select_month.get(),self.select_year.get())
		
		self.msr_end = last_month(self.select_month.get(),self.select_year.get())
		#print self.select_month.get()
		system("msr_2.py %s %s %s %s %s" % (self.msr_begin, self.msr_end, self.ffs_profile_file, self.ffs_services_file, '2'))
		system("msr_2.py %s %s %s %s %s" % (self.msr_begin, self.msr_end, self.crt_profile_file, self.crt_services_file, '1'))
		
		
		msr_dest_file = "%s/PW%sms.dat" % (self.dest_location,year_month(self.select_month.get(),self.select_year.get()))
		msr_dest = open(msr_dest_file, 'w')
		ffs_file = open("MSR_FFS_%s.txt" % year_month(self.select_month.get(),self.select_year.get()),'r')
		crt_file = open("MSR_CRT_%s.txt" % year_month(self.select_month.get(),self.select_year.get()),'r')
		
		for x in ffs_file.readlines():
			msr_dest.write(x)
		for x in crt_file.readlines():
			msr_dest.write(x)
		
		msr_dest.close()
		ffs_file.close()
		crt_file.close()
		
		startfile(msr_dest_file)
		
root = Tk()
root.wm_title("MSR File Generator")
myapp = MyApp(root)
root.mainloop()
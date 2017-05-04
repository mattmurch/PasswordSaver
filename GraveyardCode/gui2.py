from Tkinter import Tk, Frame, Label, Button, Entry, Listbox, END, StringVar

import app

TITLE_FONT = ("Helvetica", 18, "bold")

class TKPage(Tk):

	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)

		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		container = Frame(self)
		self.centerWindow()
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		for F in (LoginPage, PageOne):
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.frames[page_name] = frame

			# put all of the pages in the same location;
			# the one on the top of the stacking order
			# will be the one that is visible.
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("LoginPage")

	def show_frame(self, page_name):
		'''Show a frame for the given page name'''
		frame = self.frames[page_name]
		frame.tkraise()
		
	def centerWindow(self):
		w = 600
		h = 450
		sw = self.winfo_screenwidth()
		sh = self.winfo_screenheight()
		x = (sw - w)/2
		y = (sh - h)/2
		self.geometry('%dx%d+%d+%d' % (w, h, x, y))


class LoginPage(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		#Username and Password Entry
		loginpage = Frame(self)
		loginpage.pack(expand=1)
		lbl1 = Label(loginpage, text="Username", width=8, background="#600").pack(fill='x')
		self.username_entry = Entry(loginpage)
		self.username_entry.pack(fill='x')
		self.username_entry.focus()
		lbl2 = Label(loginpage, text="Password", width=8, background="#600").pack(fill='x')
		self.password_entry = Entry(loginpage)
		self.password_entry.pack(fill='x')

		#Quit and Okay Buttons
		okButton = Button(loginpage, text="Login", command=self.loginButtonClicked)
		okButton.pack()
		okButton.bind("<Return>", lambda x: self.loginButtonClicked())
		quitButton = Button(loginpage, text="Quit", command=self.quit)
		quitButton.pack(padx=5, pady=5)
		quitButton.bind("<Return>", lambda x: self.quit())
		
	def loginButtonClicked(self):
		username = self.username_entry.get()
		password = self.password_entry.get()
		if username == 'Matt' and password == 'holla':
			self.controller.show_frame("PageOne")

class PageOne(Frame):

	def whichSelected(self):
		print self.clist.curselection()
		return self.names[int(self.clist.curselection()[0])]
		
	def loadEntry(self):
		self.nameVar.set(self.whichSelected())

	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		self.nameVar = StringVar()
		self.p_numberVar = StringVar()
		
		#Page Title
		label = Label(self, text="My Contacts", font=TITLE_FONT)
		label.pack(side="top", fill="x", pady=10)
		
		#Selection Display
		self.disp_un_entry = Entry(self, textvariable=self.nameVar)
		self.disp_un_entry.pack(fill='x')
		#~ self.disp_pass_entry = Entry(self, text="<<ListboxSelect>>")
		#~ self.disp_pass_entry.pack(fill='x')
		
		#Add Button
		#~ addbtn = Button(self, text="Add", command=app.add_new_contact(
		
		#Delete Button
		
		
		#Update Button
		
		#Load Button
		loadbtn = Button(self, text="Load", command=self.loadEntry)
		loadbtn.pack()
		
		#Display Contacts from DB
		self.clist = Listbox(self)
		self.clist.pack(fill='x')
		self.names = app.search_all()
		for name in self.names:
			self.clist.insert(END, name)
		
		#Returnt to Login Button
		button = Button(self, text="Go to the start page", command=lambda: controller.show_frame("LoginPage"))
		button.pack()

if __name__ == "__main__":
	app = TKPage()
	app.mainloop()

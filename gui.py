from Tkinter import Tk, BooleanVar, Checkbutton, BOTH, Label, RIGHT, RAISED, Text, TOP, X, N, LEFT, W, E, S
from ttk import Button, Style, Frame, Entry
from PIL import Image, ImageTk


class TKPage(Frame):
	
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.initUI()
		
	def initUI(self):
		self.parent.title("Login")
		self.pack(fill=BOTH, expand=1)
		self.centerWindow()
		self.style = Style()
		self.style.theme_use("default")
		self.style.configure("TFrame", background="#333")
		
		#Username and Password Entry
		loginpage = Frame(self)
		loginpage.pack(expand=1)
		lbl1 = Label(loginpage, text="Username", width=8, background="#600").pack(fill='x')
		entry1 = Entry(loginpage).pack(fill='x')
		lbl2 = Label(loginpage, text="Password", width=8, background="#600").pack(fill='x')
		entry2 = Entry(loginpage).pack(fill='x')

		#Quit and Okay Buttons
		okButton = Button(loginpage, text="Login")
		okButton.pack()
		quitButton = Button(loginpage, text="Quit", command=self.quit)
		quitButton.pack(padx=5, pady=5)
		
	#~ def loginButtonClicked(self):
		#~ username = self.entry1.get()
		#~ password = self.entry2.get()
		#~ if username == 'Matt' and password == 'pooperscooper':
			#~ #do something
		#~ else:
			#~ #do something else
	
	def centerWindow(self):
		w = 600
		h = 450
		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()
		x = (sw - w)/2
		y = (sh - h)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
		
def main():
	root = Tk()
	app = TKPage(root)
	root.mainloop()
	
if __name__ == '__main__':
	main()

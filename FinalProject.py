from tkinter import *
from tkinter import ttk
from Shape import *

class FinalProject(object):
	shape_file_name = 'shape_file.shp'

	def __init__(self):
		# Create main window
		self.root = Tk()
		self.root.title('Shapes')

		# Create canvas
		self.canvas = Canvas(self.root, width=900, height=900, bg='#bda368')
		self.canvas.grid(row=0, column=0)

		# Create controls frame
		self.controls = Frame(self.root)
		self.controls.grid(row=0, column=1)

		# Create shape type selector
		self.select_shape = ttk.Label(self.controls, text='Select Shape:')
		self.select_shape.grid(row=0, column=0, sticky=E)
		self.shape_types = ['Rectangle', 'Oval']
		self.shape_var = StringVar()
		self.shape_selector = ttk.Combobox(self.controls, values=self.shape_types, state='readonly', 
			textvariable=self.shape_var)
		self.shape_selector.grid(row=0, column=1, sticky=W)
		self.current_shape = None

		# Create color textbox
		self.color_label = ttk.Label(self.controls, text='Specify Color:')
		self.color_label.grid(row=1, column=0, sticky=E)
		self.color_var = StringVar()
		self.color_entry = ttk.Entry(self.controls, textvariable=self.color_var)
		self.color_entry.grid(row=1, column=1, sticky=W)
		self.draw_button = ttk.Button(self.controls, text='Draw!', command=self.draw)
		self.draw_button.grid(row=2, column=0, columnspan=2)

		# Create save textbox
		self.save_label = ttk.Label(self.controls, text='Shape Name:')
		self.save_label.grid(row=3, column=0, sticky=E)
		self.save_var = StringVar()
		self.save_entry = ttk.Entry(self.controls, textvariable=self.save_var)
		self.save_entry.grid(row=3, column=1, sticky=W)
		self.save_button = ttk.Button(self.controls, text='Save to disk', command=self.save)
		self.save_button.grid(row=4, column=0, columnspan=2)

		# Create saved shape selector
		self.select_saved = ttk.Label(self.controls, text='Select Saved Shape:')
		self.select_saved.grid(row=5, column=0, sticky=E)
		self.saved_shapes = []
		self.saved_shape_names = []
		self.load_shapes()
		self.saved_var = StringVar()
		self.saved_selector = ttk.Combobox(self.controls, values=self.saved_shape_names, state='readonly', 
			textvariable=self.saved_var)
		self.saved_selector.grid(row=5, column=1, sticky=W)
		self.draw_saved_button = ttk.Button(self.controls, text='Draw saved shape', command=self.draw_saved)
		self.draw_saved_button.grid(row=6, column=0, columnspan=2)

		# Create Quit button
		self.quit_button = ttk.Button(self.controls, text='Quit', command=self.quit)
		self.quit_button.grid(row=7, column=0, columnspan=2)

		# Create Messages label
		self.messages = ttk.Label(self.controls, text='Messages')
		self.messages.grid(row=8, column=0, columnspan=2)

		self.root.mainloop()

	def load_shapes(self):
		try:
			shape_file = open(FinalProject.shape_file_name)
			lines = shape_file.readlines()
			shape_file.close()
			i = 0
			while i < len(lines):
				name = lines[i].strip()
				stype = lines[i+1].strip()
				color = lines[i+2].strip()
				x1 = int(lines[i+3])
				y1 = int(lines[i+4])
				x2 = int(lines[i+5])
				y2 = int(lines[i+6])
				if stype == 'Rectangle':
					shape = Rectangle(self.canvas, color, [x1, y1, x2, y2])
				else:
					shape = Oval(self.canvas, color, [x1, y1, x2, y2])
				shape.set_name(name)
				self.saved_shapes.append(shape)
				self.saved_shape_names.append(name)
				i += 7
		except:
			pass

	def draw(self):
		self.canvas.delete('all')	# Clear the screen

		try:
			# Make sure user has selected a shape
			found = False
			for shape in self.shape_types:
				if self.shape_var.get() == shape:
					found = True
					break
			if not found:
				raise NoShape
			
			# Make sure user has entered a color
			if self.color_var.get() == '':
				raise NoColor

			coords = [100, 100, 800, 800]
			if self.shape_var.get() == self.shape_types[0]:
				self.current_shape = Rectangle(self.canvas, self.color_var.get(), coords)
			elif self.shape_var.get() == self.shape_types[1]:
				self.current_shape = Oval(self.canvas, self.color_var.get(), coords)
			else:
				raise NoShape

			self.current_shape.draw()
			self.messages.config(text='')
		except NoShape:
			self.messages.config(text='No shape selected')
		except NoColor:
			self.messages.config(text='Bad color')
		except:
			self.messages.config(text='Bad color')

	def draw_saved(self):
		try:
			if self.saved_var.get() == '':
				raise NoShape
			for shape in self.saved_shapes:
				if shape.name == self.saved_var.get():
					self.canvas.delete('all')			# Clear the screen
					shape.draw()						# Draw the shape
					self.messages.config(text='')		# Clear the message text
					return
			raise ShapeNotFound
		except NoShape:
			self.messages.config(text='You must select a shape first')
		except ShapeNotFound:
			self.messages.config(text='Unable to find that shape!')

	def save(self):
		try:
			if self.current_shape == None:
				raise NoShape
			if self.save_var.get() == '':
				raise NoName
			if len(self.saved_shapes) >= 5:
				raise MaxShapes

			# Save current shape to file
			shape_file = open(FinalProject.shape_file_name, 'a')
			shape_file.write(f"{self.save_var.get()}\n")
			if isinstance(self.current_shape, Rectangle):
				shape_file.write("Rectangle\n")
			else:
				shape_file.write("Oval\n")
			shape_file.write(f"{self.current_shape.color}\n")
			shape_file.write(f"{self.current_shape.coords[0]}\n")
			shape_file.write(f"{self.current_shape.coords[1]}\n")
			shape_file.write(f"{self.current_shape.coords[2]}\n")
			shape_file.write(f"{self.current_shape.coords[3]}\n")
			shape_file.close()

			# Name shape and add to saved shape list
			self.current_shape.set_name(self.save_var.get())
			self.saved_shapes.append(self.current_shape)

			# Add shape name to saved shape selector and clear name from textbox
			self.saved_shape_names.append(self.save_var.get())
			self.saved_selector.config(values=self.saved_shape_names)
			self.save_var.set('')

		except NoShape:
			self.messages.config(text='You must select and draw a shape first')
		except NoName:
			self.messages.config(text='You must enter a name for the shape first')
		except MaxShapes:
			self.messages.config(text='Maximum number of saved shapes reached (5)')

	def quit(self):
		exit(0)





fp = FinalProject()
